import os
import hikari
import lightbulb

from komi import guildId

with open('./static/token') as t:
    _token = t.read().strip()

client = lightbulb.BotApp(
    token=_token,
    default_enabled_guilds=guildId,
    intents=hikari.Intents.ALL,
    banner='komi',
    )

client.load_extensions_from('./komi/plugins')

@client.command()
@lightbulb.command("ping", "Shows the latency for the client")
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def ping(ctx: lightbulb.Context) -> None:
    await ctx.respond(f"Client latency: {round(client.heartbeat_latency) * 100:.2f}ms")

client.run(status=hikari.Status.ONLINE,
    activity=hikari.Activity(
        name="for Commands",
        type=hikari.ActivityType.WATCHING))