import json

from discord.ext import commands
import discord

import os

with open('config.json') as configFile:
    configs = json.load(configFile)
    prefix = configs.get('prefix_list')[0]


class Setup(commands.Cog, description='Used to set up the bot for welcome messages, mute/unmute etc.'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='setup', description='Used to set the bot up, for welcome messages, mute roles, etc.\n'
                                                'Recommended to set the bot up as early as possible when it joins a '
                                                'server.')
    @commands.guild_only()
    async def setup_welcome(self, ctx):
        embed = discord.Embed(title='You can setup preferences for your server with these commands.',
                              timestamp=ctx.message.created_at,
                              color=discord.Color.random())

        embed.add_field(name='Set channel for welcome messages',
                        value=f'`{prefix}setwelcomechannel [channel]`\nExample: `{prefix}setwelcomechannel #welcome`\n'
                              f'__**What you\'d see:**__\n'
                              f'{ctx.author.mention} has joined **{ctx.guild.name}**! Say hi!\n'
                              f'{ctx.author.mention} has left **{ctx.guild.name}**. Until Next time!',
                        inline=False)

        embed.add_field(name='Set default reason when kicking/banning members',
                        value=f'`{prefix}setkickreason [reason]`\nExample: `{prefix}setkickreason Being a jerk`\n'
                              f'__**What the kicked member would see**__:\n'
                              f'You have been kicked from **{ctx.guild.name}** for **Being a jerk**.',
                        inline=False)

        embed.add_field(name='Set the mute role for this server',
                        value=f'`{prefix}setmuterole [role]`\nExample: `{prefix}setmuterole muted` '
                              f'(muted must be an actual role).\n'
                              f'You can create a mute role by `{prefix}createmuterole [role name]`',
                        inline=False)

        embed.add_field(name='Set the default Member role for this server',
                        value=f'`{prefix}setmemberrole [role]`\nExample: `{prefix}setmemberrole Member`'
                              f' (Member must be an actual role).\n'
                              f'If you want to turn off AutoRole, make a role, assign the member role to that role, and delete the role',
                        inline=False)

        embed.add_field(name='Set the default channel for BotChat.',
                        value=f'`{prefix}setbotchatchannel [channel]`\nExample: `{prefix}setbotchatchannel #botchat`'
                              f' (`channel` must be an actual channel).\n'
                              f'If you want to turn off botchat, make a channel, assign botchat to that channel, and delete the channel.',
                        inline=False)

        embed.add_field(name='Set a custom prefix for this server.',
                        value=f'`{prefix}setprefix [prefix]`',
                        inline=False)

        embed.set_footer(text=f'Command requested by {ctx.author.name}')
        await ctx.send(embed=embed)

    @commands.command(name='setwelcomechannel', description="Used to set the channel welcome messages arrive. "
                                                            "See description of the `setup` command for more info.")
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def set_welcome_channel(self, ctx, channel: discord.TextChannel):
        channel_id = channel.id
        if not os.path.exists(f'./configs/guild{ctx.guild.id}.json'):
            with open(f'./configs/guild{ctx.guild.id}.json', 'w') as jsonFile:
                json.dump({}, jsonFile, indent=4)

        with open(f'./configs/guild{ctx.guild.id}.json', 'r') as jsonFile:
            data = json.load(jsonFile)

        data['welcome_channel'] = channel_id

        with open(f'./configs/guild{ctx.guild.id}.json', 'w') as jsonFile:
            json.dump(data, jsonFile, indent=3)

        await ctx.send(f'Welcome channel set to {channel.mention} successfully.')

    @commands.command(name='setkickreason', description='Used to set the default kick/ban reason '
                                                        'in a case where no reason is given.\n'
                                                        'Check the description of the `setup` command '
                                                        'for more information.')
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def set_kick_reason(self, ctx, *, reason):
        if not os.path.exists(f'./configs/guild{ctx.guild.id}.json'):
            with open(f'./configs/guild{ctx.guild.id}.json', 'w') as jsonFile:
                json.dump({}, jsonFile, indent=4)

        with open(f'./configs/guild{ctx.guild.id}.json', 'r') as jsonFile:
            data = json.load(jsonFile)

        data['default_kick_ban_reason'] = str(reason)

        with open(f'./configs/guild{ctx.guild.id}.json', 'w') as jsonFile:
            json.dump(data, jsonFile, indent=4)

        await ctx.send(f'Default kick/ban reason set to **{reason}** successfully.')

    @commands.command(name='setmemberrole', description='Used to set the role which is given to every member upon '
                                                        'joining. '
                                                        'Check description of `setup` command for more info.')
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def set_member_role(self, ctx, role: discord.Role):
        if not os.path.exists(f'./configs/guild{ctx.guild.id}.json'):
            with open(f'./configs/guild{ctx.guild.id}.json', 'w') as jsonFile:
                json.dump({}, jsonFile, indent=4)

        with open(f'./configs/guild{ctx.guild.id}.json', 'r') as jsonFile:
            data = json.load(jsonFile)

        data['member_role'] = role.id

        with open(f'./configs/guild{ctx.guild.id}.json', 'w') as jsonFile:
            json.dump(data, jsonFile, indent=3)

        await ctx.send(f'Member role set to **{role.name}** successfully.')

    @commands.command(name='setmuterole', description='Sets the role assigned to muted people. '
                                                      'Use `createmuterole` for creating a muted role and '
                                                      'automatically setting permissions to every channel.')
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def set_mute_role(self, ctx, role: discord.Role):
        if not os.path.exists(f'./configs/guild{ctx.guild.id}.json'):
            with open(f'./configs/guild{ctx.guild.id}.json', 'w') as jsonFile:
                json.dump({}, jsonFile, indent=4)

        with open(f'./configs/guild{ctx.guild.id}.json', 'r') as jsonFile:
            data = json.load(jsonFile)

        data['mute_role'] = role.id

        with open(f'./configs/guild{ctx.guild.id}.json', 'w') as jsonFile:
            json.dump(data, jsonFile, indent=4)

        await ctx.send(f'Mute role set to **{role.name}** successfully.')

    @commands.command(name='createmuterole', description='Creates a mute role, and sets messaging permissions to '
                                                         'every channel.\n '
                                                         'the `rolename` argument is optional. (Defaults to "Muted")')
    @commands.has_permissions(manage_roles=True)
    @commands.guild_only()
    async def create_mute_role(self, ctx, rolename=None):
        if rolename is None:
            rolename = 'Muted'
        guild = ctx.guild
        mutedRole = await guild.create_role(name=rolename)  # creating the role
        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False, use_slash_commands=False)
            # setting permissions for each channel
        await ctx.send(f'Created role **{mutedRole}** and set permissions accordingly.')
        await Setup.set_mute_role(self, ctx, mutedRole)

    @commands.command(name='changeprefix', aliases=['setprefix'], description='Sets the server-specific prefix')
    @commands.has_permissions(administrator=True)
    async def change_prefix_func(self, ctx, prefix):
        with open('./storage/prefixes.json', 'r') as f:
            data = json.load(f)

        data[str(ctx.guild.id)] = prefix

        with open('./storage/prefixes.json', 'w') as f:
            json.dump(data, f, indent=4)
        await ctx.send(f'The prefix for this server has changed to {prefix}')


def setup(bot):
    bot.add_cog(Setup(bot))
