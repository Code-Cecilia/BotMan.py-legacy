import os

import discord
import topgg
from discord.ext import commands


class TopGG(commands.Cog):

    def __init__(self, bot):
        self.topggtoken = os.environ["tokggtoken"]
        if self.topggtoken == "insert topgg webhook token here""insert topgg webhook token here":
            raise ValueError
        self.bot = bot
        self.bot.topggpy = topgg.DBLClient(self.bot, self.topggtoken, autopost=True)

    @commands.command(name="getbot", description="Gets information of a bot from top.gg\n"
                                                 "Use the bot's ID as argument.")
    async def get_bot_topgg(self, ctx, bot_id: int):
        try:
            info = await self.bot.topggpy.get_bot_info(bot_id=bot_id)
        except Exception as e:
            exception = e.__class__.__name__
            return await ctx.send(f"An exception occured : `{exception}`")
        user_id = info.get("id")
        user_name, user_discriminator = info.get("username"), info.get("discriminator")
        avatar_text = info.get("avatar")
        avatar_url = f"https://cdn.discordapp.com/avatars/{user_id}/{avatar_text}.png?size=1024"
        prefix = info.get("prefix")
        long_desc = info.get("longdesc")[:100] + "...   \n    ..." + info.get("longdesc")[-100:]
        invite = info.get("invite")
        topgg_link = f"https://top.gg/bot/{user_id}"

        embed = discord.Embed(title=info.get("username"), description=info.get("shortdesc"),
                              color=discord.Color.random())
        embed.set_thumbnail(url=avatar_url)
        embed.add_field(name="Bot User", value=f"{user_name}#{user_discriminator}", inline=True)
        embed.add_field(name="ID", value=info.get("id"), inline=True)
        embed.add_field(name="Server Count", value=info.get("server_count"), inline=True)
        embed.add_field(name="Prefix", value=prefix, inline=True)
        if invite is not None:
            embed.add_field(name="Invite Link", value=f"__[Link]({invite})__", inline=True)
        embed.add_field(name="Top.gg Link", value=f"__[Link]({topgg_link})__", inline=True)
        embed.add_field(name="Long Description", value=long_desc, inline=False)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(TopGG(bot))
