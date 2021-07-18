import asyncio

import discord
from discord.ext import commands
import json
from discord.utils import get
import os

from assets import time_calc, misc_checks


class Moderation(commands.Cog, description="Moderation commands. I don\'t think this needs a description."):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='mute', description='Mutes the person mentioned. Time period is optional.')
    @commands.has_permissions(manage_roles=True)
    @commands.guild_only()
    async def mute_func(self, ctx, user: discord.Member, time_period=None):

        if misc_checks.is_author(ctx, user):
            return await ctx.send('You cannot mute yourself. Sorry lol')

        if misc_checks.is_client(self.bot, user):
            return await ctx.send('I can\'t mute myself, sorry.')

        if not os.path.exists(f'./configs/guild{ctx.guild.id}.json'):
            with open(f'./configs/guild{ctx.guild.id}.json', 'w') as createFile:
                json.dump({}, createFile, indent=4)
                print(f'Created file guild{ctx.guild.id}.json in configs...')

        with open(f'./configs/guild{ctx.guild.id}.json', 'r') as jsonFile:
            data = json.load(jsonFile)
        mute_role_id = data.get('mute_role')

        if mute_role_id is None:
            return await ctx.send('It seems you have not set the mute role. '
                                  'Please ask an administrator to set a role as the mute role, '
                                  'or make one by using the `setmuterole` or `createmuterole` commands.')

        mute_role = get(ctx.guild.roles, id=int(mute_role_id))  # get the actual mute role from the role's ID
        await user.add_roles(mute_role)  # add the mute role

        if time_period is not None:
            final_time_text = time_calc.time_suffix(time_period)
            await ctx.send(f'{user.display_name} has been muted for {final_time_text}.')
            await asyncio.sleep(time_calc.get_time(time_period))  # sleep for specified time, then remove the muted role
            await user.remove_roles(mute_role)
            await ctx.send(f'{user.display_name} has been unmuted.')
        else:
            await ctx.send(f'{user.display_name} has been muted.')

    @commands.command(name='hardmute', description='Hard-mutes the person mentioned. '
                                                   'This means all roles are removed until the mute period is over. '
                                                   'Time period is optional.')
    @commands.has_permissions(manage_roles=True)
    @commands.guild_only()
    async def hardmute_func(self, ctx, user: discord.Member, time_period=None):

        if misc_checks.is_author(ctx, user):
            return await ctx.send('You cannot mute yourself. Sorry lol')

        if misc_checks.is_client(self.bot, user):
            return await ctx.send('I can\'t mute myself, sorry.')

        if not os.path.exists(f'./configs/guild{ctx.guild.id}.json'):
            with open(f'./configs/guild{ctx.guild.id}.json', 'w') as createFile:
                json.dump({}, createFile, indent=4)

        with open(f'./configs/guild{ctx.guild.id}.json', 'r') as jsonFile:
            data = json.load(jsonFile)
        mute_role_id = int(data.get('mute_role'))

        if mute_role_id is None:
            return await ctx.send('It seems you have not set the mute role. '
                                  'Please ask an administrator to set a role as the mute role, '
                                  'or make one by using the `setmuterole` or `createmuterole` commands.')

        mute_role = get(ctx.guild.roles, id=mute_role_id)
        rolelist = [r.id for r in user.roles if r != ctx.guild.default_role]

        if not os.path.exists(f'./storage/mute_files/guild{ctx.guild.id}.json'):
            with open(f'./storage/mute_files/guild{ctx.guild.id}.json', 'w') as createFile:
                json.dump({}, createFile, indent=4)

        with open(f'./storage/mute_files/guild{ctx.guild.id}.json', 'r') as mute_file:
            data = json.load(mute_file)
        data[user.id] = list(rolelist)
        with open(f'./storage/mute_files/guild{ctx.guild.id}.json', 'w') as mute_file:
            json.dump(data, mute_file, indent=4)

        for x in rolelist:
            role = get(ctx.guild.roles, id=int(x))
            try:  # remove every role one by one
                await user.remove_roles(role)
            except:
                await ctx.send(f'Could not remove role {role.name} from {user.display_name}...')
                continue

        await user.add_roles(mute_role)  # add the mute role

        if time_period is not None:
            final_time_text = time_calc.get_time(time_period)
            await ctx.send(f'{user.display_name} has been muted for {final_time_text}.')
            await asyncio.sleep(time_calc.get_time(time_period))
            if mute_role not in user.roles:
                await Moderation.unmute_func(ctx, user)
        else:
            await ctx.send(f'{user.display_name} has been hard-muted.')

    @commands.command(name='unmute', description='Unmutes the user mentioned if muted previously.\n'
                                                 'It also attempts to add roles from before they were hard-muted '
                                                 '(if they were).\n'
                                                 'So don\'nt panic if it tries to add roles and fails.')
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    async def unmute_func(self, ctx, user: discord.Member):
        if not os.path.exists(f'./configs/guild{ctx.guild.id}.json'):
            with open(f'./configs/guild{ctx.guild.id}.json', 'w') as createFile:
                json.dump({}, createFile, indent=4)
                print(f'Created file guild{ctx.guild.id}.json in configs...')  # create file if not present

        with open(f'./configs/guild{ctx.guild.id}.json', 'r') as jsonFile:
            data = json.load(jsonFile)

        if data.get('mute_role') is None:
            return await ctx.send('It seems you have not set the mute role. '
                                  'Please ask an administrator to set a role as the mute role, '
                                  'or make one by using the `setmuterole` or `createmuterole` commands.')

        mute_role_id = int(data.get('mute_role'))

        mute_role = get(ctx.guild.roles, id=mute_role_id)

        await user.remove_roles(mute_role)

        with open(f'./storage/mute_files/guild{ctx.guild.id}.json', 'r') as mute_file:
            data = json.load(mute_file)
        role_ids = data.get(f'{user.id}')
        if role_ids is not None:
            for x in role_ids:
                actual_role = get(ctx.guild.roles, id=int(x))
                try:
                    await user.add_roles(actual_role)
                except:
                    await ctx.send(f'Could not add role **{actual_role.name}** to **{user.display_name}**')
                    continue
        await user.remove_roles(mute_role)
        await ctx.send(f'{user.display_name} has been unmuted.')

        data.pop(str(user.id))  # since they're unmuted, we don't need the role list

        with open(f'./storage/mute_files/guild{ctx.guild.id}.json', 'w') as mute_file:
            json.dump(data, mute_file, indent=4)

    # ban user
    @commands.command(name='ban', description='Does this really need a description?\n'
                                              'Bans the user who is mentioned as argument. '
                                              'Reason is optional. Defaults to the server\'s default Kick/Ban reason '
                                              'if no reason if given.')
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):

        if reason is None:
            if not os.path.exists(f'./configs/guild{ctx.guild.id}.json'):
                with open(f'./configs/guild{ctx.guild.id}.json', 'w') as createFile:
                    json.dump({}, createFile, indent=4)
                    print(
                        f'Created file guild{ctx.guild.id}.json in configs/...')  # create file if not present

            with open(f'./configs/guild{ctx.guild.id}.json', 'r') as jsonFile:
                data = json.load(jsonFile)
            default_kickBan_reason = data.get('default_kick_ban_reason')  # get the default reason
            reason = default_kickBan_reason

        message_to_user = f'You have been banned from **{ctx.guild.name}** for **{reason}**'

        try:
            await member.send(message_to_user)
        except:
            await ctx.send(f'Count not send DM to {member}. Banning anyway...')

        await member.ban(reason=reason)
        await ctx.send(f'**{member}** has been banned for **{reason}**.')

    # kick user
    @commands.command(name='kick', description='Kicks the user who is mentioned as argument.\n'
                                               'Reason is optional, '
                                               'and it defaults to the server\'s default Kick/Ban reason '
                                               'when no reason is given.')
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        if reason is None:
            if not os.path.exists(f'./storage/mute_files/guild{ctx.guild.id}.json'):
                with open(f'./storage/mute_files/guild{ctx.guild.id}.json', 'w') as createFile:
                    json.dump({}, createFile, indent=4)
                    print(
                        f'Created file guild{ctx.guild.id}.json in storage/mute_files...')  # create file if not present

            with open(f'./configs/guild{ctx.guild.id}.json', 'r') as jsonFile:
                data = json.load(jsonFile)
            default_kickBan_reason = data.get('default_kick_ban_reason')  # get the default reason
            reason = default_kickBan_reason

            message_to_user = f'You have been kicked from **{ctx.guild.name}** for **{reason}**'

            try:
                await member.send(message_to_user)
            except:
                await ctx.send(f'Count not send DM to {member}. Kicking anyway...')

            await member.kick(reason=reason)

            await ctx.send(f'**{member}** has been kicked for **{reason}**.')

    # unban user.
    @commands.command(name='unban', descriptiob='Unbans a member who is mentioned as argument.\n'
                                                'Correct format of mentioning the member is `User#0000` **ONLY**.')
    @commands.has_permissions(administrator=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split("#")

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'Unbanned {user}')


def setup(bot):
    bot.add_cog(Moderation(bot))
