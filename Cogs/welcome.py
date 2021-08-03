import json
import os

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
        owner = guild.owner
        try:
            await owner.send(f"Hello, I am {self.bot.user.name}! I was invited to {guild.name} just now.\n"
                             f"I wanted to let you know that my prefix is `{prefix}`, and "
                             f"my help command can be accessed through `{prefix}help`.\n"
                             f"Allow me to invite you to the support server: https://discord.gg/9pYEXybAHH\n"
                             f"When you can, please leave a review in my top.gg page, "
                             f"it would really help me maker improve me: https://top.gg/bot/845225811152732179/\n"
                             f"Have a good day ahead!")
        except:
            pass
        if not os.path.exists(f'configs/guild{guild.id}.json'):
            with open(f'configs/guild{guild.id}.json', 'a+') as createFile:
                json.dump({}, createFile, indent=4)

        with open('./storage/prefixes.json', 'r') as f:
            prefixes = json.load(f)

        prefixes[str(guild.id)] = "bm-"

        with open('./storage/prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)

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

        with open('prefixes.json', 'r') as prefixFile:
            data = json.load(prefixFile)
        if str(guild.id) in data.keys():
            data.pop(str(guild.id))

        with open('prefixes.json', 'w') as prefixFile:
            json.dump(data, prefixFile)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        with open(f'./configs/guild{member.guild.id}.json', 'r') as jsonFile:
            data = json.load(jsonFile)
            welcome_channel_id = dict(data).get('welcome_channel')
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
        with open(f'./configs/guild{member.guild.id}.json', 'r') as jsonFile:
            data = json.load(jsonFile)
            welcome_channel_id = dict(data).get('welcome_channel')
        welcome_channel = self.bot.get_channel(id=int(welcome_channel_id))
        await welcome_channel.send(f'{member.mention} has left **{member.guild.name}**. Until Next time!')
        if member.bot:
            await welcome_channel.send("Oof, it's a bot!")


def setup(bot):
    bot.add_cog(Welcome(bot))
