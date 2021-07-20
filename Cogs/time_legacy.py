import re

import discord
from discord.ext import commands
import os
import json

from assets import time_custom


class TimeLegacy(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='timeoffset', aliases=['legacytime', 'timelegacy'],
                      description='Gets the time of the user. if user does not have a timezone set, '
                                  'they can use an offset like "+2:30"')
    async def get_time(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author

        user_id = str(user.id)

        if not os.path.exists('./storage/time_files/time_offset.json'):  # create file if not exists
            with open('./storage/time_files/time_offset.json', 'w') as jsonFile:
                print('./storage/time_files/time_offset.json has been created')
                json.dump({}, jsonFile)

        with open('./storage/time_files/time_offset.json', 'r') as timeFile:
            time_data = json.load(timeFile)

        user_offset = time_data.get(user_id)

        if user_offset is None:
            return await ctx.send(
                f'_{user.display_name}_ has not set their offset. They can do so using the `setoffset` command.')

        """None of the following code is executed if user_offset is None"""

        final_time_string = time_custom.time_bm(user_offset)

        await ctx.send(final_time_string)

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
                print('./storage/time_files/time_offset.json has been created')
                json.dump({}, jsonFile)

        with open('./storage/time_files/time_offset.json', 'r') as timeFile:
            time_data = json.load(timeFile)

        time_data[str(ctx.author.id)] = offset

        with open('./storage/time_files/time_offset.json', 'w') as timeFile:
            json.dump(time_data, timeFile)

        await ctx.send(f'Time offset set as {offset} successfully.')


def setup(bot):
    bot.add_cog(TimeLegacy(bot))
