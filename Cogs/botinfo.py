import os
import platform
import random
import time

import discord
import psutil
import speedtest
from discord.ext import commands

from assets import count_lines, get_color, random_assets


class BotInfo(commands.Cog, description="Information on various aspects of the bot."):
    def __init__(self, bot):
        self.bot = bot
        self.startTime = time.monotonic()
        self.speedtest = speedtest.Speedtest()
        self.last_speedtest_dict = {}

    @commands.command(name='ping', description='Returns the latency in milliseconds.')
    async def ping_command(self, ctx):
        latency = float(self.bot.latency) * 1000
        latency = round(latency, 2)  # convert to float with 2 decimal places
        await ctx.send(f'Pong! `Latency: {latency}ms`')

    @commands.command(name="vote", description="Vote for BotMan on top.gg!")
    async def vote_topgg(self, ctx):
        embed = discord.Embed(title=f"{ctx.author.display_name}, you can vote for me here!",
                              description="__[Link to my (very own) page!]("
                                          "https://top.gg/bot/845225811152732179/vote)__",
                              color=discord.Color.blue())
        embed.set_footer(
            text=f"It's the gesture that counts first, so thanks a lot, {ctx.author.name}!")
        await ctx.send(embed=embed)

    @commands.command(name='countlines', aliases=['countline'], description='Counts the number of lines of python code '
                                                                            'the bot currently has.')
    async def countlines_func(self, ctx):
        lines = count_lines.countlines('./')  # get lines
        final_str = random.choice(
            random_assets.countlines_responses).format(lines)  # get response sentence
        embed = discord.Embed(
            title=final_str, color=get_color.get_color(self.bot.user))
        await ctx.send(embed=embed)

    @commands.command(name='botinfo', aliases=['clientinfo', 'botstats'],
                      description='Returns information about the bot.')
    async def stats(self, ctx):
        dpyVersion = f"Version {discord.__version__}"
        serverCount = len(self.bot.guilds)
        memberCount = len(set(self.bot.get_all_members()))  # returns a list, so we're getting the length of that list
        latency = float(self.bot.latency) * 1000
        latency = f"{int(latency)} ms"  # integer is good enough in this case
        source = "__[Github](https://github.com/Code-Cecilia/BotMan.py)__"
        guren = f"__[Guren Ichinose](https://github.com/Code-Cecilia/Guren)__"
        now = time.monotonic()
        uptime_seconds = int(now - self.startTime)
        m, s = divmod(uptime_seconds, 60)  # getting the uptime mins, secs, hrs, days
        h, m = divmod(m, 60)
        d, h = divmod(h, 24)

        embed = discord.Embed(title=f'{self.bot.user.name} Stats', description='\uFEFF',
                              color=get_color.get_color(ctx.guild.me),
                              timestamp=ctx.message.created_at)
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.add_field(name='Discord.Py', value=dpyVersion, inline=True)
        embed.add_field(name='Total Guilds',
                        value=str(serverCount), inline=True)
        embed.add_field(name='Total Users', value=str(
            memberCount), inline=True)
        embed.add_field(name='Latency', value=str(latency), inline=True)
        embed.add_field(
            name="Uptime", value=f"{d}d, {h}h, {m}m, {s}s", inline=True)
        embed.add_field(name='Talk to my maker!',
                        value="__[Mahasvan](https://discord.com/users/775176626773950474)__", inline=True)
        embed.add_field(name="Source", value=source, inline=True)
        embed.add_field(name="Sibling Bot", value=guren, inline=True)
        embed.add_field(name="Found an issue?",
                        value="__[Report Here!](https://github.com/Code-Cecilia/BotMan.py/issues)__", inline=True)
        embed.add_field(name='Invite Me!',
                        value=f"__[Link to invite](https://discord.com/api/oauth2/authorize?client_id"
                              f"=848529420716867625&permissions=261993005047&scope=applications.commands%20bot)__",
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

    @commands.command(name="speedtest", aliases=["speed", "spid"], description="Checks the internet speed of my host.")
    @commands.is_owner()
    async def speedtest(self, ctx, *args):
        """Use the `last` argument to view results of last test."""
        embed = discord.Embed(title="Speed Test", color=get_color.get_color(ctx.guild.me))
        if "last" not in [x.lower() for x in args]:  # show last test results if "last" argument is specified
            embed.description = "Testing download..."
            # edit the embed with progress
            message = await ctx.send(embed=embed)  # send the message
            self.speedtest.download()  # this is gonna take a while
            embed.description = "Testing Upload..."  # change the description
            await message.edit(embed=embed)  # edit the embed
            self.speedtest.upload()  # this is also going to take a while
            result_dict = self.speedtest.results.dict()
            self.last_speedtest_dict = result_dict
            # setting the result dict to be used again if the "last" argument is used
            await message.delete()  # delete the progress message
        else:
            result_dict = self.last_speedtest_dict
            if result_dict == {}:  # if no speed tests were conducted.
                return await ctx.send("No speed tests were conducted since I woke up.")
            embed.title = "Last Test Result"

        download = round((result_dict.get("download") / 1000000), 2)
        upload = round((result_dict.get("upload") / 1000000), 2)
        ping = round(result_dict.get("ping"), 2)
        server_region, server_name = result_dict.get("server").get("name"), result_dict.get("server").get("sponsor")
        embed.description = f"Region: **{server_region}** | Server: **{server_name}**"
        embed.add_field(name="Ping", value=f"{ping}ms", inline=True)
        embed.add_field(name="Download", value=f"{download} Mbps", inline=True)
        embed.add_field(name="Upload", value=f"{upload} Mbps", inline=True)
        sent, recieved = int(result_dict.get("bytes_sent")) / 1000000, int(result_dict.get("bytes_received")) / 1000000
        embed.set_footer(text=f"Sent: {int(sent)}MB | Received:  {int(recieved)}MB")

        await ctx.send(embed=embed)  # send embed with results

    @commands.command(name="hostinfo", description="Returns information about my host.")
    async def hostinfo(self, ctx):
        system = platform.uname()
        cpu_usage = psutil.cpu_percent()
        memstats = psutil.virtual_memory()
        memUsedGB = "{0:.1f}".format(((memstats.used / 1024) / 1024) / 1024)  # Thanks CorpNewt
        memTotalGB = "{0:.1f}".format(((memstats.total / 1024) / 1024) / 1024)
        processor = str(system.processor) if str(system.processor) != "" else "N/A"
        embed = discord.Embed(title=f"Host Name: {system.node}",
                              description=f"Platform: {system.system} | Version: {system.version}",
                              color=get_color.get_color(ctx.guild.me))
        embed.add_field(name="Release", value=system.release, inline=True)
        embed.add_field(name="Machine Type", value=system.machine, inline=True)
        embed.add_field(name="Threads", value=str(os.cpu_count()), inline=True)
        embed.add_field(name="CPU", value=processor, inline=False)
        embed.add_field(name="CPU Frequency", value=f"{int(list(psutil.cpu_freq())[0])} MHz", inline=True)
        embed.add_field(name="CPU Usage", value=f"{cpu_usage}%", inline=True)
        embed.add_field(name="RAM Usage", value=f"{memUsedGB} GB of {memTotalGB} GB ({memstats.percent}%)", inline=True)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(BotInfo(bot))
