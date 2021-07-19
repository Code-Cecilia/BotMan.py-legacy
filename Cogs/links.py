import discord
from discord.ext import commands
import json
import os


class Links(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='link', description='Sends a value to the corresponding link name, given as argument.\n'
                                               'PS: Ignore the last argument `IgnoreThis`')
    async def get_links(self, ctx, link_name, IgnoreThis=False):
        with open('./assets/global_links.json') as jsonFile:
            links_list_global = json.load(jsonFile)  # getting global links

        if not os.path.exists(f'./links/guild{ctx.guild.id}.json'):
            with open(f'./links/guild{ctx.guild.id}.json', 'w') as writeFile:
                print(f'./links/guild{ctx.guild.id}.json has been created')
                json.dump({}, writeFile)
        with open(f'./links/guild{ctx.guild.id}.json', 'r') as readFile:
            # getting guild-specific links
            guild_specific_links = json.load(readFile)

        # final links list, guild-specific links override global ones
        links_list_global.update(guild_specific_links)

        link_value = links_list_global.get(link_name)
        if link_value is None:
            link_value = "No Value Found\nCheck your spelling and/or capitalization. " \
                         "If this link does not exist, ask the server's administrators to make one."

        embed = discord.Embed(title=link_name.title(
        ), description=link_value, color=discord.Color.random())

        if IgnoreThis is True:
            # since we call the function for linkslist command, we dont want the embed in that case
            return link_value
        await ctx.send(embed=embed)

    @commands.command(name='addlink', description='Add a guild-only link,'
                                                  ' which can be accessed anywhere in this server.')
    @commands.has_permissions(administrator=True)
    async def add_link(self, ctx, link_name, link_url):
        # add the file if not present
        if not os.path.exists(f'./links/guild{ctx.guild.id}.json'):
            with open(f'./links/guild{ctx.guild.id}.json', 'w') as jsonFile:
                json.dump({}, jsonFile)
                print(f'./links/guild{ctx.guild.id}.json has been created')

        with open(f'./links/guild{ctx.guild.id}.json', 'r') as jsonFile:
            data = json.load(jsonFile)
        data[link_name] = str(link_url)

        with open(f'./links/guild{ctx.guild.id}.json', 'w') as writeFile:
            json.dump(data, writeFile)
        await ctx.send(f'{link_name} has been added to the guild-specific links.')
        await Links.get_links(self, ctx, link_name)

    @commands.command(name='remlink', description='Removed the guild-only link whose name is mentioned as argument')
    @commands.has_permissions(administrator=True)
    async def remove_link(self, ctx, link_name):
        # add the file if not present
        if not os.path.exists(f'./links/guild{ctx.guild.id}.json'):
            with open(f'./links/guild{ctx.guild.id}.json', 'w') as jsonFile:
                json.dump({}, jsonFile)
                print(f'./links/guild{ctx.guild.id}.json has been created')

        with open(f'./links/guild{ctx.guild.id}.json', 'r') as jsonFile:
            data = json.load(jsonFile)

        if link_name not in data.keys():
            await ctx.send(f'{link_name} is not in the links list.')
            return

        data.pop(link_name)
        await ctx.send(f'{link_name} removed from the link list.')

    @commands.command(name='linklist', aliases=['linkslist'], description='Lists all global and guild-specific links.')
    async def list_links(self, ctx):
        # add the file if not present
        if not os.path.exists(f'./links/guild{ctx.guild.id}.json'):
            with open(f'./links/guild{ctx.guild.id}.json', 'w') as jsonFile:
                json.dump({}, jsonFile)
                print(f'./links/guild{ctx.guild.id}.json has been created')

        with open('./assets/global_links.json') as GlobalLinksJson:
            links_list_global = json.load(GlobalLinksJson)
            links_list_global_keys = links_list_global.keys()  # getting global links
        with open(f'./links/guild{ctx.guild.id}.json', 'r') as readFile:
            guild_specific_links = json.load(readFile)
            # getting guild-specific links
            guild_specific_links_keys = guild_specific_links.keys()

        global_list_embed = ""
        guild_links_embed = ""
        for x in links_list_global_keys:
            link_value = await Links.get_links(self, ctx, x, True)
            global_list_embed += f"__[{x}]({link_value})__\n"

        for x in guild_specific_links_keys:
            link_value = await Links.get_links(self, ctx, x, True)
            guild_links_embed += f"__[{x}]({link_value})__\n"

        embed = discord.Embed(title="List of links", color=discord.Color.random(
        ), timestamp=ctx.message.created_at)
        embed.add_field(name='Global Links',
                        value=global_list_embed, inline=False)
        embed.add_field(name="Guild-specific Links",
                        value=guild_links_embed, inline=False)
        embed.set_footer(
            text=f'Command requested by {ctx.author.display_name}', icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Links(bot))
