import json
import os

import discord
from discord.ext import commands

from assets import get_link


class Links(commands.Cog, description="A cog for storing, sending, and modifying links."):

    def __init__(self, bot):
        self.bot = bot
        self.linksPath = "./links/"

    @commands.command(name='link', description='Sends a value to the corresponding link name, given as argument.\n')
    @commands.guild_only()
    async def get_links(self, ctx, link_name):
        link_value = get_link.get_link(ctx, link_name)
        link_final_return = f"__**{link_name}**__\n{link_value}"

        await ctx.send(link_final_return)

    @commands.command(name='addlink', description='Add a guild-only link,'
                                                  ' which can be accessed anywhere in this server.')
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def add_link(self, ctx, link_name, *, link_or_text):
        # add the file if not present
        if not os.path.exists(f'{self.linksPath}{ctx.guild.id}.json'):
            with open(f'{self.linksPath}{ctx.guild.id}.json', 'w') as jsonFile:
                json.dump({}, jsonFile)
                print(f'{self.linksPath}{ctx.guild.id}.json has been created')

        with open(f'{self.linksPath}{ctx.guild.id}.json', 'r') as jsonFile:
            data = json.load(jsonFile)
        data[link_name] = str(link_or_text)

        with open(f'{self.linksPath}{ctx.guild.id}.json', 'w') as writeFile:
            json.dump(data, writeFile)
        await ctx.send(f'{link_name} has been added to the guild-specific links.')
        await Links.get_links(self, ctx, link_name)

    @commands.command(name='remlink', description='Removed the guild-only link whose name is mentioned as argument')
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def remove_link(self, ctx, link_name):
        # add the file if not present
        if os.path.exists(f'{self.linksPath}{ctx.guild.id}.json'):
            with open(f'{self.linksPath}{ctx.guild.id}.json', 'r') as jsonFile:
                data = json.load(jsonFile)
        else:
            data = {}

        if link_name not in data.keys():
            await ctx.send(f'{link_name} is not in the links list.')
            return

        data.pop(link_name)
        with open(f'{self.linksPath}{ctx.guild.id}.json', 'w') as jsonFile:
            json.dump(data, jsonFile)
        await ctx.send(f'{link_name} removed from the link list.')

    @commands.command(name='linklist', aliases=['linkslist', "links"], description='Lists all global and guild-specific links.')
    @commands.guild_only()
    async def list_links(self, ctx):
        # add the file if not present
        with open('./assets/global_links.json') as GlobalLinksJson:
            links_list_global = json.load(GlobalLinksJson)
            links_list_global_keys = links_list_global.keys()  # getting global links
        if os.path.exists(f'{self.linksPath}{ctx.guild.id}.json'):
            with open(f'{self.linksPath}{ctx.guild.id}.json', 'r') as readFile:
                guild_specific_links = json.load(readFile)
                # getting guild-specific links
                guild_specific_links_keys = guild_specific_links.keys()
        else:
            guild_specific_links_keys = []

        global_list_embed = ""
        guild_links_embed = ""
        global_link_list = []
        guild_link_list = []
        for x in links_list_global_keys:
            global_link_list.append(x)
        global_link_list.sort()

        for x in guild_specific_links_keys:
            guild_link_list.append(x)
        guild_link_list.sort()

        for x in global_link_list:
            global_list_embed += f"{x}\n"

        for x in guild_link_list:
            guild_links_embed += f"{x}\n"

        global_list_embed += '\uFEFF'
        guild_links_embed += '\uFEFF'

        embed = discord.Embed(title="List of links", color=discord.Color.random(
        ), timestamp=ctx.message.created_at)
        embed.add_field(name='Global Links',
                        value=global_list_embed, inline=False)
        embed.add_field(name="Guild-specific Links",
                        value=guild_links_embed, inline=False)
        embed.set_footer(
            text=f'Requested by {ctx.author.display_name}', icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Links(bot))
