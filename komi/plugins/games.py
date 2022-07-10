import asyncio
import hikari
import lightbulb
import requests
import json
import random

gamePlug = lightbulb.Plugin('Games')

#Reads the Steam API key from the static/Steamkey
with open('./static/steamKey') as sk:
    apiKey = sk.read()
    
#Command that suggests games from steam libary
@gamePlug.command
@lightbulb.option ('vanity', 'Enter your Steam vanity url username or Steam ID', required=True)
@lightbulb.option ('unplayed', 'Chose a game from the libary with zero playtime', required=False, type=bool, default=False)
@lightbulb.command('steam-game', 'Randomly selects a game from your Steam libary using URL')
@lightbulb.implements(lightbulb.SlashCommand)
async def steamGame(ctx):
    s = ctx.options.vanity
    try:
        #if statement verifies whether a vanity URL has been used or a Steam ID
        if s.isnumeric() != True:
            rQ1 = requests.get(f'https://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key={apiKey}&vanityurl=' + s)    
            steamID = json.loads(rQ1.content) ["response"]["steamid"]
        else:
            steamID = s

        #Steam ID is passed into a request to pull user's Steam Libary 
        rQ2 = requests.get(f'https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?key={apiKey}&steamid={steamID}&include_appinfo=true')
        gameList = json.loads(rQ2.content) ["response"]["games"]

        games = []
        unplayedgames = []
        for i in gameList:
            games.append(i["name"])
            if(i['playtime_forever'] == 0):
                unplayedgames.append(i["name"])

        if ctx.options.unplayed != True:
            await ctx.respond('How about ' + random.choice(games) + '?')
        else:
            await ctx.respond('How about ' + random.choice(unplayedgames) + '?')
    except:
        await ctx.respond("S-s-sorry... I was unable to find you on Steam... Please check your Steam URL or maybe your account is private")

def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(gamePlug)