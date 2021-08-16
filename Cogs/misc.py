import asyncio
import re

import discord
from discord.ext import commands

from assets import time_calc, get_color


class Misc(commands.Cog, description="A category for miscellaneous stuff, of course."):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="remindme", aliases=["reminder", "timer"], description="Reminds you. Nothing else.")
    async def remind(self, ctx, time_duration: str, *, reason: commands.clean_content(fix_channel_mentions=True,
                                                                                      use_nicknames=True,
                                                                                      escape_markdown=False,
                                                                                      remove_markdown=False) = None):
        pattern = r"^[\d]+[s|m|h|d]{1}$"
        if not re.match(pattern, time_duration):
            return await ctx.send("Time period is of the wrong format.\n"
                                  "Example usage: `5s`, `10m`, `15h`, `2d`")
        if not reason:
            reason = "No reason given."
        time_seconds = time_calc.get_time(time_duration)
        pretty_time = time_calc.time_suffix(time_duration)
        await ctx.send(f"Alright, {ctx.author.display_name}. I will remind you in {pretty_time}.")
        await asyncio.sleep(time_seconds)
        description = f"You asked me to remind you {pretty_time} ago."
        embed = discord.Embed(title=f"{ctx.author.name}, here is your reminder", description=description,
                              color=get_color.get_color(ctx.author))
        embed.add_field(name="Reason", value=reason, inline=False)
        try:
            await ctx.author.send(embed=embed)
        except:
            await ctx.reply(content=f"{ctx.author.mention}, I could not send you a DM.", embed=embed)


def setup(bot):
    bot.add_cog(Misc(bot))
