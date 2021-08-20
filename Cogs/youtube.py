import discordTogether
from discord.ext import commands
from discordTogether import DiscordTogether as D_Together


class DiscordTogether(commands.Cog,
                      description="Don't have the Youtube Together or other activity features in your server?"
                                  " Use the commands in this category"):
    def __init__(self, bot):
        self.bot = bot
        self.togetherControl = D_Together(bot)

    @commands.command(name="startyoutube", aliases=["ytstart", "startyt", "youtubetogether"])
    async def start_youtube_activity(self, ctx):
        """Starts a Youtube Together activity in the voice channel you are in"""
        try:
            link = await self.togetherControl.create_link(ctx.author.voice.channel.id, "youtube")
        except AttributeError:
            return await ctx.send("You need to be in a voice channel to start a Youtube Together activity.")
        text = f"_{ctx.author.display_name}_, join the activity using this link!\n" \
               f"{link}"
        await ctx.send(text)

    @commands.command(name="startpoker", aliases=["startpokernight", "pokernight"])
    async def start_poker_together(self, ctx):
        """Starts the Poker Night activity in the voice channel you are in."""
        try:
            link = await self.togetherControl.create_link(ctx.author.voice.channel.id, "poker")
        except AttributeError:
            return await ctx.send("You need to be in a voice channel to start a Poker Night activity.")
        text = f"_{ctx.author.display_name}_, join the activity using this link!\n" \
               f"{link}"
        await ctx.send(text)

    @commands.command(name="startchess", aliases=["chessinthepark", "startchessinthepark", "chess"])
    async def start_chess_activity(self, ctx):
        """Starts the Chess In The Park activity in the voice channel you are in."""
        try:
            link = await self.togetherControl.create_link(ctx.author.voice.channel.id, "chess")
        except AttributeError:
            return await ctx.send("You need to be in a voice channel to start a Chess In The Park activity.")
        text = f"_{ctx.author.display_name}_, join the activity using this link!\n" \
               f"{link}"
        await ctx.send(text)

    @commands.command(name="startbetrayal", aliases=["startbetrayalio", "startberayal", "betrayalio"])
    async def start_betrayal_activity(self, ctx):
        """Starts the Betrayal.io activity in the voice channel you are in."""
        try:
            link = await self.togetherControl.create_link(ctx.author.voice.channel.id, "betrayal")
        except AttributeError:
            return await ctx.send("You need to be in a voice channel to start a Betrayal.io activity.")
        text = f"_{ctx.author.display_name}_, join the activity using this link!\n" \
               f"{link}"
        await ctx.send(text)

    @commands.command(name="startfishington", aliases=["startfishingtonio", "fishingtonio", "fishing"])
    async def start_fishington_activity(self, ctx):
        """Starts the Fishington.io activity in the voice channel you are in."""
        try:
            link = await self.togetherControl.create_link(ctx.author.voice.channel.id, "fishing")
        except AttributeError:
            return await ctx.send("You need to be in a voice channel to start a Fishington.io activity.")
        text = f"_{ctx.author.display_name}_, join the activity using this link!\n" \
               f"{link}"
        await ctx.send(text)

    @commands.command(name="startcustomactivity", aliases=["customactivity", "activity"])
    async def start_custom_activity(self, ctx, activity_id_or_name: str):
        """Starts a custom activity in the voice channel you are in.
Both the activity's ID and the activity's name are accepted as valid arguments."""
        try:
            if activity_id_or_name.isnumeric():
                link = await self.togetherControl.create_link(ctx.author.voice.channel.id, int(activity_id_or_name))
            else:
                link = await self.togetherControl.create_link(ctx.author.voice.channel.id, activity_id_or_name)
        except AttributeError:
            return await ctx.send("You need to be in a voice channel to start an activity.")
        except discordTogether.InvalidCustomID:
            return await ctx.send("Invalid activity ID. Please try with a valid ID.")
        except discordTogether.InvalidActivityChoice:
            return await ctx.send("Invalid activity name. Please try with a valid ID or name.")
        text = f"_{ctx.author.display_name}_, join the activity using this link!\n" \
               f"{link}"
        await ctx.send(text)


def setup(bot):
    bot.add_cog(DiscordTogether(bot))
