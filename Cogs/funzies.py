import asyncio
import json
import os
import random

import discord
from discord.ext import commands

from assets import misc_checks
from assets import random_assets as rand_ass
from assets import refine_text


class Funzies(commands.Cog, description='Fun commands for everyone to try out'):
    def __init__(self, bot):
        self.bot = bot
        self.hello_last = None
        self.last_lenny = None

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
    @commands.guild_only()
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
    @commands.guild_only()
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
        embed.add_field(
            name="Message", value=f"```\n{content}\n```", inline=False)
        embed.set_footer(
            text=f"Server: {server.name} • Channel: {channel.name}")
        await ctx.send(embed=embed)

    @commands.command(name="cookie", aliases=["biscuit", "feed"], description="Feed a fellow member a cookie!")
    @commands.guild_only()
    async def cookie(self, ctx, *, user: discord.Member):

        if misc_checks.is_author(ctx, user):
            return await ctx.send(f"_{ctx.author.display_name}_, You give yourself a cookie. "
                                  f"This doesn't count towards my database. 🤦")

        if misc_checks.is_client(self.bot, user):
            return await ctx.send(f"_{ctx.author.display_name}_, Thanks for the cookie. "
                                  f"If you don't tell anyone, I won't.\n"
                                  f"Now _gently_ turn around and walk back like nothing happened. "
                                  f"We don't want people to become suspicious.")

        if not os.path.exists(f"./storage/cookie/{ctx.guild.id}.json"):
            with open(f"./storage/cookie/{ctx.guild.id}.json", "w") as cookieFile:
                json.dump({}, cookieFile)

        with open(f"./storage/cookie/{ctx.guild.id}.json", "r") as cookieFile:
            cookie_data = json.load(cookieFile)
            data_user = cookie_data.get(str(user.id))
            if data_user is None:
                cookie_data[str(user.id)] = 1
                no_of_cookies = 1
            else:
                data_user = int(data_user)
                cookie_data[str(user.id)] = data_user + 1
                no_of_cookies = data_user + 1

        with open(f"./storage/cookie/{ctx.guild.id}.json", "w") as cookieFile:
            json.dump(cookie_data, cookieFile)

            embed = discord.Embed(title=f"{user.display_name}, have a cookie!",
                                  description=f"Say thanks to {ctx.author.mention}!",
                                  color=discord.Color.random())
            embed.set_thumbnail(
                url="https://cdn.discordapp.com/attachments/612050519506026506/870332758348668998/cookie.png")
            embed.set_footer(
                text=f"You now have {no_of_cookies} cookies in this server!")
        await ctx.send(embed=embed)

    @commands.command(name="cookies", aliases=["howmanycookiesdoihave", "howmanycookies"],
                      description="Returns how many cookies the user has.")
    @commands.guild_only()
    async def no_of_cookies(self, ctx, *, user: discord.Member = None):
        if user is None:
            user = ctx.author

        if not os.path.exists(f"./storage/cookie/{ctx.guild.id}.json"):
            with open(f"./storage/cookie/{ctx.guild.id}.json", "w") as cookieFile:
                json.dump({}, cookieFile)

        with open(f"./storage/cookie/{ctx.guild.id}.json", "r") as cookieFile:
            cookie_data = json.load(cookieFile)
            data_user = cookie_data.get(str(user.id))

        if data_user is None and misc_checks.is_author(ctx, user):
            await ctx.send(f"_{user.display_name}_, you haven't gotten cookies from anyone yet. "
                           f"Don't be sad though, I'll give you one 🍪")
            cookie_data[str(user.id)] = 1
            with open(f"./storage/cookie/{ctx.guild.id}.json", "w") as cookieFile:
                json.dump(cookie_data, cookieFile)
            return
        if misc_checks.is_author(ctx, user):
            await ctx.send(f"_{user.display_name}_, you have {data_user} cookies in your collection in this server.")
            if random.choice([True, False, False, False]):
                cookie_data[str(user.id)] = int(data_user) + 1
                with open(f"./storage/cookie/{ctx.guild.id}.json", "w") as cookieFile:
                    json.dump(cookie_data, cookieFile)
                return await ctx.send("|| I've given you an extra cookie. Don't tell anyone... ||")
        if not misc_checks.is_author(ctx, user):
            if data_user is None:
                data_user = 0
            await ctx.send(f"_{user.display_name}_ has {data_user} cookies in their collection.")

    @commands.command(name="alien", aliases=["shuffle"], description="Wanna see how aliens communicate?")
    async def shuffle_chard(self, ctx, *, message: list):
        random.shuffle(message)
        final_str = "".join(message)
        await ctx.send(final_str)


def setup(bot):
    bot.add_cog(Funzies(bot))
