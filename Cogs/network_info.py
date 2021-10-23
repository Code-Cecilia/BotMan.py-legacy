import aiohttp
import json
from discord.ext import commands
import discord


class Network(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.url = "https://myip.wtf/json"

    @commands.command(name="networkinfo", hidden=True)
    @commands.is_owner()
    async def network_thing(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get(url=self.url) as response:
                response = await response.content.read()
        response = json.loads(response)
        embed = discord.Embed(title=f"Network Info, lord {self.bot.get_user(self.bot.owner_id).name}",
                              color=discord.Color.orange())
        for k, v in response.items():
            embed.add_field(name=k, value=v, inline=False)

        await ctx.author.send(embed=embed)


def setup(bot):
    bot.add_cog(Network(bot))
