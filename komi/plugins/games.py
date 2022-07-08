import asyncio
import hikari
import lightbulb
import requests
import json
import random

gamePlug = lightbulb.Plugin('Games')

with open('./static/steamKey') as sk:
    apiKey = sk.read()
    
@gamePlug.command
@lightbulb.option ('username', 'Enter your Steam vanity url username or Steam ID')
@lightbulb.command('game', 'Randomly selects a game from your Steam libary using URL')
@lightbulb.implements(lightbulb.SlashCommand)
async def game(ctx):
    s = ctx.options.username
    try:
        if s.isnumeric() != True:
            rQ1 = requests.get(f'https://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key={apiKey}&vanityurl=' + s)    
            steamID = json.loads(rQ1.content) ["response"]["steamid"]
        else:
            steamID = s
            
        rQ2 = requests.get(f'https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?key={apiKey}&steamid={steamID}&include_appinfo=true')
        gameList = json.loads(rQ2.content) ["response"]["games"]

        games = []
        for i in gameList:
            games.append(i["name"])

        await ctx.respond('You should play ' + random.choice(games))
    except:
        await ctx.respond("S-s-sorry... I was unable to find you on Steam... Please check your Steam URL or maybe you're account is private")

def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(gamePlug)