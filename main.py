import discord
from discord.ext import commands
import json
import os

from pathlib import Path

with open('config.json', 'r') as detailsFile:
    details_data = json.load(detailsFile)
    prefix_list = details_data['prefix_list']
    main_prefix = details_data['main_prefix']
    token = details_data['token']
    status_link = details_data['status_link']
    bot_bio = details_data['bio']

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.members = True
activity = discord.Streaming(name=f'{main_prefix}help', url=status_link)


class NewHelpName(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
            embed = discord.Embed(description=page, color=discord.Color.random())
            embed.set_thumbnail(url=bot.user.avatar_url)
            embed.set_footer(text='')
            await destination.send(embed=embed)


cwd = Path(__file__).parents[0]
cwd = str(cwd)
bot = commands.Bot(command_prefix=prefix_list,
                   intents=intents,
                   help_command=NewHelpName(),
                   activity=activity,
                   owner_id=775176626773950474)
bot.cwd = cwd


@bot.event
async def on_ready():
    print(f'{bot.user} is online!')


if __name__ == '__main__':
    failed_modules = []
    for file in os.listdir(cwd + "/Cogs"):
        if file.endswith(".py") and not file.startswith("_"):
            print(f'Loading {file}...')
            try:
                bot.load_extension(f"Cogs.{file[:-3]}")  # loading the cogs
                print(f'        |--- Success')
            except:
                print(f'        |--- Failed')
                failed_modules.append(file)
    if len(failed_modules) != 0:
        print('====================')
        print('These cogs failed to load:')
        for x in failed_modules:
            print(x)
    print('====================')
    bot.run(token)
