import discord
from discord.ext import commands
import requests
import json

lol_api = 'RGAPI-695ddbd2-474f-4639-a1ae-b8ba05cb8f86'

Client = discord.Client()
bot_prefix= "!"
client = commands.Bot(command_prefix=bot_prefix)


@client.event
async def on_ready():
    print("Bot Online!")
    print("Name: {}".format(client.user.name))
    print("ID: {}".format(client.user.id))


@client.command(pass_context=True, aliases=['whatismypurpose', 'purpose'])
async def whatisyourpurpose(ctx):
    await client.say("I pass butter.")
    await client.say("Oh my god.")


@client.command(pass_context=True)
async def debug(ctx, *args):
    if ctx.message.author.top_role.position == len(ctx.message.server.roles)-1:
        try:
            out = (eval(' '.join(args)))
            if out:
                await client.say(str(out))
        except Exception as e:
            await client.say(str(e))
    else:
        await client.say("You don't have permissions for this command.")


@client.command(pass_context=True, aliases=['purge'])
async def clear(ctx, count):
    if ctx.message.author.server_permissions.manage_messages:
        await client.purge_from(ctx.message.channel, limit=int(count)+1)
    else:
        await client.say("You don't have permissions for this command.")


@client.command(pass_context=True, aliases=['list', 'registered'])
async def listign(ctx):
    with open('igns/igns-{}'.format(ctx.message.server.id), 'r+') as f:
        lines = f.readlines()
    await client.say("Registered summoners:")
    for line in lines:
        await client.say(line)


@client.command(pass_context=True, aliases=['register', 'add'])
async def addign(ctx, *ign):
    ign = ' '.join(ign)

    resp = requests.get(
        'https://na1.api.riotgames.com/lol/summoner/v3/summoners/by-name/{}?api_key={}'.format(ign, lol_api))
    resp = json.loads(resp.text)
    print(resp)
    if 'status' not in resp:
        ign = resp['name']
    elif resp['status']['status_code'] == 404:
        await client.say("{} is not a registered summoner".format(ign))
        return
    else:
        await client.say("Summoner Error {}".format(str(resp['status']['status_code'])))
        return

    with open('igns/igns-{}'.format(ctx.message.server.id), 'a+') as f:
        f.write(ign+'\n')
    await client.say("{} added".format(ign))


@client.command(pass_context=True, aliases=['delete', 'remove'])
async def removeign(ctx, *ign):
    ign = ' '.join(ign)

    resp = requests.get(
        'https://na1.api.riotgames.com/lol/summoner/v3/summoners/by-name/{}?api_key={}'.format(ign, lol_api))
    resp = json.loads(resp.text)
    print(resp)
    if 'status' not in resp:
        ign = resp['name']
    elif resp['status']['status_code'] == 404:
        await client.say("{} is not a summoner".format(ign))
        return
    else:
        await client.say("Summoner Error {}".format(str(resp['status']['status_code'])))
        return

    with open('igns/igns-{}'.format(ctx.message.server.id), 'r+') as f:
        lines = f.readlines()
    if ign+'\n' in lines:
        lines.remove(ign+'\n')
    else:
        await client.say("{} is not on my summoner list".format(ign))
        return
    with open('igns/igns-{}'.format(ctx.message.server.id), 'w') as f:
        f.writelines(lines)
    await client.say("{} removed".format(ign))


@client.command(pass_context=True, aliases=['ingame'])
async def checkingame(ctx, *ign):
    if ign:
        ign = ' '.join(ign)
        await client.say(gamestatus(ign))
    else:
        s = set()
        with open('igns/igns-{}'.format(ctx.message.server.id), 'r+') as f:
            for line in f:
                s.add(line.replace('\n', '').lower())
        for ign in s:
            await client.say(gamestatus(ign))


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


def get_self(ctx):
    bots = [member for member in list(client.get_all_members()) if member.id == client.user.id]
    this_server = [member for member in bots if member.server == ctx.message.server][0]
    return this_server


client.run("MzQ5MDQxNDczMjU1MTEyNzEw.DHy9cA.ko_yXYlnIcauv2g9bAxmAw-T8GA")
