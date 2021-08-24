import asyncio
import json
import os
import random

import discord.errors
from discord.ext import commands

reactions_random = ['👋', '♥', '⚡']


class Errors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if f"<@{self.bot.user.id}>" in str(message.content) or f"<@!{self.bot.user.id}>" in str(message.content):
            reaction = random.choice(reactions_random).strip()
            await message.add_reaction(reaction)

        if message.content not in [f'<@{self.bot.user.id}>', f'<@!{self.bot.user.id}>']:
            return

        with open('./storage/prefixes.json', 'r') as f:
            prefixes = json.load(f)
            prefix_server = prefixes.get(str(message.guild.id))

            if prefix_server is None:
                prefix_server = "bm-"

            pre = prefix_server

            await message.channel.send(f'Hello! I am {self.bot.user.name},\n'
                                       f'The prefix for this server is : `{pre}`, '
                                       f'and my help command can be accessed using `{pre}help`.')

    @commands.Cog.listener()  # error handling Cog, thanks @YuiiiPTChan
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            error = error.original
        if isinstance(error, commands.CommandNotFound):
            pass
        elif isinstance(error, discord.errors.Forbidden):
            await ctx.send("I do not have enough permissions to perform this action.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.message.add_reaction("‼️".strip())
            await ctx.send("An argument is missing or invalid. Check the help command for the correct usage..")
        elif isinstance(error, commands.BadArgument):
            await ctx.message.add_reaction("‼️".strip())
            await ctx.send("A bad argument has been passed, please check the context and the needed arguments.")
        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.message.add_reaction("‼️".strip())
            await ctx.send("This command cannot be used in private messages. Please use this command in a server.")
        elif isinstance(error, commands.CheckFailure):
            await ctx.message.add_reaction("‼️".strip())
            await ctx.send("You lack the necessary permissions to use this command.")
        elif isinstance(error, asyncio.TimeoutError):
            pass
        else:
            raise error

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        owner = guild.owner
        try:
            await owner.send(f"Hello, it seems I have been removed from {guild.name}.\n"
                             f"Your server's config files will be deleted, "
                             f"along with the mute files, and the custom prefix.\n"
                             f"Thank you for having me in your server for this long.\n"
                             f"Until next time!")
        except:
            pass
        if os.path.exists(f'configs/guild{guild.id}.json'):
            os.remove(f'./configs/guild{guild.id}.json')

        if os.path.exists(f'./storage/mute_files/guild{guild.id}.json'):
            os.remove(f'./storage/mute_files/guild{guild.id}.json')

        with open('./storage/prefixes.json', 'r') as prefixFile:
            data = json.load(prefixFile)
        if str(guild.id) in data.keys():
            data.pop(str(guild.id))

        with open('./storage/prefixes.json', 'w') as prefixFile:
            json.dump(data, prefixFile)


def setup(bot):
    bot.add_cog(Errors(bot))
