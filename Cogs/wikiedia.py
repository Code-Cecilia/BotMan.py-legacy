import discord
import requests
from discord.ext import commands

from assets import wiki_assets, get_color


class Wikipedia(commands.Cog, description="WIP Wikipedia Cog"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="wikisearch", description="Gives search results for a query.")
    async def wiki_search(self, ctx, *, search_term):
        async with ctx.typing():
            try:
                results = wiki_assets.wiki_search(search_term, limit=5, suggest=True)
            except requests.exceptions.ConnectionError:
                return await ctx.send("Error: Timed out. Please try again later.")
            except IndexError:
                return await ctx.send("No results were returned.")
            search_result = results[0]
            suggestion = results[1]
            embed = discord.Embed(title=f"Search Results for \"{search_term}\"", color=get_color.get_color(ctx.author))
            if suggestion:
                embed.description = f"**Suggested**: {suggestion}"
            embed.add_field(name="Results", value="\n".join([f"> {x}" for x in search_result]))
            embed.set_footer(text=f"Search requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)

    @commands.command(name="wiki", description="Wikipedia summary for a search term.")
    async def wiki_define(self, ctx, *, search_term):
        async with ctx.typing():
            try:
                name, summary, suggestion, url, images, links = wiki_assets.wiki_result(search_term)
            except requests.exceptions.ConnectionError:
                return await ctx.reply("Error: Timed out. Please try again later.")
            except IndexError:
                return await ctx.reply("No results were returned.")

            description = f"__[Page URL]({url})__"
            embed = discord.Embed(title=name, color=get_color.get_color(ctx.author), description=description)
            embed.add_field(name="Summary", value=summary if len(summary) < 1024 else summary[:1000] + "...")

            if links:
                embed.add_field(name="Links in this page", value="\n".join(links), inline=False)
            if suggestion:
                embed.add_field(name="Suggested", value=suggestion, inline=False)

            embed.set_thumbnail(url=images[0])
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Wikipedia(bot))
