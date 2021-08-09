import random
import time

import discord
from discord.ext import commands

from assets import count_lines, get_color, random_assets


class BotInfo(commands.Cog, description="Information on various aspects of the bot."):
    def __init__(self, bot):
        self.bot = bot
        self.startTime = time.monotonic()

    @commands.command(name='ping', description='Returns the latency in milliseconds.')
    async def ping_command(self, ctx):
        latency = float(self.bot.latency) * 1000
        latency = round(latency, 2)
        await ctx.send(f'Pong! `Latency: {latency}ms`')

    @commands.command(name="vote", description="Vote for BotMan on top.gg!")
    async def vote_topgg(self, ctx):
        embed = discord.Embed(title=f"{ctx.author.display_name}, you can vote for me here!",
                              description="__[Link to my (very own) page!]("
                                          "https://top.gg/bot/845225811152732179/vote)__",
                              color=discord.Color.random())
        embed.set_footer(text=f"It's the gesture that counts first, so thanks a lot, {ctx.author.name}!")
        await ctx.send(embed=embed)

    @commands.command(name='countlines', aliases=['countline'], description='Counts the number of lines of python code '
                                                                            'the bot currently has.')
    async def countlines_func(self, ctx):
        lines = count_lines.countlines('./')
        final_str = random.choice(random_assets.countlines_responses).format(lines)
        embed = discord.Embed(title=final_str, color=get_color.get_color(self.bot.user))
        await ctx.send(embed=embed)

    @commands.command(name='botinfo', aliases=['clientinfo', 'botstats'],
                      description='Returns information about the bot.')
    async def stats(self, ctx):
        dpyVersion = f"Version {discord.__version__}"
        serverCount = len(self.bot.guilds)
        memberCount = len(set(self.bot.get_all_members()))
        latency = float(self.bot.latency) * 1000
        latency = f"{int(latency)} ms"
        source = "__[Github](https://github.com/Code-Cecilia/BotMan.py)__"
        guren = f"__[Guren Ichinose](https://github.com/Code-Cecilia/Guren)__"
        now = time.monotonic()
        uptime_seconds = int(now - self.startTime)
        m, s = divmod(uptime_seconds, 60)
        h, m = divmod(m, 60)
        d, h = divmod(h, 24)

        embed = discord.Embed(title=f'{self.bot.user.name} Stats', description='\uFEFF',
                              colour=get_color.get_color(self.bot.user),
                              timestamp=ctx.message.created_at)
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.add_field(name='Discord.Py', value=dpyVersion, inline=True)
        embed.add_field(name='Total Guilds',
                        value=str(serverCount), inline=True)
        embed.add_field(name='Total Users', value=str(
            memberCount), inline=True)
        embed.add_field(name='Latency', value=str(latency), inline=True)
        embed.add_field(name="Uptime", value=f"{d}d, {h}h, {m}m, {s}s", inline=True)
        embed.add_field(name='Talk to my maker!',
                        value="__[Mahasvan](https://discord.com/users/775176626773950474)__", inline=True)
        embed.add_field(name="Source", value=source, inline=True)
        embed.add_field(name="Sibling Bot", value=guren, inline=True)
        embed.add_field(name="Found an issue?",
                        value="__[Report Here!](https://github.com/Code-Cecilia/BotMan.py/issues)__", inline=True)
        embed.add_field(name='Invite Me!',
                        value=f"__[Link to invite](https://discord.com/oauth2/authorize"
                              f"?client_id={self.bot.user.id}&permissions=4294836215&scope=bot)__",
                        inline=True)
        embed.add_field(name="Support Server",
                        value="__[Link](https://discord.gg/pVEPfA3N3U)__", inline=True)
        embed.set_footer(
            text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name="uptime", description="Returns how long I have been awake.")
    async def get_uptime(self, ctx):
        now = time.monotonic()
        uptime_seconds = int(now - self.startTime)
        m, s = divmod(uptime_seconds, 60)
        h, m = divmod(m, 60)
        d, h = divmod(h, 24)
        embed = discord.Embed(title="Uptime", description=f"I have been awake for **{d}** days, **{h}** hours, "
                                                          f"**{m}** minutes and **{s}** seconds.",
                              color=get_color.get_color(self.bot.user))
        embed.set_footer(text=random.choice(random_assets.uptime_footers))
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(BotInfo(bot))
