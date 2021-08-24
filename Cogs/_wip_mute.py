import json
import re
import time

import discord
from discord.ext import commands, tasks

from assets import time_calc


class NewMute(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.muteFilesPath = "./storage/mute_file_iter.json"

    async def unmute_user(self, guild: int, user: int):
        guild = self.bot.get_guild(id=guild)
        member = guild.get_member(user_id=user)
        with open(f"./configs/guild{guild.id}.json", "r") as muteDetails:
            data = json.load(muteDetails)
        mute_role = guild.get_role(role_id=int(data.get("mute_role")))
        await member.remove_roles(mute_role)

    @tasks.loop(seconds=1)
    async def unmute_sweeps(self):
        try:
            time_now = time.time()
            with open(self.muteFilesPath, "r") as jsonFile:
                data = json.load(jsonFile)
                for guild_id in data.keys():
                    for user_id in data[str(guild_id)].keys():
                        if data[str(guild_id)][str(user_id)] <= int(time_now):
                            data[str(guild_id)].pop(str(user_id))
                            with open(self.muteFilesPath, "w") as writeFile:
                                json.dump(data, writeFile)
                            await NewMute.unmute_user(self, guild=int(guild_id), user=int(user_id))
        except RuntimeError:
            pass
        except json.JSONDecodeError:
            pass

    @commands.command(name="mute_new")
    async def mute(self, ctx, user: discord.Member, time_period=None):
        if time_period is not None:
            pattern = r"^[\d]+[s|m|h|d]{1}$"
            if not re.match(pattern, time_period):
                return await ctx.send("Time period is of the wrong format.\n"
                                      "Example usage: `5s`, `10m`, `15h`, `2d`")

        time_seconds = time_calc.get_time(time_period)
        time_thing = time.time()
        print(time_thing)
        unmute_time = time_thing + time_seconds
        with open(f"./configs/guild{ctx.guild.id}.json", "r") as muteDetails:
            data = json.load(muteDetails)
        if data.get("mute_role") is None:
            return await ctx.send('It seems you have not set the mute role. '
                                  'Please ask a person with the `Manage Server` permission '
                                  'to set a role as the mute role, '
                                  'or make one by using the `setmuterole` or `createmuterole` commands.')

        mute_role = ctx.guild.get_role(role_id=int(data.get("mute_role")))
        if time_period is not None:
            with open(self.muteFilesPath, "r") as jsonFile:
                data = json.load(jsonFile)
            try:
                data[str(ctx.guild.id)][str(user.id)] = unmute_time
            except KeyError:
                data[str(ctx.guild.id)] = {}
                data[str(ctx.guild.id)][str(user.id)] = unmute_time
            with open(self.muteFilesPath, "w") as jsonFile:
                json.dump(data, jsonFile)

            await user.add_roles(mute_role)
            final_time_text = time_calc.time_suffix(time_period)
            await ctx.send(f"{user} has been muted for {final_time_text}")
        else:
            await user.add_roles(mute_role)
            await ctx.send(f"{user.display_name} has been muted.")

    @commands.Cog.listener()
    async def on_ready(self):
        await NewMute.unmute_sweeps.start(self)


def setup(bot):
    bot.add_cog(NewMute(bot))
