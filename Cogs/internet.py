import json
import os
import random
import urllib.parse

import aiohttp
import asyncpraw
import discord
from discord.ext import commands

from assets import UrbanDict
from assets import money_convert
from assets import quotes
from assets import tinyurl

with open('reddit_details.json', 'r') as jsonFile:
    data = json.load(jsonFile)
client_id = data.get('client_id')
client_secret = data.get('client_secret')
username = data.get('username')
password = data.get('password')

reddit = asyncpraw.Reddit(client_id=client_id, client_secret=client_secret, username=username, password=password,
                          user_agent="pythonpraw")


class WebSurf(commands.Cog, description='Fun commands using AsyncPraw, PRSAW, UrbanDict, MoneyExchangeAPI and more!\n'
                                        'Basically gets data from the internet.'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='nocontext', description='Returns a random post\'t title from r/NoContext')
    async def NoContext(self, ctx):
        subreddit = await reddit.subreddit("nocontext")
        x = subreddit.hot(limit=20)
        title_list = []
        async for y in x:
            title_list.append(str(y.title))
        choice = random.choice(title_list)
        embed = discord.Embed(title=choice, color=discord.Colour.random())
        await ctx.send(embed=embed)

    @commands.command(name='meme', description='Sends a random meme from r/memes, and '
                                               'if "all" is passed in as an argument, a few more subreddits are used.')
    async def get_meme(self, ctx, arg=None):
        if arg == "all":
            subreddit = await reddit.subreddit('memes')
        else:
            subreddit = await reddit.subreddit('memes+dankmemes+prequelmemes+otmemes+funny')
        sub_list = []
        x = subreddit.hot(limit=50)
        async for y in x:
            sub_list.append(y)
        final_choice = random.choice(sub_list)
        author = final_choice.author
        like_ratio = float(final_choice.upvote_ratio) * 100
        embed = discord.Embed(title=final_choice.title,
                              color=discord.Color.random())
        embed.set_image(url=final_choice.url)
        embed.set_footer(
            text=f"By u/{author} | {int(like_ratio)}% upvoted | Powered by Reddit")
        await ctx.send(embed=embed)

    @commands.command(name="funfact", aliases=['randomfact', 'fact'], description="Sends a random fact.")
    async def fact(self, ctx):
        url = f'https://uselessfacts.jsph.pl/random.json?language=en'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                r = await response.json()
                fact = r['text']
                embed = discord.Embed(title=f'Random Fact', colour=discord.Colour.random(),
                                      timestamp=ctx.message.created_at)
                embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/669973636156751897/734100544918126592"
                                        "/article-fact-or-opinion.jpg")
                embed.set_footer(text="Useless Facts")
                embed.add_field(name='***Fun Fact***',
                                value=fact, inline=False)
                await ctx.send(embed=embed)

    @commands.command(name='inspire', description='Sends a random quote.')
    async def inspire(self, ctx):
        await ctx.send(await quotes.get_quote())

    @commands.command(name='art', description='You might think this uses a machine learning algorithm, '
                                              'but no.\nIt just gets a random image from '
                                              '__[this website](https://thisartworkdoesnotexist.com)__')
    async def art_command(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://thisartworkdoesnotexist.com/") as response:
                f = await response.content.read()
        if not os.path.exists('./storage/art.png'):
            with open('./storage/art.png', 'w') as imageFile:
                # create file if not present
                print('created file art.png inside the storage folder')
        with open('./storage/art.png', 'wb') as fl:
            fl.write(f)  # f is already in binary, so don't need to decode
            fl = open('./storage/art.png', 'rb')
            pic = discord.File(fl)
        await ctx.send(file=pic)

    @commands.command(name='define', description='Pulls a description from Urban Dictionary of the term entered as '
                                                 'argument.\n '
                                                 'Take caution, as sometimes it can be a bit... too accurate.')
    async def define_from_urban(self, ctx, *, term):
        try:
            word, definition, likes, dislikes, example, author = await UrbanDict.define(term)
        except:
            await ctx.send(f'Could not load definition for **{term}**.')
            return
        embed = discord.Embed(
            title=word, description=definition, color=discord.Color.random())
        embed.add_field(name="Example", value=example, inline=False)
        embed.add_field(
            name='Likes', value=f"👍 {likes} | 👎 {dislikes}", inline=True)
        embed.set_footer(
            text=f'Powered by UrbanDictionary | Author - {author}')
        await ctx.send(embed=embed)

    @commands.command(name='convert', description='Converts an integer value from one currency to another.\n'
                                                  f'Usage example: `bm-convert 100 USD EUR`\n'
                                                  f'For currency codes, check '
                                                  f'__[here](https://www.iban.com/currency-codes)__')
    async def get_currency(self, ctx, value: float, from_currency: str.upper, to_currency: str.upper):
        async with ctx.typing():
            final_string = await money_convert.get_converted_currency(value, from_currency, to_currency)
            await ctx.send(final_string)

    @commands.command(name="google", aliases=["search"], description="Feeling too lazy to open a browser? Search here!")
    async def lmgtfy(self, ctx, *, search_term):
        encoded_term = urllib.parse.quote(search_term)
        lmgtfy_link = f"https://lmgtfy.app/?q={encoded_term}"
        tinyurl_link = await tinyurl.get_tinyurl(lmgtfy_link)
        await ctx.send(f"_{ctx.author.display_name}_, here is the google search you asked for.\n"
                       f"<{tinyurl_link}>")


def setup(bot):
    bot.add_cog(WebSurf(bot))
