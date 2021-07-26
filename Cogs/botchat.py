import os
import json
import discord
from discord.ext import commands
from prsaw import RandomStuff

from assets import refine_text

with open('config.json', 'r') as configFile:
    data = json.load(configFile)

api_key = data.get('rsa_api_key')
rs = RandomStuff(async_mode=True, api_key=api_key)


class BotChat(commands.Cog, description='A Cog to... chat with the bot, i guess?\n'
                                        'Uses the __[RSA](https://docs.pgamerx.com/version-4/ai-response)__ API.\n'
                                        'Have fun!'):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="setbotchatchannel", description="Sets the channel for botchat")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def set_botchat_channel(self, ctx, channel: discord.TextChannel):
        channel_id = channel.id
        # create file if not exists
        if not os.path.exists(f'./configs/guild{ctx.guild.id}.json'):
            with open(f'./configs/guild{ctx.guild.id}.json', 'w') as jsonFile:
                json.dump({}, jsonFile)

        with open(f'./configs/guild{ctx.guild.id}.json', 'r') as jsonFile:
            data = json.load(jsonFile)
        data['botchat_channel'] = channel_id  # set botchat channel

        with open(f'./configs/guild{ctx.guild.id}.json', 'w') as jsonFile:
            json.dump(data, jsonFile, indent=4)  # dump the file

        await ctx.send(f"Set botchat channel as {channel} succesfully!")

    @commands.Cog.listener()
    @commands.guild_only()
    async def on_message(self, message):

        if message.author == self.bot.user:  # ignore if author of message is the bot user
            return

        # create file if not exists
        try:
            if not os.path.exists(f'./configs/guild{message.guild.id}.json'):
                with open(f'./configs/guild{message.guild.id}.json', 'w') as jsonFile:
                    json.dump({}, jsonFile)
        except AttributeError:
            return None

        with open(f'./configs/guild{message.guild.id}.json') as jsonFIle:
            data = json.load(jsonFIle)
            if data.get('botchat_channel') is not None:
                botchat_channel_id = int(data.get('botchat_channel'))  # getting the botchat channel id
            else:
                botchat_channel_id = data.get('botchat_channel')
            botchat_channel = self.bot.get_channel(botchat_channel_id)  # getting the botchat channel
            if message.channel == botchat_channel:
                message_refined = refine_text.remove_mentions(str(message.content))  # remove everyone and here mentions
                response = await rs.get_ai_response(message=message_refined, language='english')
                response = response[0]
                response = response.get('message')
                await botchat_channel.send(response)  # sending the response

    @commands.command(name='chat', aliases=['botchat'], description='One-time chat command.')
    async def one_time_chat(self, ctx, *, message):
        message_refined = refine_text.remove_mentions(message)
        response = await rs.get_ai_response(message=message_refined)  # returns a list
        response = response[0]  # getting the first entry, which is a dict
        # getting the message, which is inside the dict
        response = response.get('message')
        await ctx.send(response)  # sending the response


def setup(bot):
    bot.add_cog(BotChat(bot))
