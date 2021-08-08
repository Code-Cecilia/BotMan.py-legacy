import random
import time

import discord
from discord.ext import commands

from assets import count_lines

countlines_responses = ["I am made of _{0}_ lines of python code. Pretty cool, huh?",
                        r"My owner has written _{0}_ lines of code in my brain. I a-a-am ... _glitches out_",
                        "I have _{0}_ lines of python code as my insides. That's pretty cool to me, you know...",
                        "Oh no! How did _{0}_ lines of python code get inside me? _I'm scared..._",
                        "I am made of _{0}_ lines of python code. What can I say except 😎",
                        "Some poor soul wrote _{0}_ lines of python code to give me a life."]


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
        final_str = random.choice(countlines_responses).format(lines)
        await ctx.send(final_str)

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
        days = int(uptime_seconds // (3600 * 24))
        hours = int(uptime_seconds // 3600)
        minutes = int(uptime_seconds // 60)
        seconds = int(uptime_seconds % 60)

        embed = discord.Embed(title=f'{self.bot.user.name} Stats', description='\uFEFF', colour=discord.Color.random(),
                              timestamp=ctx.message.created_at)
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.add_field(name='Discord.Py', value=dpyVersion, inline=True)
        embed.add_field(name='Total Guilds',
                        value=str(serverCount), inline=True)
        embed.add_field(name='Total Users', value=str(
            memberCount), inline=True)
        embed.add_field(name='Latency', value=str(latency), inline=True)
        embed.add_field(name="Uptime", value=f"{days}d, {hours}h, {minutes}m, {seconds}s", inline=True)
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

    @commands.command(name="uptime")
    async def get_uptime(self, ctx):
        now = time.monotonic()
        uptime_seconds = int(now - self.startTime)
        days = int(uptime_seconds // (3600 * 24))
        hours = int(uptime_seconds // 3600)
        minutes = int(uptime_seconds // 60)
        seconds = int(uptime_seconds % 60)
        await ctx.send(f"I have been awake for _{days} days, {hours} hours, {minutes} minutes and {seconds} seconds_.")


def setup(bot):
    bot.add_cog(BotInfo(bot))
