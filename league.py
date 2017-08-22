import discord
from discord.ext import commands
import requests
import json


lol_api = 'RGAPI-695ddbd2-474f-4639-a1ae-b8ba05cb8f86'


class LeagueofLegends():
    """Commands relating to League of Legends"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, aliases=['list', 'registered'],
                    help="list saved LoL igns for server")
    async def listign(self, ctx):
        with open('igns/igns-{}'.format(ctx.message.server.id), 'r+') as f:
            lines = f.readlines()
        await self.bot.say("Registered summoners:")
        for line in lines:
            await self.bot.say(line)


    @commands.command(pass_context=True, aliases=['register', 'add'],
                    help="add a LoL ign to server list")
    async def add_ign(self, ctx, *ign):
        ign = ' '.join(ign)

        resp = requests.get(
            'https://na1.api.riotgames.com/lol/summoner/v3/summoners/by-name/{}?api_key={}'.format(ign, lol_api))
        resp = json.loads(resp.text)
        print(resp)
        if 'status' not in resp:
            ign = resp['name']
        elif resp['status']['status_code'] == 404:
            await self.bot.say("{} is not a registered summoner".format(ign))
            return
        else:
            await self.bot.say("Summoner Error {}".format(str(resp['status']['status_code'])))
            return

        with open('igns/igns-{}'.format(ctx.message.server.id), 'a+') as f:
            f.write(ign+'\n')
        await self.bot.say("{} added".format(ign))

    @commands.command(pass_context=True, aliases=['delete', 'remove'],
                    help="remove a LoL ign from server list")
    async def remove_ign(self, ctx, *ign):
        ign = ' '.join(ign)

        resp = requests.get(
            'https://na1.api.riotgames.com/lol/summoner/v3/summoners/by-name/{}?api_key={}'.format(ign, lol_api))
        resp = json.loads(resp.text)
        print(resp)
        if 'status' not in resp:
            ign = resp['name']
        elif resp['status']['status_code'] == 404:
            await self.bot.say("{} is not a summoner".format(ign))
            return
        else:
            await self.bot.say("Summoner Error {}".format(str(resp['status']['status_code'])))
            return

        with open('igns/igns-{}'.format(ctx.message.server.id), 'r+') as f:
            lines = f.readlines()
        if ign+'\n' in lines:
            lines.remove(ign+'\n')
        else:
            await self.bot.say("{} is not on my summoner list".format(ign))
            return
        with open('igns/igns-{}'.format(ctx.message.server.id), 'w') as f:
            f.writelines(lines)
        await self.bot.say("{} removed".format(ign))


    @commands.command(pass_context=True, aliases=['ingame'],
                    help="check if all saved igns are in-game")
    async def check_ingame(self, ctx, *ign):
        if ign:
            ign = ' '.join(ign)
            await self.bot.say(gamestatus(ign))
        else:
            s = set()
            with open('igns/igns-{}'.format(ctx.message.server.id), 'r+') as f:
                for line in f:
                    s.add(line.replace('\n', '').lower())
            for ign in s:
                await self.bot.say(gamestatus(ign))


def gamestatus(summ):
    resp = requests.get(
        'https://na1.api.riotgames.com/lol/summoner/v3/summoners/by-name/{}?api_key={}'.format(summ, lol_api))
    resp = json.loads(resp.text)
    print(resp)
    if 'status' in resp and resp['status']['status_code'] == 404:
        return "{} is not a registered summoner".format(summ)
    elif 'status' in resp:
        return "Summoner Error {}".format(str(resp['status']['status_code']))
    sid = resp['id']
    name = resp['name']
    resp = requests.get(
        'https://na1.api.riotgames.com/lol/spectator/v3/active-games/by-summoner/{}?api_key={}'.format(sid, lol_api))
    resp = json.loads(resp.text)
    print(resp)
    if 'status' not in resp:
        mins = int(resp['gameLength'] / 60)
        secs = resp['gameLength'] % 60
        return "{} has been in a(n) {} game for {}:{}".format(name, resp['gameMode'], mins, secs)
    elif resp['status']['status_code'] == 404:
        return "{} is not in game".format(name)
    else:
        return "Game Error {}".format(str(resp['status']['status_code']))


def setup(bot):
    bot.add_cog(LeagueofLegends(bot))