import ast
import asyncio
import os

import discord
from discord.ext import commands
import aiohttp
import json
import re

from assets import list_funcs, time_operations

time_link = 'http://worldtimeapi.org/api/timezone/'


class Time(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='tzlist', aliases=['listtz', 'timezones'],
                      description='Gets the list of timezones available')
    async def get_tz_list(self, ctx):

        author = ctx.author

        async with aiohttp.ClientSession() as session:
            async with session.get(time_link) as response:
                response_list = (await response.content.read()).decode('utf-8')
                response_list = ast.literal_eval(response_list)

        chunk_list = list(list_funcs.chunks(response_list, 24))

        try:
            await author.send('Here\'s a list of timezones to choose from.')
        except:
            return await ctx.send('Could not send PM to you. '
                                  'Please check your settings to allow me to send messages to you.')
        for i in chunk_list:
            embed = discord.Embed(title="List of available Timezones", color=discord.Color.random())
            for j in i:
                embed.add_field(name=j, value="\uFEFF", inline=True)
            await author.send(embed=embed)
            await asyncio.sleep(1)

    @commands.command(name='timeinfo', description='Gets the timezone from __[this website](http://worldtimeapi.org)__')
    async def get_time_location(self, ctx, timezone: str.lower):
        timezone_link = f"{time_link}{timezone}"
        async with aiohttp.ClientSession() as session:
            async with session.get(timezone_link) as response:
                response_dict = (await response.content.read()).decode('utf-8')
                response_dict = json.loads(response_dict)
        if response_dict.get('error') == "unknown location":
            return await ctx.send('Unknown timezone name. Check the `tzlist` command for a list of timezones.\n'
                                  'PS: It\'s gonna be a long message, the `tzlist` command.')

        if response_dict.get('datetime') is None:
            return await ctx.send(f'Couldn\'t get time data for **{timezone}**. '
                                  f'Check the `tzlist` command for a list of valid timezones.\n'
                                  f'PS: It\'s gonna be a long message, the `tzlist` command.')

        time = response_dict.get('datetime')[11:19]
        timezone_embed = response_dict.get('timezone')
        date = response_dict.get('utc_datetime')[:10]
        offset = response_dict.get('utc_offset')
        day_of_week = response_dict.get('day_of_week')
        day_of_year = response_dict.get('day_of_year')

        embed = discord.Embed(title=f"Time information for {timezone_embed}", description=f"UTC Offset: {offset}",
                              color=discord.Color.random())
        embed.set_thumbnail(url='https://i.pinimg.com/originals/d0/73/35/d07335a92f67a04adc75b402004ad1d7.gif')
        embed.add_field(name='Time', value=time, inline=True)
        embed.add_field(name='Date', value=date, inline=True)
        embed.add_field(name='Day of week', value=day_of_week, inline=True)
        embed.add_field(name='Day of year', value=day_of_year, inline=True)

        await ctx.send(embed=embed)

    @commands.command(name='settz',
                      description='Sets the timezone. Check the `tzlist` command for a list of timezones.')
    async def set_timezone_from_api(self, ctx, timezone: str.lower):
        timezone_link = f"{time_link}{timezone}"
        async with aiohttp.ClientSession() as session:
            async with session.get(timezone_link) as response:
                response_dict = (await response.content.read()).decode('utf-8')
                response_dict = json.loads(response_dict)
        if response_dict.get('error') == "unknown location":
            return await ctx.send('Unknown timezone name. Check the `tzlist` command for a list of timezones.\n'
                                  'PS: It\'s gonna be a long message, the `tzlist` command.')

        if response_dict.get('datetime') is None:
            return await ctx.send(f'Couldn\'t get time data for **{timezone}**. '
                                  f'Check the `tzlist` command for a list of valid timezones.\n'
                                  f'PS: It\'s gonna be a long message, the `tzlist` command.')

        if not os.path.exists('./storage/time_tz.json'):  # create file if not exists
            with open('./storage/time_files/time_tz.json', 'w') as jsonFile:
                print('./storage/time_tz.json has been created')
                json.dump({}, jsonFile)

        with open('./storage/time_files/time_tz.json', 'r') as timeFile:
            time_data = json.load(timeFile)

        time_data[str(ctx.author.id)] = timezone

        with open('./storage/time_files/time_tz.json', 'w') as timeFile:
            json.dump(time_data, timeFile)

        await ctx.send(f'Timezone set as {timezone} successfully.')

    @commands.command(name='time', description='Gets the user\'s time if they have set the timezone or offset. '
                                               'Check the `settz` and `setoffset` command for more info.')
    async def get_time(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author

        with open('./storage/time_files/time_tz.json', 'r') as timeFile:
            data = json.load(timeFile)
            user_timezone = data.get(str(user.id))
        if user_timezone is None:
            return await ctx.send(f"{ctx.author.display_name} has not set their timezone. "
                                  f"They can do so with the `settz` command.")

        timezone_link = f"{time_link}{user_timezone}"
        async with aiohttp.ClientSession() as session:
            async with session.get(timezone_link) as response:
                response_dict = (await response.content.read()).decode('utf-8')
                response_dict = json.loads(response_dict)
        if response_dict.get('error') == "unknown location":
            return await ctx.send('Unknown timezone name. Check the `tzlist` command for a list of valid timezones.\n'
                                  'PS: It\'s gonna be a long message, the `tzlist` command.')

        if response_dict.get('datetime') is None:
            return await ctx.send(f'Couldn\'t get time data for **{user_timezone}**. '
                                  f'Check the `tzlist` command for a list of valid timezones.\n'
                                  f'PS: It\'s gonna be a long message, the `tzlist` command.')

        time = response_dict.get('datetime')[11:16]
        actual_timezone = response_dict.get('timezone')

        time_formatted = time_operations.format_time(time)

        final_string = f"`{actual_timezone}`, where **{user.display_name}** is, it's **{time_formatted}**."
        await ctx.send(final_string)


def setup(bot):
    bot.add_cog(Time(bot))
