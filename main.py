import json
import os
import random
from pathlib import Path

import discord
import discord_slash
from discord.ext import commands, menus

from assets import count_lines, random_assets, get_color, list_funcs
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


class EmbedPageSource(menus.ListPageSource):
    async def format_page(self, menu, item):
        embed = discord.Embed(title=bot.description, color=discord.Color.blue(),
                              description="Use `bm-help [command/category]` for more information on a command/category.")
        embed.set_footer(text="React with the emojis to switch pages!")
        embed.set_thumbnail(url=bot.user.avatar_url)
        for x in item:
            embed.add_field(name=x["name"], value=x["value"], inline=x["inline"])
        return embed


def get_command_clean(command):
    return command.qualified_name


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
            command_signatures = [get_command_clean(c) for c in filtered]
            if command_signatures:
                cog_name = getattr(cog, "qualified_name", "No Category")
                embed.add_field(name=cog_name, value=", ".join([f"`{x}`" for x in command_signatures]), inline=False)
        to_dict = embed.to_dict()
        fields = to_dict.get("fields")
        chunked_fields = list_funcs.chunks(fields, 10)
        items_to_add = [x for x in chunked_fields]
        menu = menus.MenuPages(EmbedPageSource(items_to_add, per_page=1))
        await menu.start(self.context)

    async def send_command_help(self, command):
        channel = self.get_destination()
        user = channel.guild.me
        if command.cog is not None:
            cog_name = command.cog.qualified_name
            embed = discord.Embed(title=f"{get_command_clean(command)} - Extension of the {cog_name} cog"
                                  , color=get_color.get_color(user))
        else:
            embed = discord.Embed(title=f"{self.get_command_signature(command)}"
                                  , color=get_color.get_color(user))
        embed.set_thumbnail(url=bot.user.avatar_url)
        if command.description:
            embed.add_field(name="Description", value=command.description, inline=False)
        if command.help:
            embed.add_field(name="Help", value=command.help, inline=False)
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
        if cog.description:
            embed.description = cog.description
        if not len(commands_embed_list) == 0:
            embed.add_field(name="Commands", value=commands_embed_list, inline=False)
        else:
            embed.add_field(name="Commands", value="No Commands are present in this Cog.", inline=False)
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
                   owner_id=owner_id,  # owner's ID as in the config file
                   max_messages=100000)
bot.cwd = cwd


@bot.event
async def on_ready():
    print(f'{bot.user} is online!')
    if os.path.exists("./storage/reboot.json"):
        with open("./storage/reboot.json", "r") as readFile:
            channel_id = json.load(readFile)
        channel = bot.get_channel(id=channel_id)
        await channel.send("Rebooted Successfully!")
        if len(failed_modules) != 0:
            failed_modules_string = "\n".join(failed_modules)
            embed = discord.Embed(title="These modules failed to load", color=discord.Color.dark_red())
            embed.description = failed_modules_string
            await channel.send(embed=embed)
        os.remove("./storage/reboot.json")

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
