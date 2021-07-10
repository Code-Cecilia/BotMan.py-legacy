from discord.ext import commands
from assets import random_assets


class RandomEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='toss',
                      description='Tosses a coin and tells you the result. '
                                  'Totally unbiased, of course. Why would you think otherwise?')
    async def toss_command(self, ctx):
        await ctx.send(random_assets.coin_flip())

    @commands.command(name='roll', aliases=['dice'], description='Rolls a die, and tells you the result. '
                                                                 'Result varies from 1 to 6. '
                                                                 'Totally unbiased, just like the Toss command 👌')
    async def roll_command(self, ctx):
        await ctx.send(random_assets.roll_dice())

    @commands.command(name='ask', description='Gives an honest answer to any question you ask. '
                                              'Contrary to public conception, this is **not** random. Yeah, totally. /s')
    async def ask_qn(self, ctx, *, question=None):
        await ctx.send(random_assets.ask_qn(question))


def setup(bot):
    bot.add_cog(RandomEvents(bot))
