import json
import os

import discord
from discord.ext import commands
from discord.utils import get

with open('config.json', 'r') as detailsFile:
    details_data = json.load(detailsFile)
    prefix = details_data.get('prefix')


class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        try:
            embed = discord.Embed(title=f"Hello! I am {self.bot.user.name}!", colour=discord.Color.blue())
            embed.description = f"I am pleased to have been invited to {guild.name}, " \
                                f"and I wanted to let the members and administrators of this server " \
                                f"know a few things about me."
            embed.add_field(name="Basic Information", value="My prefix is `bm-`, "
                                                            "and a list of my commands is available in `bm-help`.",
                            inline=False)
            embed.add_field(name="Changing my prefix", value="Use `bm-changeprefix [new prefix]` "
                                                             "to change my prefix for this server.",
                            inline=False)
            embed.add_field(name="Setting up my preferences for this server",
                            value="You can set a channel for welcome messages, botchat, madlibs, etc. "
                                  "using their respective commands.\n"
                                  "You can set a mute-role using the `setmuterole` command, "
                                  "or I could make one for this server using the `createmuterole` command. "
                                  "I set the permissions for the role automatically.\n"
                                  "You can set the default reason to be used for kicking/banning members "
                                  "using the `setkickreason` command.\n"
                                  "You can set a role to be assigned to new members "
                                  "using the `setmemberrole` command.\n",
                            inline=False)
            embed.set_thumbnail(url=self.bot.user.avatar_url)
            embed.set_footer(text="Have fun!")
            await guild.system_channel.send(embed=embed)
            embed.description = f"I am pleased to have been invited to {guild.name}, " \
                                f"and I wanted to let you, the owner of the server, " \
                                f"know a few things about me."
            await guild.owner.send(embed=embed)
        except:
            pass

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        owner = guild.owner
        try:
            await owner.send(f"Hello, it seems I have been removed from {guild.name}.\n"
                             f"Your server's config files will be deleted, "
                             f"along with the mute files, and the custom prefix.\n"
                             f"Thank you for having me in your server for this long.\n"
                             f"Until next time!")
        except:
            pass
        if os.path.exists(f'configs/guild{guild.id}.json'):
            os.remove(f'./configs/guild{guild.id}.json')

        if os.path.exists(f'./storage/mute_files/guild{guild.id}.json'):
            os.remove(f'./storage/mute_files/guild{guild.id}.json')

        with open('./storage/prefixes.json', 'r') as prefixFile:
            data = json.load(prefixFile)
        if str(guild.id) in data.keys():
            data.pop(str(guild.id))

        with open('./storage/prefixes.json', 'w') as prefixFile:
            json.dump(data, prefixFile)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if not os.path.exists(f'./configs/guild{member.guild.id}.json'):
            return
        with open(f'./configs/guild{member.guild.id}.json', 'r') as jsonFile:
            data = json.load(jsonFile)
            welcome_channel_id = dict(data).get('welcome_channel')
            if welcome_channel_id is None:
                return
            member_role_id = data.get('member_role')
        welcome_channel = self.bot.get_channel(id=int(welcome_channel_id))
        await welcome_channel.send(f'{member.mention} has joined **{member.guild.name}**! Say hi!')
        if not member.bot:
            # add the member role
            await member.add_roles(get(member.guild.roles, id=int(member_role_id)))
        else:
            # doesnt add the member role
            await welcome_channel.send('Oh, it\'s a bot')

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if member == self.bot.user:
            return
        if not os.path.exists(f'./configs/guild{member.guild.id}.json'):
            return
        with open(f'./configs/guild{member.guild.id}.json', 'r') as jsonFile:
            data = json.load(jsonFile)
            welcome_channel_id = dict(data).get('welcome_channel')
            if welcome_channel_id is None:
                return
        welcome_channel = self.bot.get_channel(id=int(welcome_channel_id))
        await welcome_channel.send(f'{member.mention} has left **{member.guild.name}**. Until Next time!')
        if member.bot:
            await welcome_channel.send("Oof, it's a bot!")


def setup(bot):
    bot.add_cog(Welcome(bot))
