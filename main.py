import json
import os
import random
from pathlib import Path

import discord
import discord_slash
from discord.ext import commands

from assets import count_lines, random_assets, get_color
from assets.keep_alive import keep_alive

with open('config.json', 'r') as detailsFile:
    details_data = json.load(detailsFile)
    prefix = details_data['prefix']
    token = details_data['token']
    owner_id = int(details_data['owner_id'])

replit = True

status_link = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

intents = discord.Intents.all()
activity = discord.Streaming(name=f'{prefix}help', url=status_link)
description = "The coolest python bot ever 😎"


def get_prefix(bot, message):
    with open('./storage/prefixes.json', 'r') as f:
        prefixes = json.load(f)
        try:
            prefix_server = prefixes.get(str(message.guild.id))

        except AttributeError:  # direct messages dont have a message.guild
            return 'bm-'

        if prefix_server is None:
            prefix_server = "bm-"
        data = prefix_server
        return commands.when_mentioned_or(data)(bot, message)


help_attributes = {
    'name': "help",
    'aliases': ["hell", "helps", "helmp", "helo"],
    'description': "Shows this command. (Obviously)"
}


class MyHelp(commands.MinimalHelpCommand):
    def get_command_signature(self, command):
        return '%s%s %s' % (self.clean_prefix, command.qualified_name, command.signature)

    def get_command_name(self, command):
        return '%s%s' % (self.clean_prefix, command.qualified_name)

    async def send_bot_help(self, mapping):
        channel = self.get_destination()
        user = channel.guild.me
        embed = discord.Embed(title=bot.description, colour=get_color.get_color(user))
        embed.description = f"Use `{self.clean_prefix}help [command/category]` " \
                            f"for more information on a command/category."
        embed.set_thumbnail(url=bot.user.avatar_url)
        for cog, commands_list in mapping.items():
            filtered = await self.filter_commands(commands_list, sort=True)
            command_signatures = [self.get_command_signature(c) for c in filtered]
            if command_signatures:
                cog_name = getattr(cog, "qualified_name", "No Category")
                embed.add_field(name=cog_name, value=", ".join(command_signatures), inline=False)

        await channel.send(embed=embed)

    async def send_command_help(self, command):
        channel = self.get_destination()
        user = channel.guild.me
        if command.cog is not None:
            cog_name = command.cog.qualified_name
            embed = discord.Embed(title=f"{self.get_command_name(command)}: Extension of {cog_name}"
                                  , color=get_color.get_color(user))
        else:
            embed = discord.Embed(title=f"{self.get_command_signature(command)}"
                                  , color=get_color.get_color(user))
        embed.set_thumbnail(url=bot.user.avatar_url)
        if command.description:
            embed.add_field(name="Description", value=command.description)
        alias = command.aliases
        embed.add_field(name="Usage", value=self.get_command_signature(command), inline=False)
        if alias:
            embed.add_field(name="Aliases", value=", ".join(alias), inline=False)
        await channel.send(embed=embed)

    async def send_cog_help(self, cog):
        channel = self.get_destination()
        user = channel.guild.me
        commands_list = cog.get_commands()
        cog_title = cog.qualified_name
        filtered = await self.filter_commands(commands_list, sort=True)
        embed = discord.Embed(title=f"Cog - {cog_title}", colour=get_color.get_color(user))
        embed.set_thumbnail(url=bot.user.avatar_url)
        commands_embed_list = "\n".join([("%s%s" % (self.clean_prefix, command.name)) for command in filtered])
        embed.description = cog.description
        embed.add_field(name="Commands", value=commands_embed_list, inline=False)
        await channel.send(embed=embed)

    async def send_error_message(self, error):
        channel = self.get_destination()
        user = channel.guild.me
        embed = discord.Embed(title="Error", description=error, colour=get_color.get_color(user))
        await channel.send(embed=embed)


cwd = Path(__file__).parents[0]
cwd = str(cwd)
bot = commands.Bot(command_prefix=get_prefix,
                   intents=intents,
                   help_command=MyHelp(command_attrs=help_attributes),  # custom help command
                   activity=activity,
                   description=description,
                   owner_id=owner_id,
                   max_messages=100000,
                   shard_count=10)  # owner's ID as in the config file
bot.cwd = cwd


@bot.event
async def on_ready():
    print(f'{bot.user} is online!')


# slash commands
slash = discord_slash.SlashCommand(client=bot, sync_commands=True)


@slash.slash(name="ping", description="Returns the latency of the bot.")
async def ping(ctx):
    latency = float(bot.latency) * 1000
    latency = round(latency, 2)
    await ctx.send(f'Pong! `Latency: {latency}ms`')


@slash.slash(name="vote", description="Vote for me on top.gg!")
async def vote_topgg(ctx):
    embed = discord.Embed(title=f"{ctx.author.display_name}, you can vote for me here!",
                          description="https://top.gg/bot/845225811152732179/vote",
                          color=discord.Color.random())
    await ctx.send(embed=embed)


@slash.slash(name='countlines', description='Counts the number of lines of python code the bot currently has.')
async def countlines_func(ctx):
    lines = count_lines.countlines('./')
    final_str = random.choice(random_assets.countlines_responses).format(lines)
    embed = discord.Embed(title=final_str, color=get_color.get_color(bot.user))
    await ctx.send(embed=embed)


@slash.slash(name="help", description="Are you lost? Let me show you the way!")
async def slash_help(ctx):
    embed = discord.Embed(
        title=f"Need help, {ctx.author.name}?", color=get_color.get_color(ctx.author))
    guild_prefix = get_prefix(bot, ctx.message)
    embed.description = f"My prefix for this server is `{guild_prefix}` " \
                        f"and my help command can be accessed through `{guild_prefix}help`.\n" \
                        f"If you want to use my commands in private messages, use the `bm-` prefix."
    embed.set_thumbnail(url=bot.user.avatar_url)
    embed.set_footer(text="Have fun!")
    await ctx.send(embed=embed)


if __name__ == '__main__':
    failed_modules = []
    for file in os.listdir(cwd + "/Cogs"):
        if file.endswith(".py") and not file.startswith("_"):  # loading the cog
            print(f'Loading {file}...')
            try:
                bot.load_extension(f"Cogs.{file[:-3]}")  # loading the cogs
                print(f'        |--- Success')
            except:
                print(f'        |--- Failed')  # if failed, print as failed
                # append the file to the list of cogs which failed to load
                failed_modules.append(file)
    if len(failed_modules) != 0:
        print('====================')
        print('These cogs failed to load:')
        for x in failed_modules:
            print(x)
    print('====================')
    if replit:
        keep_alive()  # run the replit-specific code (refer assets/keep_alive.py)
    bot.run(token)  # actually running the bot
