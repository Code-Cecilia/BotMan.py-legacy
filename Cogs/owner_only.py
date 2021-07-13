import os
import sys

from discord.ext import commands
import discord
import asyncio
import traceback


class OwnerOnly(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True, name='shutdown', description='Hidden command, youre not supposed to access this.\n'
                                                                'Now off you go. Nothing to see here.')  # thanks, Yuichiro
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

    @commands.command(name='reload', description="Reload all/one of the bot's cogs.\n"
                                                 "This is Owner-only, so don't have any funny ideas.")
    @commands.is_owner()
    async def reload(self, ctx, cog=None):
        if not cog:
            async with ctx.typing():
                embed = discord.Embed(title="Reloading all cogs!", color=0x808080, timestamp=ctx.message.created_at)
                for ext in os.listdir("./Cogs/"):
                    if ext.endswith(".py") and not ext.startswith("_"):
                        try:
                            self.bot.unload_extension(f"Cogs.{ext[:-3]}")
                            self.bot.load_extension(f"Cogs.{ext[:-3]}")
                            embed.add_field(
                                name=f"Reloaded: `{ext}`",
                                value='\uFEFF',
                                inline=False
                            )
                        except Exception as e:
                            embed.add_field(
                                name=f"Failed to reload: `{ext}`",
                                value=e,
                                inline=False
                            )
                        await asyncio.sleep(0.5)
                await ctx.send(embed=embed)
        else:
            async with ctx.typing():
                embed = discord.Embed(
                    title="Reloading all cogs!", color=0x808080, timestamp=ctx.message.created_at)
                ext = f"{cog.lower()}.py"
                if not os.path.exists(f"./cogs/{ext}"):
                    embed.add_field(name=f"Failed to reload: `{ext}`",value="This cog does not exist.",inline=False)

                elif ext.endswith(".py") and not ext.startswith("_"):
                    try:
                        self.bot.unload_extension(f"Cogs.{ext[:-3]}")
                        self.bot.load_extension(f"Cogs.{ext[:-3]}")
                        embed.add_field(name=f"Reloaded: `{ext}`",value='\uFEFF',inline=False)
                    except Exception:
                        desired_trace = traceback.format_exc()
                        embed.add_field(
                            name=f"Failed to reload: `{ext}`",
                            value=desired_trace,
                            inline=False
                        )
                await ctx.send(embed=embed)
def setup(bot):
    bot.add_cog(OwnerOnly(bot))
