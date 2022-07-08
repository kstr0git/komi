import asyncio
import hikari
import lightbulb

adminPlug = lightbulb.Plugin('Admin')

#Command to delete messages
@adminPlug.command
@lightbulb.add_checks(
    lightbulb.has_guild_permissions(hikari.Permissions.MANAGE_MESSAGES),
    lightbulb.guild_only
    )
@lightbulb.option('messages', 'The number of messages to delete', type=int, required=True,)
@lightbulb.command('purge', 'Purge messages in the channel', aliases=['clear', 'delete'])
@lightbulb.implements(lightbulb.SlashCommand)
async def purge(ctx):
    msgNum = ctx.options.messages
    channel = ctx.channel_id 
    msgs = await ctx.bot.rest.fetch_messages(channel).limit(msgNum)
    await ctx.bot.rest.delete_messages(channel, msgs)

    response = await ctx.respond(f'{len(msgs)} messages deleted')
    await asyncio.sleep(5)
    await response.delete()

#Command to issue warnings to users
@adminPlug.command
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.KICK_MEMBERS))
@lightbulb.option('member', 'Member you are warning', type=hikari.User, required=True,)
@lightbulb.option('reason', 'reason you are warning member', required=False, default='No reason given', type=str)
@lightbulb.command('warn', 'Warn member of rule violation (Admin)')
@lightbulb.implements(lightbulb.SlashCommand)
async def warn(ctx):
    member = ctx.options.member
    reason = ctx.options.reason 
    guild = ctx.get_guild()

    await ctx.respond(embed=hikari.Embed(
        title='Warning sent', 
        description=f'A warning has been sent to {member} for {reason}', 
        color=hikari.Color.of('#c27c0e')))
    
    await member.send(embed=hikari.Embed(
        title="You've recieved a warning", 
        description=f"{guild} Warning: You've been warned for the following: {reason}. Further warnings will result in potential ban", 
        color=hikari.Color.of('#c27c0e')))

def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(adminPlug)