import json
import os
from pathlib import Path

import discord
from discord.ext import commands

from assets.keep_alive import keep_alive

with open('config.json', 'r') as detailsFile:
    details_data = json.load(detailsFile)
    prefix = details_data['prefix']
    token = details_data['token']
    owner_id = int(details_data['owner_id'])

replit = False

status_link = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.members = True
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


class NewHelpName(commands.MinimalHelpCommand):  # we're making a new help command
    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
            embed = discord.Embed(
                description=page, color=discord.Color.random())
            embed.set_thumbnail(url=bot.user.avatar_url)
            embed.set_footer(text='')
            await destination.send(embed=embed)


cwd = Path(__file__).parents[0]
cwd = str(cwd)
bot = commands.Bot(command_prefix=get_prefix,
                   intents=intents,
                   help_command=NewHelpName(),  # custom help command
                   activity=activity,
                   description=description,
                   owner_id=owner_id)  # owner's ID as in the config file
bot.cwd = cwd


@bot.event
async def on_ready():
    print(f'{bot.user} is online!')


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
