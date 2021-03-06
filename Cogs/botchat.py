import json
import os
import aiml
import discord
from discord.ext import commands

from assets import refine_text


class BotChat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.chatBot = aiml.Kernel()
        self.botBrain = 'BotChat/brain.brn'
        self.botDir = "BotChat/AimlFiles"
        self.botName = "BotMan"
        self.botGender = "male"
        self.ownerName = "Mahasvan"
        self.ownerGender = "male"
        self.botBirthDate = "21 May 2021"
        self.botEmail = "mahasvan@gmail.com"
        # Credit for the whole AIML code - CorpNewt
        with open("./storage/botchat_channels.json", "r") as botchatFile:
            self.botchat_channels = json.load(botchatFile)
        with open("./storage/botchat_mode.json", "r") as botchatModeFile:
            self.botchat_mode = json.load(botchatModeFile)
        with open('config.json', 'r') as configFile:
            self.api_key = json.load(configFile).get('rsa_api_key')

    @commands.Cog.listener()
    async def on_ready(self):
        if not os.path.exists(self.botBrain):
            # No brain, let's learn and create one
            files = os.listdir(self.botDir)
            for file in files:
                # Omit files starting with . or _
                if file.startswith(".") or file.startswith("_"):
                    continue
                self.chatBot.learn(self.botDir + '/' + file)
            # Save brain
            self.chatBot.saveBrain(self.botBrain)
        else:
            # Already have a brain - load it
            self.chatBot.bootstrap(brainFile=self.botBrain)
        # Learned by this point - let's set our owner's name/gender
        # Start the convo
        self.chatBot.respond('Hello')
        # Bot asks for our Name
        self.chatBot.respond('My name is {}'.format(self.ownerName))
        # Bot asks for our gender
        self.chatBot.respond('I am a {}'.format(self.ownerGender))

    @commands.command(name="setbotchatchannel", description="Sets the channel for botchat")
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    async def set_botchat_channel(self, ctx, channel: discord.TextChannel):

        self.botchat_channels[str(ctx.guild.id)] = channel.id  # set botchat channel

        with open(f'./storage/botchat_channels.json', 'w') as jsonFile:
            json.dump(self.botchat_channels, jsonFile, indent=4)  # dump the file

        await ctx.send(f"Set botchat channel as {channel.mention} successfully!")

    @commands.Cog.listener()
    @commands.guild_only()
    async def on_message(self, message):
        if message.author.bot:
            return
        try:
            botchat_channel_id = self.botchat_channels.get(str(message.guild.id))
        # getting the botchat channel from storage
        except AttributeError:  # direct messages don't have a guild
            return
        if botchat_channel_id is None:
            return
        botchat_channel = self.bot.get_channel(botchat_channel_id)
        # getting the botchat channel
        if botchat_channel is None or message.author == self.bot.user or not message.channel == botchat_channel:
            return
        response = self.chatBot.respond(message.content.replace("@", "`@`"))
        await botchat_channel.send(response)  # sending the response

    @commands.command(name='chat', aliases=['botchat'], description='One-time chat command.')
    async def one_time_chat(self, ctx, *, message: commands.clean_content(fix_channel_mentions=True, use_nicknames=True,
                                                                          remove_markdown=True)):
        response = self.chatBot.respond(message)
        await ctx.send(response)  # sending the response


def setup(bot):
    bot.add_cog(BotChat(bot))
