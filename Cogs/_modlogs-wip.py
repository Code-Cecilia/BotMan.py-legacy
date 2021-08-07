import json

import discord
from discord.ext import commands

from assets import get_color


class Modlogs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open("./storage/modlogs_channels.json", "r") as modlogsFile:
            self.modlogsFile = json.load(modlogsFile)

    @commands.command(name="setmodlogschannel", aliases=["modlogschannel", "setlogschannel", "setmodlogchannel"],
                      description="Sets the channel in which modlogs are sent.")
    async def set_modlogs_channel(self, ctx, channel: discord.TextChannel):
        channel_id = channel.id
        self.modlogsFile[str(ctx.guild.id)] = int(channel_id)
        with open("./storage/modlogs_channels.json", "w") as modlogsFile:
            json.dump(self.modlogsFile, modlogsFile, indent=4)
        await ctx.send(f"Modlogs channel set as {channel.mention}")

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if self.modlogsFile.get(str(before.guild.id)) is None:
            return

        embed = discord.Embed(title=f"Message edited in {before.channel.name}",
                              color=get_color.get_color(before.author), timestamp=after.created_at)
        embed.add_field(name="Before", value=before.content, inline=False)
        embed.add_field(name="After", value=after.content, inline=False)
        embed.set_footer(text=f"Author  •  {before.author}  |  Edited", icon_url=before.author.avatar_url)
        # the edited timestamp would come in the right, so we dont need to specify it in the footer

        message_channel = self.bot.get_channel(id=int(self.modlogsFile.get(str(before.guild.id))))
        await message_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if self.modlogsFile.get(str(message.guild.id)) is None:
            return

        embed = discord.Embed(title=f"Message deleted in {message.channel.name}",
                              color=get_color.get_color(message.author), timestamp=message.created_at)
        embed.add_field(name="Content", value=message.content, inline=False)
        embed.set_footer(text=f"Author  •  {message.author}  |  Created", icon_url=message.author.avatar_url)
        # the edited timestamp would come in the right, so we dont need to specify it in the footer

        message_channel = self.bot.get_channel(id=int(self.modlogsFile.get(str(message.guild.id))))

        await message_channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Modlogs(bot))
