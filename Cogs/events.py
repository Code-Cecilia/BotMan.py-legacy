from discord.ext import commands


class Errors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()  # error handling Cog, thanks @YuiiiPTChan
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            pass
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
