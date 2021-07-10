import discord
from discord.ext import commands
from discord.utils import get
import json

with open('config.json', 'r') as detailsFile:
    details_data = json.load(detailsFile)
    prefix_list = details_data['prefix_list']
    main_prefix = details_data['main_prefix']
    token = details_data['token']
    status_link = details_data['status_link']
    bot_bio = details_data['bio']


class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        owner = guild.owner
        await owner.send(f"Hello, I am {self.bot.user.name}! I was invited to {guild.name} just now."
                         f"I wanted to inform you that my prefix is `{main_prefix}`."
                         f"My help command can be accessed through `{main_prefix}help`."
                         f"G'day!")
        with open(f'configs/guild{guild.id}.json', 'a+') as createFile:
            json.dump({}, createFile)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        with open(f'./configs/guild{member.guild.id}.json', 'r') as detailsFile:
            data = json.load(detailsFile)
            welcome_channel_id = dict(data).get('welcome_channel')
            member_role_id = data.get('member_role')
        welcome_channel = self.bot.get_channel(id=int(welcome_channel_id))
        await welcome_channel.send(f'{member.mention} has joined **{member.guild.name}**! Say hi!')
        if not member.bot:
            await member.add_roles(get(member.guild.roles, id=int(member_role_id)))  # add the member role
        else:
            await welcome_channel.send('Oh, it\'s a bot')  # doesnt add the member role

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        with open(f'./configs/guild{member.guild.id}.json', 'r') as detailsFile:
            data = json.load(detailsFile)
            welcome_channel_id = dict(data).get('welcome_channel')
        welcome_channel = self.bot.get_channel(id=int(welcome_channel_id))
        await welcome_channel.send(f'{member.mention} has left **{member.guild.name}**. Until Next time!')
        if member.bot:
            await welcome_channel.send('It\'s a bot. Oh, well...')


def setup(bot):
    bot.add_cog(Welcome(bot))
