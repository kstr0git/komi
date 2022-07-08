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

@client.listen(hikari.StartedEvent)
async def on_started(event):
    print('Bot has started')

@client.command()
@lightbulb.command("ping", "Shows the latency for the client")
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def ping(ctx: lightbulb.Context) -> None:
    await ctx.respond(f"Client latency: {round(client.heartbeat_latency) * 100:.2f}ms")

def run() -> None:
    if os.name != 'nt':
        import uvloop
        uvloop.install()
    
    client.run()