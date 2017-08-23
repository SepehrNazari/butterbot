import discord
from discord.ext import commands

Client = discord.Client()
bot_prefix= "!"
bot = commands.Bot(command_prefix=bot_prefix)
startup_extensions = ['league', 'mod']

@bot.event
async def on_ready():
    print("Bot Online!")
    print("Name: {}".format(bot.user.name))
    print("ID: {}".format(bot.user.id))
    print("-----------------------")


@bot.command(pass_context=True, aliases=['whatismypurpose', 'purpose'])
async def whatisyourpurpose(ctx):
    await bot.say("I pass butter.")
    await bot.say("Oh my god.")


@bot.command(pass_context=True, hidden=True)
async def debug(ctx, *args):
    if ctx.message.author.top_role.position == len(ctx.message.server.roles)-1:
        try:
            out = exec(' '.join(args))
            if out:
                await bot.say(str(out))
        except Exception as e:
            await bot.say(str(e))
    else:
        await bot.say("You don't have permissions for this command.")

        
@bot.command(pass_context=True)
async def die(ctx):
    if ctx.message.author.top_role.position == len(ctx.message.server.roles)-1:
        try:
            await ctx.bot.logout()
    else:
        await bot.say("Gladly. *Kills self*")

if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

    bot.run("MzQ5MDQxNDczMjU1MTEyNzEw.DH5g1w.Vn6iK_lurC3Fnj6k2kMQameowF0")
