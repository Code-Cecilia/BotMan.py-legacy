import os
import sys

from discord.ext import commands


class OwnerOnly(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True, name='shutdown', descriptiob='Hidden command, youre not supposed to access this.\n'
                                                                'Now off you go. Nothing to see here.')
    @commands.is_owner()
    async def shutdown_command(self, ctx):
        await ctx.send('Shutting down...')
        await self.bot.close()

    @commands.command(hidden=True, name='reboot', description='Hidden command, youre not supposed to access this.\n'
                                                              'Now off you go. Nothing to see here.')
    @commands.is_owner()
    async def reboot(self, ctx):
        await ctx.send('Rebooting...')
        os.execv(sys.executable, ['python'] + sys.argv)


def setup(bot):
    bot.add_cog(OwnerOnly(bot))
