import asyncio
import random

import discord
from discord.ext import commands

from assets import random_assets as rand_ass
from assets import refine_text


class Funzies(commands.Cog, description='Fun commands for everyone to try out'):
    def __init__(self, bot):
        self.bot = bot
        self.hello_last = None
        self.last_lenny = None

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

    @commands.command(name='editmagic', aliases=['edit', 'messagemagic'],
                      description="Try it. I\'m not gonna spoil anything for you.")
    async def edit_fun(self, ctx):
        message = await ctx.send('Wanna see something cool?')
        await asyncio.sleep(1)
        await message.edit(content='Look, I \u202b this message \u202B')

    @commands.command(name='empty', aliases=['emptymessage', 'emptywtf'], description='Try it. That\'s all.')
    async def empty_message(self, ctx):
        await ctx.send("\uFEFF")

    @commands.command(name='choose', aliases=['choice'], description='Chooses an option from a list of choices.\n'
                                                                     'For multi-word options, '
                                                                     'enclose in "double quotes"')
    async def choose(self, ctx, *options):
        result = random.choice(options)
        result = refine_text.remove_mentions(result)
        await ctx.send(result)

    @commands.command(name='whatdidtheysay', aliases=['whatdidhesay', 'whatdidshesay', 'whatdidisay', 'whatdidyousay'],
                      description='Sends the whole message content of the message link passed as argument.\n'
                                 f'usage: `bm-whatdidtheysay https://discord.com/channels/....`')
    async def send_content(self, ctx, *, link_to_message):
        link_to_message = link_to_message.split('/')
        server_id = int(link_to_message[-3])
        channel_id = int(link_to_message[-2])
        msg_id = int(link_to_message[-1])

        server = self.bot.get_guild(server_id)
        try:
            channel = server.get_channel(int(channel_id))
        except AttributeError:
            return await ctx.send("Could not find a message from that link! "
                                  "Maybe I am not in the server the message is from.")
        try:
            message = await channel.fetch_message(int(msg_id))
        except:
            return await ctx.send(f"Could not find message in {channel.mention}!")
        content = message.content
        author = message.author
        created_at = message.created_at
        color = author.color
        if str(color) == '#000000':
            color = discord.Color.random()
        embed = discord.Embed(title=f"{author.display_name} sent in #{channel.name}",
                              timestamp=created_at, color=color)
        embed.add_field(name="Message", value=f"```\n{content}\n```", inline=False)
        embed.set_footer(text=f"Server: {server.name} | Channel: {channel.name}")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Funzies(bot))
