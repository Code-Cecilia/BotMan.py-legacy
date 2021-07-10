import random
import discord
import asyncpraw
from discord.ext import commands
import json

with open('reddit_details.json', 'r') as jsonFile:
    data = json.load(jsonFile)
client_id = data.get('client_id')
client_secret = data.get('client_secret')
username = data.get('username')
password = data.get('password')


reddit = asyncpraw.Reddit(client_id=client_id, client_secret=client_secret, username=username, password=password,
                          user_agent="pythonpraw")


class Reddit(commands.Cog, description='Fun commands using __[PRAW](https://praw.readthedocs.io/en/stable/)__'):
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
        if arg is None:
            subreddit = await reddit.subreddit('memes')
        elif arg == 'all':
            subreddit = await reddit.subreddit('memes+dankmemes+prequelmemes+otmemes+funny')
        sub_list = []
        x = subreddit.hot(limit=50)
        async for y in x:
            sub_list.append(y)
        final_choice = random.choice(sub_list)
        author = final_choice.author
        like_ratio = float(final_choice.upvote_ratio) * 100
        embed = discord.Embed(title=final_choice.title, color=discord.Color.random())
        embed.set_image(url=final_choice.url)
        embed.set_footer(text=f"By u/{author} | {int(like_ratio)}% upvoted | Powered by Reddit")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Reddit(bot))
