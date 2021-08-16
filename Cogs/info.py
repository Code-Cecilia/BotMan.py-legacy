import discord
from discord.ext import commands

from assets import time_calc, get_color


class Info(commands.Cog,
           description="Returns information about specific aspects of the server, role, emoji or a user."):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='userid', description='Returns the User\'s ID mentioned. '
                                                 'Returns author\'s ID if no argument is given.')
    async def userid(self, ctx, target: discord.Member = None):
        if target:
            await ctx.reply(target.id)
        else:
            await ctx.reply(ctx.author.id)

    @commands.command(name='avatar', description='Returns the avatar/pfp of the user mentioned.')
    async def get_avatar(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author
        embed = discord.Embed(
            title=f'Avatar of {user.display_name}', colour=get_color.get_color(user))
        embed.set_image(url=user.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name='serverinfo', description='Returns basic information about the server.\n'
                                                     'Add "features" to the command as an argument '
                                                     'to see a list of special features of this server.\n'
                                                     'More features will be added with time.')
    @commands.guild_only()
    async def serverinfo(self, ctx, *args):
        bots_count = len([bot.mention for bot in ctx.guild.members if bot.bot])
        channels_list = "{:,} text, {:,} voice".format(
            len(ctx.guild.text_channels), len(ctx.guild.voice_channels))
        created_date, created_time = time_calc.parse_utc(
            str(ctx.guild.created_at))

        embed = discord.Embed(title=ctx.guild.name, description=f'Server ID: {ctx.guild.id}',
                              timestamp=ctx.message.created_at,
                              color=discord.Color.random())
        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.add_field(
            name='Owner', value=ctx.guild.owner.mention, inline=True)
        embed.add_field(
            name='Members', value=ctx.guild.member_count, inline=True)
        embed.add_field(name='No. of roles', value=str(
            len(ctx.guild.roles) - 1), inline=True)
        embed.add_field(name='Date of creation',
                        value=str(created_date), inline=True)
        embed.add_field(name='Time of creation',
                        value=str(created_time), inline=True)
        embed.add_field(name='Channel Categories',
                        value=str(len(list(ctx.guild.categories))), inline=True)
        embed.add_field(name='Channels', value=str(channels_list), inline=True)
        try:
            embed.add_field(
                name='Booster Role', value=ctx.guild.premium_subscriber_role.mention, inline=True)
        except AttributeError:  # if no boost role, it gives a None value
            embed.add_field(name="Booster Role", value="No Role", inline=True)
        embed.add_field(name='Boost Tier',
                        value=f'Tier {ctx.guild.premium_tier}')
        embed.add_field(name='No. of Boosts',
                        value=ctx.guild.premium_subscription_count)
        embed.add_field(name='Emojis', value=str(
            len(ctx.guild.emojis)), inline=True)
        embed.add_field(name='Bots', value=str(bots_count))
        if not str(ctx.guild.banner_url) == "":
            embed.add_field(name="Banner", value="Banner below!", inline=False)
            embed.set_image(url=ctx.guild.banner_url)
        embed.set_footer(
            text=f'Command requested by {ctx.author.name}', icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
        print(ctx.guild.features)

        if "features" in args or "feature" in args:
            feature_string = ""
            if len(ctx.guild.features) == 0:
                embed_features = discord.Embed(title=f"{ctx.guild.name} does not have any special features",
                                               color=embed.color)
                return await ctx.send(embed=embed_features)
            for feature in ctx.guild.features:
                new_str = str(feature).replace("_", " ").title()
                feature_string += new_str + "\n"
            embed_features = discord.Embed(title=f"{ctx.guild.name}'s Special Features",
                                           description=feature_string, color=embed.color)
            await ctx.send(embed=embed_features)

    @commands.command(name='roleinfo', description='Returns basic information about the role mentioned as argument.')
    @commands.guild_only()
    async def role_info(self, ctx, role: discord.Role):
        role_name = role.name
        role_id = role.id
        role_creation_date, role_creation_time = time_calc.parse_utc(
            str(role.created_at))
        members_count = len(role.members)
        is_mentionable = str(role.mentionable)
        role_color = role.color
        embed = discord.Embed(title=f'Role: {role_name}', description=f'ID: {role_id} | Color: {role_color}',
                              timestamp=ctx.message.created_at, color=role_color)
        embed.add_field(name='Creation Date',
                        value=role_creation_date, inline=True)
        embed.add_field(name='Creation Time',
                        value=role_creation_time, inline=True)
        embed.add_field(name='No. of members',
                        value=str(members_count), inline=True)
        embed.add_field(name='Mentionable', value=is_mentionable, inline=False)
        embed.set_footer(
            text=f'Command requested by {ctx.author.name}', icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed)

    @commands.command(name='userinfo', aliases=['user', 'whois'],
                      description='Returns basic information about the user mentioned as argument.')
    @commands.guild_only()
    async def user_info(self, ctx, user: discord.Member):
        name = user.display_name
        discriminator = user.discriminator
        color = user.color
        id = user.id
        bot_bool = user.bot
        username = user.name
        avatar = user.avatar_url
        creation_date, creation_time = time_calc.parse_utc(
            str(user.created_at))
        try:
            mutual_guilds = len(user.mutual_guilds)
        except:
            mutual_guilds = 0
        req = await self.bot.http.request(discord.http.Route("GET", "/users/{uid}", uid=user.id))
        banner_id = req["banner"]
        # If statement because the user may not have a banner
        if banner_id:
            banner_url = f"https://cdn.discordapp.com/banners/{user.id}/{banner_id}?size=4096"
        else:
            banner_url = None

        embed = discord.Embed(
            title=name, description=f'ID: {id}', color=color, timestamp=ctx.message.created_at)
        embed.set_thumbnail(url=avatar)
        embed.set_footer(
            text=f'Command requested by {ctx.author.name}', icon_url=ctx.author.avatar_url)
        embed.add_field(name='Username',
                        value=f"{username}#{discriminator}", inline=True)
        embed.add_field(name='Is a Bot', value=bot_bool)
        embed.add_field(name='Color', value=color, inline=True)
        embed.add_field(name='Account Creation Date',
                        value=creation_date, inline=True)
        embed.add_field(name='Creation Time', value=creation_time, inline=True)
        embed.add_field(name=f'Mutual Servers with {self.bot.user.name}', value=str(
            mutual_guilds), inline=False)
        if banner_url:
            embed.add_field(name="Banner", value="See image below!", inline=False)
            embed.set_image(url=banner_url)
        await ctx.send(embed=embed)

    @commands.command(name='emojiinfo', description='Returns information about the emoji, passed as argument')
    async def emoji_info(self, ctx, emoji: discord.Emoji):
        emoji_actual = await ctx.guild.fetch_emoji(int(emoji.id))
        emoji = ctx.author if not emoji else emoji
        emoji_name = emoji.name
        guild = emoji.guild
        available_for_use = emoji.available
        creation_date, creation_time = time_calc.parse_utc(
            str(emoji.created_at))
        emoji_id = emoji.id
        emoji_url = emoji.url
        try:
            # emoji.user.mention cannot be used - it returns None
            creator = emoji_actual.user.mention
        except AttributeError:
            creator = "Insufficient Permissions"
        embed = discord.Embed(
            title=emoji_name, description=f'ID: {emoji_id}', color=get_color.get_color(ctx.author))
        embed.set_thumbnail(url=emoji_url)
        embed.add_field(name='Source Server', value=guild, inline=True)
        embed.add_field(name='Creator', value=creator, inline=True)
        embed.add_field(name="Is available",
                        value=available_for_use, inline=True)
        embed.add_field(name='Date of creation',
                        value=creation_date, inline=True)
        embed.add_field(name='Time of creation',
                        value=creation_time, inline=True)
        embed.set_footer(
            text=f'Command requested by {ctx.author}', icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Info(bot))
