import discord
from discord.ext import commands

class Mod():
    """Commands used to help moderate a server"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, aliases=['purge'],
                 help="delete last <count> messages")
    async def clear(self, ctx, count):
        if ctx.message.author.server_permissions.manage_messages:
            await self.bot.purge_from(ctx.message.channel, limit=int(count) + 1)
        else:
            await self.bot.say("You don't have permissions for this command.")


def setup(bot):
    bot.add_cog(Mod(bot))