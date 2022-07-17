import asyncio
from audioop import add
from genericpath import exists
from itertools import count
import hikari
import lightbulb
import sqlite3
import datetime

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
@lightbulb.option('messages', 'The number of messages to delete', type=int, required=True, min_value=1, max_value=1000)
@lightbulb.command('purge', 'Purge messages in the channel')
@lightbulb.implements(lightbulb.SlashCommand)
async def purge(ctx):
    try:
        msgNum = ctx.options.messages
        channel = ctx.channel_id
        #Fetches only the messages younger than 14 days when command is invoked (bots can only delete messages less than 14 days)
        msgs = await ctx.bot.rest.fetch_messages(channel).take_until(lambda m: datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=14) > m.created_at).limit(msgNum)
        await ctx.bot.rest.delete_messages(channel, msgs)

        response = await ctx.respond(f'{len(msgs)} messages deleted.')
        await asyncio.sleep(5)
        await response.delete()
        
    except:
        response = await ctx.respond('Could not find any messages to delete.')
        await asyncio.sleep(5)
        await response.delete()

#Command to issue warnings to users and log warning on SQL database
@adminPlug.command
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.ADMINISTRATOR))
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
                count=1
                c.execute("INSERT INTO warnings (memberID, warningCount) VALUES (?,?)", (memID, 1))
            else:
                count=result[0]+1
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
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.ADMINISTRATOR))
@lightbulb.option('member', 'Member you are checking', type=hikari.User, required=True,)
@lightbulb.command('warn-count', "Checks the total number of times a member has had a warning", ephemeral=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def warnCount(ctx):
    member = ctx.options.member
    db = sqlite3.connect('warnings.db')
    c = db.cursor()
    try:
        c.execute(f"SELECT warningCount FROM warnings WHERE memberID={member.id}")
        result=c.fetchone()
        count=result[0]
        c.close()
        db.close()

        if result is None:
            await ctx.respond(f'{member} currently has not no warnings.')
        else:
            await ctx.respond(f'{member} has recieved a total of **{count}** warnings.')
    except:
        await ctx.respond('You do not have the permissions to run this command.')

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

#Command to timeout users
@adminPlug.command
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.ADMINISTRATOR))
@lightbulb.option('reason', 'Reason you are timingout the member', required=False, default='No reason given', type=str)
@lightbulb.option('member', 'Member to timeout', required=True, type=hikari.User)
@lightbulb.option('minutes', 'How long you would like the member to be timeouted for in minutes', required=True, type=int)
@lightbulb.command('timeout', 'Timeouts a member', ephemeral=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def timeout(ctx: lightbulb.Context):
    targetTime = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=ctx.options.minutes)
    member = ctx.options.member
    reason = ctx.options.reason
    author = ctx.author

    try:
        if member.id == author.id:
            await ctx.respond('You cannot time yourself out')
        else:
            await member.send(f"You've been timedout for the following reason: **{reason}** \n The timeout will expire at {targetTime}")
            await member.edit(communication_disabled_until=targetTime)
            ctx.respond(f'{member} has been timedout until {targetTime}')
    except:
        await ctx.respond('You do not have the permissions to run this command.')

#Command to ban members 
@adminPlug.command
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.ADMINISTRATOR))
@lightbulb.option("reason", "Reason for the ban",required=False, default='No reason given', type=str)
@lightbulb.option("member", "Member to ban",type=hikari.User, required=True)
@lightbulb.command('ban', 'Bans a member from the server')
@lightbulb.implements(lightbulb.SlashCommand)
async def ban(ctx):
    guild = ctx.get_guild()
    member = ctx.options.member
    reason = ctx.options.reason
    author = ctx.author

    try:
        if member.id == author.id:
            await ctx.respond('You cannot ban yourself')
        else:
            await ctx.bot.rest.ban_user(guild, member.id)
            await ctx.respond(f'{member} has been banned for the following reason: **{reason}**.')
    except:
        await ctx.respond('You do not have the permissions to run this command.')
    
def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(adminPlug)