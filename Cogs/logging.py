import datetime
import json
import os

import discord
from discord.errors import HTTPException
from discord.ext import commands

from assets import get_color


class Modlogs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open("./storage/modlogs_channels.json", "r") as modlogsFile:
            self.modlogsFile = json.load(modlogsFile)

    @commands.command(name="messagelogschannel",
                      aliases=["seteditedlogschannel", "setdeletedlogschannel", "setlogschannel", "setlogchannel"],
                      description="Sets the channel in which edited/deleted message logs are sent.")
    async def set_modlogs_channel(self, ctx, channel: discord.TextChannel):
        channel_id = channel.id
        self.modlogsFile[str(ctx.guild.id)] = int(channel_id)
        with open("./storage/modlogs_channels.json", "w") as modlogsFile:
            json.dump(self.modlogsFile, modlogsFile, indent=4)
        await ctx.send(f"Logs channel set as {channel.mention} succesfully. "
                       f"Edited/Deleted mesages, and profile changes will be shown in this channel.")

    # message edit event
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if self.modlogsFile.get(str(before.guild.id)) is None:
            return
        message_link = f"https://discord.com/channels/{before.guild.id}/{before.channel.id}/{before.id}"
        embed = discord.Embed(title=f"Message edited in {before.channel.name}",
                              color=get_color.get_color(before.author), timestamp=after.created_at)
        embed.add_field(name="Before", value=before.content, inline=False)
        embed.add_field(name="After", value=after.content, inline=False)
        embed.add_field(name="Link", value=f"__[Message]({message_link})__", inline=False)
        embed.set_footer(text=f"Author  •  {before.author}  |  Edited")
        embed.set_thumbnail(url=before.author.avatar_url)
        # the edited timestamp would come in the right, so we dont need to specify it in the footer
        message_channel = self.bot.get_channel(id=int(self.modlogsFile.get(str(before.guild.id))))
        if message_channel is None:
            return
        await message_channel.send(embed=embed)

    # message delete event
    @commands.Cog.listener()
    async def on_message_delete(self, message):

        embed = discord.Embed(title=f"Message deleted in {message.channel.name}",
                              color=get_color.get_color(message.author), timestamp=message.created_at)
        embed.add_field(name="Content", value=message.content, inline=False)
        embed.set_footer(text=f"Author  •  {message.author}  |  Created")
        embed.set_thumbnail(url=message.author.avatar_url)
        # the edited timestamp would come in the right, so we dont need to specify it in the footer

        message_channel = self.bot.get_channel(id=int(self.modlogsFile.get(str(message.guild.id))))
        if message_channel is None:
            return
        try:
            await message_channel.send(embed=embed)
        except HTTPException:
            pass

    # bulk delete event
    @commands.Cog.listener()
    async def on_bulk_message_delete(self, messages):
        if self.modlogsFile.get(str(messages[0].guild.id)) is None:
            return
        message_channel = self.bot.get_channel(id=int(self.modlogsFile.get(str(messages[0].guild.id))))
        if message_channel is None:
            return
        with open(f"./storage/tempText/{messages[0].guild.id}.txt", "w") as temp_textfile:
            for x in messages:
                line1 = f"From: {x.author} | in: {x.channel.name} | Created at: {x.created_at}\n"
                temp_textfile.write(line1)
                temp_textfile.write(f"{x.content}\n\n")

        file = discord.File(f"./storage/tempText/{messages[0].guild.id}.txt")
        await message_channel.send(file=file, content=f"{len(messages)} messages deleted. "
                                                      f"Sending information as text file.")
        os.remove(f"./storage/tempText/{messages[0].guild.id}.txt")

    # ban event
    @commands.Cog.listener()
    async def on_member_ban(self, guild, member: discord.Member):
        message_channel_id = self.modlogsFile.get(str(guild.id))
        if message_channel_id is None:
            return
        message_channel = self.bot.get_channel(id=int(message_channel_id))
        if message_channel is None:
            return
        embed = discord.Embed(title=f"{member} has been banned from {guild.name}", description=f"ID: {member.id}",
                              timestamp=member.created_at)
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text="Account created at")
        await message_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        message_channel_id = self.modlogsFile.get(str(before.guild.id))
        if message_channel_id is None:
            return
        message_channel = self.bot.get_channel(id=int(message_channel_id))
        if message_channel is None:
            return
        embed = discord.Embed(title=f"{before}'s profile has been updated", description=f"ID: {before.id}",
                              color=get_color.get_color(after), timestamp=before.created_at)

        if not before.name == after.name:
            embed.add_field(name="Username", value=f"{before.name} --> {after.name}", inline=False)
        if not before.discriminator == after.discriminator:
            embed.add_field(name="Discriminator", value=f"{before.discriminator} --> {after.discriminator}", inline=False)
        if not before.avatar_url == after.avatar_url:
            embed.add_field(name="Avatar", value=f"__[Before]({before.avatar_url})__ --> __[After]({after.avatar_url})__",
                            inline=False)
        if not before.color == after.color:
            embed.add_field(name="Color", value=f"{before.color} --> {after.color}", inline=False)
        if not before.nick == after.nick:
            embed.add_field(name="Nickname", value=f"{before.nick} --> {after.nick}", inline=False)
        if not before.roles == after.roles:
            before_roles_str, after_roles_str = "", ""
            for x in before.roles:
                before_roles_str += f"{x.mention} "
            for x in after.roles:
                after_roles_str += f"{x.mention} "
            embed.add_field(name="Before", value=before_roles_str, inline=False)
            embed.add_field(name="After", value=after_roles_str, inline=False)
        embed.set_thumbnail(url=after.avatar_url)
        embed.set_footer(text="Account created at")
        await message_channel.send(embed=embed)

    # unban event
    @commands.Cog.listener()
    async def on_member_unban(self, guild, member: discord.Member):
        message_channel_id = self.modlogsFile.get(str(guild.id))
        if message_channel_id is None:
            return
        message_channel = self.bot.get_channel(id=int(message_channel_id))
        if message_channel is None:
            return
        embed = discord.Embed(title=f"{member} has been unbanned", description=f"ID: {member.id}",
                              color=get_color.get_color(discord.Color.random()),
                              timestamp=member.created_at)
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text="Account created at")
        await message_channel.send(embed=embed)

    # join event
    @commands.Cog.listener()
    async def on_member_join(self, guild, member: discord.Member):
        message_channel_id = self.modlogsFile.get(str(guild.id))
        if message_channel_id is None:
            return
        message_channel = self.bot.get_channel(id=int(message_channel_id))
        if message_channel is None:
            return
        embed = discord.Embed(title=f"Member {member} joined the the server.", color=member.color,
                              timestamp=datetime.datetime.utcnow(),
                              description=f"**Their account was created at:** {member.created_at}")
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text="Join time")
        await message_channel.send(embed=embed)

    # leave event
    @commands.Cog.listener()
    async def on_member_remove(self, guild, member: discord.Member):
        message_channel_id = self.modlogsFile.get(str(guild.id))
        if message_channel_id is None:
            return
        message_channel = self.bot.get_channel(id=int(message_channel_id))
        if message_channel is None:
            return
        roles = [role for role in member.roles]
        embed = discord.Embed(title=f"Member {member} left from the server.", color=member.color,
                              timestamp=datetime.datetime.utcnow(),
                              description=f"**Their account was created at:** {member.created_at}")
        embed.add_field(name="Their roles:", value=" ".join(
            [role.mention for role in roles]))
        embed.set_footer(text=f"Left at")
        embed.set_thumbnail(url=member.avatar_url)
        await message_channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Modlogs(bot))
