import json
import random

from discord.ext import commands

reactions_random = ['👋', '♥', '⚡']


class Errors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if f"<@{self.bot.id}>" in message or f"<@!<{self.bot.id}>" in message:
            reaction = random.choice(reactions_random)
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
        if isinstance(error, commands.CommandNotFound):
            await ctx.message.add_reaction("‼️")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.message.add_reaction("‼️")
            await ctx.send("An argument is missing or invalid. Check the help command for the correct usage..")
        elif isinstance(error, commands.BadArgument):
            await ctx.message.add_reaction("‼️")
            await ctx.send("A bad argument has been passed, please check the context and the needed arguments.")
        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.message.add_reaction("‼️")
            await ctx.send("This command cannot be used in private messages. Please use this command in a server.")
        elif isinstance(error, commands.CheckFailure):
            await ctx.message.add_reaction("‼️")
            await ctx.send("You lack the necessary permissions to use this command.")
        else:
            raise error


def setup(bot):
    bot.add_cog(Errors(bot))
