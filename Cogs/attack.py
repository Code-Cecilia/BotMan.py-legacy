import discord
from discord.ext import commands

from assets import random_assets as rand_ass


class Attack(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='eat', description='Eat a member, install fear!')
    async def eat_func_actual(self, ctx, user: discord.Member):
        await ctx.send(rand_ass.eat_func(ctx.author, user, self.bot))

    @commands.command(name='drink', description='Beware, you might spill the user you\'re trying to drink.')
    async def drink_func(self, ctx, user: discord.Member):
        await ctx.send(rand_ass.drink_func(ctx.author, user, self.bot))

    @commands.command(name='hug', description='Try hugging yourself.')
    async def hug_func(self, ctx, user: discord.Member):
        await ctx.send(rand_ass.hug_func(ctx.author, user, self.bot))

    @commands.command(name='pet', description='Pets whoever you mention. Exceptions may exist.')
    async def pet_func(self, ctx, user: discord.Member):
        await ctx.send(rand_ass.pet_func(ctx.author, user, self.bot))


def setup(bot):
    bot.add_cog(Attack(bot))
