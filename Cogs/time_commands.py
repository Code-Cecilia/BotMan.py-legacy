import ast
import asyncio
import json
import discord
from discord.ext import commands
import aiohttp
import os
import re

from assets import time_operations, time_custom, list_funcs

time_link = 'http://worldtimeapi.org/api/timezone/'


class Time(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='time', description='Gets the time from a location, or using the offset. '
                                               'Use the `settz` and `setoffset` commands for setting it up.')
    async def time_user(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author

        is_offset, is_tz = await time_operations.check_time(user)

        if not is_offset and not is_tz:
            return await ctx.send(f"{user.display_name} has not set their timezone. "
                                  f"They can do so with the `settz` or `setoffset` commands.")

        if is_tz:
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
                return await ctx.send(
                    'Unknown timezone name. Check the `tzlist` command for a list of valid timezones.\n'
                    'PS: It\'s gonna be a long message, the `tzlist` command.')

            if response_dict.get('datetime') is None:
                return await ctx.send(f'Couldn\'t get time data for **{user_timezone}**. '
                                      f'Check the `tzlist` command for a list of valid timezones.\n'
                                      f'PS: It\'s gonna be a long message, the `tzlist` command.')

            time = response_dict.get('datetime')[11:16]
            actual_timezone = response_dict.get('timezone')

            time_formatted = time_operations.format_time(time)

            final_string = f"`{actual_timezone}`, where **{user.display_name}** is, it's **{time_formatted}**."
            return await ctx.send(final_string)

        if is_offset:
            with open('./storage/time_files/time_offset.json', 'r') as timeFile:
                time_data = json.load(timeFile)

            user_offset = time_data.get(str(ctx.author.id))
            time_unformatted = time_custom.time_bm(user_offset)
            time_formatted = time_operations.format_time(time_unformatted)
            await ctx.send(f"UTC{user_offset}, where **{user.display_name}** is, it's **{time_formatted}**.")

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
                json.dump({}, jsonFile)

        with open('./storage/time_files/time_tz.json', 'r') as timeFile:
            time_data = json.load(timeFile)

        time_data[str(ctx.author.id)] = timezone

        with open('./storage/time_files/time_tz.json', 'w') as timeFile:
            json.dump(time_data, timeFile)

        await ctx.send(f'Timezone set as {timezone} successfully.')

        with open('./storage/time_files/time_offset.json', 'r') as timeFile:
            offset_data = json.load(timeFile)

        offset_data.pop(str(ctx.author.id))

        with open('./storage/time_files/time_offset.json', 'w') as timeFile:
            json.dump(offset_data, timeFile, indent=4)

        await ctx.send('Removed offset entry because you\'re using the location format now.')

    @commands.command(name='setoffset', description='Sets the user\'s time offset.\n'
                                                    'Format for offset: `-2:30` and `+2:30`\n'
                                                    '**Nerd note**: the regex for the offset is '
                                                    r'`^[+\-]+\d+:\d+$`')
    async def set_offset(self, ctx, offset):
        pattern = r'^[+\-]+\d+:\d+$'
        # matches the pattern, and if it fails, returns an error message
        if not re.match(pattern, offset):
            return await ctx.send('Improper offset format. Please read the help command for more info.')

        if not os.path.exists('./storage/time_files/time_offset.json'):  # create file if not exists
            with open('./storage/time_files/time_offset.json', 'w') as jsonFile:
                json.dump({}, jsonFile)

        with open('./storage/time_files/time_offset.json', 'r') as timeFile:
            time_data = json.load(timeFile)

        time_data[str(ctx.author.id)] = offset

        with open('./storage/time_files/time_offset.json', 'w') as timeFile:
            json.dump(time_data, timeFile)

        await ctx.send(f'Time offset set as {offset} successfully.')

        with open('./storage/time_files/time_tz.json', 'r') as timeFile:
            tz_data = json.load(timeFile)
        tz_data.pop(str(ctx.author.id))
        # delete the api tz entry
        with open('./storage/time_files/time_tz.json', 'w') as timeFile:
            json.dump(tz_data, timeFile, indent=4)

        await ctx.send("Removed the location entry because you\'re using the offset format now.")

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
            embed = discord.Embed(title="List of Available Timezones", color=discord.Color.random())
            for j in i:
                embed.add_field(name=j, value="\uFEFF", inline=True)
            await author.send(embed=embed)
            await asyncio.sleep(1)


def setup(bot):
    bot.add_cog(Time(bot))
