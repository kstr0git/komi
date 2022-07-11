import asyncio
from audioop import add
from genericpath import exists
from itertools import count
import warnings
import hikari
import lightbulb
import sqlite3

adminPlug = lightbulb.Plugin('Admin')

db = sqlite3.connect('warnings.db')
c = db.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS warnings (
    memberID INTEGER,
    warningCount INTEGER
    )""")
c.close
db.close()

#Command to delete messages
@adminPlug.command
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.MANAGE_MESSAGES), lightbulb.guild_only)
@lightbulb.option('messages', 'The number of messages to delete', type=int, required=True,)
@lightbulb.command('purge', 'Purge messages in the channel')
@lightbulb.implements(lightbulb.SlashCommand)
async def purge(ctx):
    try:
        msgNum = ctx.options.messages
        channel = ctx.channel_id 
        msgs = await ctx.bot.rest.fetch_messages(channel).limit(msgNum)
        await ctx.bot.rest.delete_messages(channel, msgs)

        response = await ctx.respond(f'{len(msgs)} messages deleted')
        await asyncio.sleep(5)
        await response.delete()
        
    except:
        response = await ctx.respond('You can only bulk delete messages posted within 2 weeks. No messages deleted, reduce the number of messages to purge.')
        await asyncio.sleep(5)
        await response.delete()

#Command to issue warnings to users and log warning on SQL database
@adminPlug.command
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.KICK_MEMBERS))
@lightbulb.option('member', 'Member you are warning', type=hikari.User, required=True,)
@lightbulb.option('reason', 'reason you are warning member', required=False, default='No reason given', type=str)
@lightbulb.command('warn', 'Warn member of rule violation (Admin)',ephemeral=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def warn(ctx):
    author = ctx.author
    member = ctx.options.member
    reason = ctx.options.reason 
    guild = ctx.get_guild()
    memID = ctx.options.member.id
    
    try:
        if memID == author.id:
            await ctx.respond('You cannot warn yourself')
        else:
            await ctx.respond(f'A warning has been sent to {member} for {reason}')
            db = sqlite3.connect('warnings.db')
            c = db.cursor()
            c.execute(f"SELECT warningCount FROM warnings WHERE memberID={memID}")
            result=c.fetchone()
    
            #checks if entry exists on the warning database and creates one if one doesn't exist
            if result is None:
                c.execute("INSERT INTO warnings (memberID, warningCount) VALUES (?,?)", (memID, 1))
                count=1
            else:
                #Very messy way of converting tuple to string (future fix pending)
                count=int(str(result).strip("(,)"))+1
                c.execute("UPDATE warnings SET warningCount=? WHERE memberID=?", (count, memID))
            db.commit()
            c.close()
            db.close()

            await member.send(embed=hikari.Embed(
                title=f"You've recieved a warning", 
                description=f"{guild} Warning: You've been warned for the following reason: **{reason}**. \n You currently have **{count}** warnings. Further warnings will could result in potential ban", 
                color=hikari.Color.of('#c27c0e')
                ))
    except:
        await ctx.respond('You do not have the permissions to run this command.')

#Returns a count of warnings
@adminPlug.command
@lightbulb.command('warn-count', "Checks the total number of times you've had a warning", ephemeral=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def warnCount(ctx):
    db = sqlite3.connect('warnings.db')
    c = db.cursor()
    author = ctx.author.id
    c.execute(f"SELECT warningCount FROM warnings WHERE memberID={author}")
    result=c.fetchone()
    count=int(str(result).strip("(,)"))
    c.close()
    db.close()
    
    await ctx.respond(f"You've recieved a total of **{count}** warnings. \n You can request to appeal warnings via `/appeal`")

#Command to anonymously report users to mods 
@adminPlug.command
@lightbulb.option('reason', 'Reason you are reporting the member', required=True, type=str)
@lightbulb.option('member', 'Member you wish to report', type=hikari.User, required=True,)
@lightbulb.command('report', 'Reports a member of the server to the moderation team', ephemeral=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def report(ctx):
    author = ctx.author
    member = ctx.options.member
    reason = ctx.options.reason

    if member.id == author.id:
        await ctx.respond('You cannot report yourself')
    else:
        await ctx.respond(f'A report has been made against {member} for **{reason}**. \n The mods have been notified')

        #972183435428921420 is the channel ID for #report-queue on my discord server
        await ctx.bot.rest.create_message(972183435428921420, embed=hikari.Embed(
            title=f'Report issued to {member} by {author}',
            description=f'A report has been made against {member} for **{reason}**. \n Please could you investigate this issue and attempt to resolve any conflicts. Perhaps issue a warning?',
            color=hikari.Color.of('#14a2d3')
            ))
    
def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(adminPlug)