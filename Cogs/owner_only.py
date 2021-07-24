import os
import sys

from discord.ext import commands
import discord
import asyncio
import traceback


class OwnerOnly(commands.Cog, description='A bunch of owner-only commands.\n'
                                          'You probably can\'t see the list of commands.\n'
                                          'This is because you are not the bot\'s owner.'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='shutdown', description='Hidden command, youre not supposed to access this.\n'
                                                   'Now off you go. Nothing to see here.')  # thanks, Yuichiro
    @commands.is_owner()
    async def shutdown_command(self, ctx):
        await ctx.send('Shutting down...')
        await self.bot.close()

    @commands.command(name='reboot', description='Hidden command, youre not supposed to access this.\n'
                                                 'Now off you go. Nothing to see here.')
    @commands.is_owner()
    async def reboot(self, ctx):
        async with ctx.typing():
            await ctx.send('Rebooting...')
            os.execv(sys.executable, ['python'] + sys.argv)

    @commands.command(name='reload', description="Reload all/one of the bot's cogs.\n"
                                                 "This is Owner-only, so don't have any funny ideas.", )
    @commands.is_owner()
    async def reload(self, ctx, cog=None):
        async with ctx.typing():
            if not cog:
                embed = discord.Embed(title="Reloading cogs!", color=discord.Color.random(),
                                      timestamp=ctx.message.created_at)
                for ext in os.listdir("./Cogs/"):
                    if ext.endswith(".py") and not ext.startswith("_"):
                        try:
                            self.bot.unload_extension(f"Cogs.{ext[:-3]}")
                            self.bot.load_extension(f"Cogs.{ext[:-3]}")
                            embed.add_field(
                                name=f"Reloaded: `{ext}`", value='\uFEFF', inline=False)
                        except Exception as e:
                            embed.add_field(
                                name=f"Failed to reload: `{ext}`", value=str(e), inline=False)
                        await asyncio.sleep(0.5)
                await ctx.send(embed=embed)
                return

            """ Now the code for reloading One cog comes into play"""

            embed = discord.Embed(
                title="Reloading cogs!", color=discord.Color.random(), timestamp=ctx.message.created_at)
            ext = f"{cog.lower()}.py"
            if not os.path.exists(f"./cogs/{ext}"):
                embed.add_field(
                    name=f"Failed to reload: `{ext}`", value="This cog does not exist.", inline=False)

            elif ext.endswith(".py") and not ext.startswith("_"):
                try:
                    self.bot.unload_extension(f"Cogs.{ext[:-3]}")
                    self.bot.load_extension(f"Cogs.{ext[:-3]}")
                    embed.add_field(
                        name=f"Reloaded: `{ext}`", value='\uFEFF', inline=False)
                except Exception:
                    desired_trace = traceback.format_exc()
                    embed.add_field(
                        name=f"Failed to reload: `{ext}`", value=desired_trace, inline=False)
            await ctx.send(embed=embed)

    @commands.command(name='load', description='Loads a Cog.')
    @commands.is_owner()
    async def load_cog(self, ctx, cog_file_name):
        embed = discord.Embed(title=f"Loading Cog {cog_file_name}.py!", color=discord.Color.random(),
                              timestamp=ctx.message.created_at)
        if os.path.exists(f"./Cogs/{cog_file_name}.py"):
            try:
                self.bot.load_extension(f"Cogs.{cog_file_name}")
                embed.add_field(
                    name=f"Loaded: `{cog_file_name}.py`", value='\uFEFF', inline=False)
            except Exception as e:
                embed.add_field(
                    name=f"Failed to load: `{cog_file_name}.py`", value=str(e), inline=False)
            await ctx.send(embed=embed)

    @commands.command(name='unload')
    @commands.is_owner()
    async def unload_cog(self, ctx, cog_file_name):
        embed = discord.Embed(title=f"Unloading Cog {cog_file_name}.py!", color=discord.Color.random(),
                              timestamp=ctx.message.created_at)
        if os.path.exists(f"./Cogs/{cog_file_name}.py"):
            try:
                self.bot.unload_extension(f"Cogs.{cog_file_name}")
                embed.add_field(
                    name=f"Unloaded: `{cog_file_name}.py`", value='\uFEFF', inline=False)
            except Exception as e:
                embed.add_field(
                    name=f"Failed to unload: `{cog_file_name}.py`", value=str(e), inline=False)
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(OwnerOnly(bot))
