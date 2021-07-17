import discord
from discord.ext import commands
import json
import os
import time

from pathlib import Path
from assets.keep_alive import keep_alive

with open('config.json', 'r') as detailsFile:
    details_data = json.load(detailsFile)
    prefix_list = details_data['prefix_list']
    main_prefix = details_data['main_prefix']
    token = details_data['token']
    status_link = details_data['status_link']
    bot_bio = details_data['bio']
    is_replit = details_data['replit']
    owner_id = int(details_data['owner_id'])

replit_bool = False
if is_replit.lower() in ['true', 'yes', 'sure', 'why not']:
    replit_bool = True

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.members = True
activity = discord.Streaming(name=f'{main_prefix}help', url=status_link)


def get_prefix(client, message):
    with open('./storage/prefixes.json', 'r') as f:
        prefixes = json.load(f)
        prefix_server = prefixes.get(str(message.guild.id))

        if prefix_server is None:
            prefix_server = "bm-"

        return prefix_server


class NewHelpName(commands.MinimalHelpCommand):  # we're making a new help command
    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
            embed = discord.Embed(description=page, color=discord.Color.random())
            embed.set_thumbnail(url=bot.user.avatar_url)
            embed.set_footer(text='')
            await destination.send(embed=embed)


cwd = Path(__file__).parents[0]
cwd = str(cwd)
bot = commands.Bot(command_prefix=get_prefix,
                   intents=intents,
                   help_command=NewHelpName(),  # custom help command
                   activity=activity,
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
                failed_modules.append(file)  # append the file to the list of cogs which failed to load
    if len(failed_modules) != 0:
        print('====================')
        print('These cogs failed to load:')
        for x in failed_modules:
            print(x)
    print('====================')
    if replit_bool:
        keep_alive()  # run the replit-specific code (refer assets/keep_alive.py)
    bot.run(token)  # actually running the bot
