import asyncio
import json
import random
import re
import urllib.parse

import aiohttp
import discord
from discord.ext import commands

from assets import time_calc, get_color, random_assets


class Misc(commands.Cog, description="A category for miscellaneous stuff, of course."):

    def __init__(self, bot):
        self.bot = bot
        self.bored_api_link = "http://www.boredapi.com/api/activity/"
        self.spongebob_api_link = "https://api.devs-hub.xyz/spongebob-timecard?text="

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

    @commands.command(name="bored", aliases=["randomactivity"], description="Bored? Let's find you something to do!")
    async def get_activity(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get(url=self.bored_api_link) as response:
                response_json = (await response.content.read()).decode("utf-8")
        response_json = json.loads(response_json)
        activity = response_json.get("activity")
        type = response_json.get("type")
        participants = response_json.get("participants")
        price = response_json.get("price")
        accessibility = response_json.get("accessibility")
        embed = discord.Embed(title=f"Type: {type.title()}", description=activity,
                              color=get_color.get_color(ctx.author))
        embed.add_field(name="Participants", value=participants, inline=True)
        embed.add_field(name="Accessibility", value=accessibility, inline=True)
        embed.add_field(name="Price", value=price, inline=True)
        await ctx.send(embed=embed)

    @commands.command(name="spongebob", aliases=["timecard"], description="Returns an image, the spongebob style.")
    async def get_spongebob_timecard(self, ctx, *, text=None):
        async with ctx.typing():
            if text is None:
                text = random.choice(random_assets.spongebob_text_responses)
            encoded_text = urllib.parse.quote(text)
            image_url = f"{self.spongebob_api_link}{encoded_text}"
            async with aiohttp.ClientSession() as session:
                async with session.get(image_url) as response:
                    binary_data = await response.content.read()

            with open("./storage/spongebob.png", "wb") as writeFile:
                writeFile.write(binary_data)
            file = discord.File("./storage/spongebob.png", filename="timecard.png")

            embed = discord.Embed(title=f"{ctx.author.display_name}, here is your timecard!",
                                  color=get_color.get_color(ctx.author))
            embed.set_image(url="attachment://timecard.png")
            await ctx.reply(file=file, embed=embed)
            await asyncio.sleep(1)


def setup(bot):
    bot.add_cog(Misc(bot))
