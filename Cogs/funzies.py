import discord
from discord.ext import commands
import random
import aiohttp
import os
import asyncio
import json

from assets import quotes
from assets import random_assets as rand_ass
from assets import random_reactions


class Funzies(commands.Cog, description='Fun commands for everyone to try out'):
    def __init__(self, bot):
        self.bot = bot
        self.hello_last = None
        self.last_lenny = None

    @commands.Cog.listener()
    async def on_message(self, message):
        if self.bot.user.mentioned_in(message):  # check for mentions, and react with a random emoji
            reaction = random.choice(random_reactions.reactions_random)
            await message.add_reaction(reaction)

            with open('./storage/prefixes.json', 'r') as f:
                prefixes = json.load(f)
                prefix_server = prefixes.get(str(message.guild.id))

                if prefix_server is None:
                    prefix_server = "bm-"

                pre = prefix_server

                await message.channel.send(f'The prefix for this server is : `{pre}`')

    @commands.command(name='eat', description='Eats the person, I guess')
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

    @commands.command(name='fart', description='Does this really need a description?')
    async def fart_func(self, ctx):
        await ctx.send(rand_ass.fart_reaction())

    @commands.command(name='art', description='You might think this uses a machine learning algorithm, '
                                              'but no.\nIt just gets a random image from '
                                              '__[this website](https://thisartworkdoesnotexist.com)__')
    async def art_command(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://thisartworkdoesnotexist.com/") as response:
                f = await response.content.read()
        if not os.path.exists('./storage/art.png'):
            with open('./storage/art.png', 'w') as imageFile:
                print('created file art.png inside the storage folder')  # create file if not present
        with open('./storage/art.png', 'wb') as fl:
            fl.write(f)  # f is already in binary, so don't need to decode
            fl = open('./storage/art.png', 'rb')
            pic = discord.File(fl)
        await ctx.send(file=pic)

    @commands.command()
    async def inspire(self, ctx):
        await ctx.send(await quotes.get_quote())

    @commands.command(name='hello', description='Says hello, and remembers nothing after that. I\'m kidding, '
                                                'it knows who last said hello to it.')
    async def hello(self, ctx, *, some_text=None):
        await ctx.send(f'Hello, {ctx.author.display_name}!')
        if some_text is not None:
            await ctx.send(f'I don\'t understand why you say "{some_text}". Doesn\'t make sense.')
        if self.hello_last == ctx.author.id:
            await ctx.send('This does feel familiar, though')

        self.hello_last = ctx.author.id  # saves the last user's id to be used again

    @commands.command(name='sendemoji', description='Sends the emoji, and that\'s it.\n'
                                                    'It can send animated emojis too!\n'
                                                    'Note: Only guild-only emojis are taken into account.')
    async def emoji_command(self, ctx, emoji_name):
        for x in ctx.guild.emojis:
            if emoji_name == x.name:
                return await ctx.send(str(x))
        await ctx.send(f'No guild-only emoji called **{emoji_name}** found.')

    @commands.command(name='selfdestruct', description='**DO NOT USE THIS COMMAND**')
    async def selfdestruct_command(self, ctx):
        msg_content = "███"
        message = await ctx.send(f"{msg_content}")
        for x in range(2):
            await asyncio.sleep(1)
            msg_content = msg_content[:-1]
            await message.edit(content=f'{msg_content}')
        await asyncio.sleep(1)
        await message.edit(content='**Kaboom!**')

    @commands.command(name='lenny', description='( ͡° ͜ʖ ͡°)')
    async def lenny(self, ctx):
        await ctx.send('( ͡° ͜ʖ ͡°)')
        self.last_lenny = ctx.author.id
        await ctx.message.delete()

    @commands.command(name='lastlenny', description='Last Lenny user is returned')
    async def lastlenny(self, ctx):
        last_user_id = self.last_lenny
        user = self.bot.get_user(last_user_id)
        if user is None:
            return await ctx.send('Nobody. Nobody used the `lenny` command since I got online')
        await ctx.send(f'{user.display_name} was the last `lenny` user')


def setup(bot):
    bot.add_cog(Funzies(bot))
