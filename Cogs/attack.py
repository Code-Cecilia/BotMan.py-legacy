import ast
import asyncio
import os

import discord
from discord.ext import commands

from assets import aiohttp_assets, get_color, otp_assets
from assets import random_assets as rand_ass


class Attack(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.spank_url = "https://api.devs-hub.xyz/spank?"
        self.hitler_url = "https://api.devs-hub.xyz/hitler?image="
        self.grab_url = "https://api.devs-hub.xyz/grab?image="
        self.trigger_url = "https://api.devs-hub.xyz/trigger?image="
        self.delete_url = "https://api.devs-hub.xyz/delete?image="
        self.wasted_url = "https://api.devs-hub.xyz/wasted?image="
        self.beautiful_url = "https://api.devs-hub.xyz/beautiful?image="

    @commands.command(name='eat', description='Eat a member, install fear!')
    async def eat_func_actual(self, ctx, *, user: discord.Member):
        await ctx.send(rand_ass.eat_func(ctx.author, user, self.bot))

    @commands.command(name='drink', description='Beware, you might spill the user you\'re trying to drink.')
    async def drink_func(self, ctx, *, user: discord.Member):
        await ctx.send(rand_ass.drink_func(ctx.author, user, self.bot))

    @commands.command(name='hug', description='Try hugging yourself.')
    async def hug_func(self, ctx, *, user: discord.Member):
        await ctx.send(rand_ass.hug_func(ctx.author, user, self.bot))

    @commands.command(name='pet', description='Pets whoever you mention. Exceptions may exist.')
    async def pet_func(self, ctx, *, user: discord.Member):
        await ctx.send(rand_ass.pet_func(ctx.author, user, self.bot))

    @commands.command(name="spank", description="Spank a user.")
    async def spank(self, ctx, *, member: discord.Member):
        one_time_int = otp_assets.get_otp(digits=4)
        #  random 4 digit int so multiple requests dont overwrite the file
        if member is None:
            member = ctx.author
        async with ctx.typing():
            user1 = ctx.author.avatar_url
            user2 = member.avatar_url
            spank_url = f"{self.spank_url}face={user1}&face2={user2}"

            binary_data = await aiohttp_assets.aiohttp_get_binary(spank_url)

            with open(f"./storage/spank{one_time_int}.png", "wb") as writeFile:
                writeFile.write(binary_data)
            file = discord.File(f"./storage/spank{one_time_int}.png", filename=f"spank{one_time_int}.png")

            embed = discord.Embed(title=f"Get spanked, {member.display_name}!", color=get_color.get_color(member))
            embed.set_image(url=f"attachment://spank{one_time_int}.png")
            await ctx.reply(file=file, embed=embed)
        await asyncio.sleep(1)
        os.remove(f"./storage/spank{one_time_int}.png")

    @commands.command(name="hitler", description="Breaking news! [user] is worse than Hitler!")
    async def hitler(self, ctx, *, member: discord.Member = None):
        one_time_int = otp_assets.get_otp(digits=4)
        #  random 4 digit int so multiple requests dont overwrite the file
        if member is None:
            member = ctx.author
        async with ctx.typing():
            hitler_url = f"{self.hitler_url}{member.avatar_url}"

            binary_data = await aiohttp_assets.aiohttp_get_binary(hitler_url)

            with open(f"./storage/hitler{one_time_int}.png", "wb") as writeFile:
                writeFile.write(binary_data)
            file = discord.File(f"./storage/hitler{one_time_int}.png", filename=f"hitler{one_time_int}.png")

            embed = discord.Embed(title=f"Oh no {member.name}, what have you done!",
                                  color=get_color.get_color(member))
            embed.set_image(url=f"attachment://hitler{one_time_int}.png")
            await ctx.reply(file=file, embed=embed)
        await asyncio.sleep(1)
        os.remove(f"./storage/hitler{one_time_int}.png")

    @commands.command(name="grab", description="Make a user's pfp grab you!")
    async def grab(self, ctx, *, user: discord.Member = None):
        one_time_int = otp_assets.get_otp(digits=4)
        #  random 4 digit int so multiple requests dont overwrite the file
        if user is None:
            user = ctx.author
        grab_url = f"{self.grab_url}{user.avatar_url}"
        async with ctx.typing():
            binary_data = await aiohttp_assets.aiohttp_get_binary(grab_url)
            try:
                dict_error = ast.literal_eval(binary_data.decode("utf-8"))
                if dict_error.get("error") is not None:
                    return await ctx.send(dict_error.get("error"))
            except:
                pass
            with open(f"./storage/grab{one_time_int}.png", "wb") as writeFile:
                writeFile.write(binary_data)
            file = discord.File(f"./storage/grab{one_time_int}.png", filename=f"grab{one_time_int}.png")

            embed = discord.Embed(color=get_color.get_color(ctx.author))
            embed.set_image(url=f"attachment://grab{one_time_int}.png")
            await ctx.reply(file=file, embed=embed)
        await asyncio.sleep(1)
        os.remove(f"./storage/grab{one_time_int}.png")

    @commands.command(name="trigger", description="Trigger a user! Get a \"Triggered!\" image!")
    async def trigger(self, ctx, *, member: discord.Member = None):
        one_time_int = otp_assets.get_otp(digits=4)
        #  random 4 digit int so multiple requests dont overwrite the file
        if member is None:
            member = ctx.author
        grab_url = f"{self.trigger_url}{member.avatar_url}"
        async with ctx.typing():
            binary_data = await aiohttp_assets.aiohttp_get_binary(grab_url)
            with open(f"./storage/trigger{one_time_int}.gif", "wb") as writeFile:
                writeFile.write(binary_data)
            file = discord.File(f"./storage/trigger{one_time_int}.gif", filename=f"trigger{one_time_int}.gif")

            embed = discord.Embed(color=get_color.get_color(ctx.author))
            embed.set_image(url=f"attachment://trigger{one_time_int}.gif")
            await ctx.reply(file=file, embed=embed)
        await asyncio.sleep(1)
        os.remove(f"./storage/trigger{one_time_int}.gif")

    @commands.command(name="delete", description="Delete a member. Begone, filthy mortal!")
    async def delete_user(self, ctx, user: discord.Member = None, dark=None):
        if user is None:
            user = ctx.author

        one_time_int = otp_assets.get_otp(digits=4)
        if dark == "dark":
            grab_url = f"{self.delete_url}{user.avatar_url}&darkmode={dark}"
        else:
            grab_url = f"{self.delete_url}{user.avatar_url}"
        async with ctx.typing():
            binary_data = await aiohttp_assets.aiohttp_get_binary(grab_url)
            with open(f"./storage/delete{one_time_int}.png", "wb") as writeFile:
                writeFile.write(binary_data)
            file = discord.File(f"./storage/delete{one_time_int}.png", filename=f"delete{one_time_int}.png")
            embed = discord.Embed(color=get_color.get_color(user))
            embed.set_image(url=f"attachment://delete{one_time_int}.png")
            await ctx.reply(file=file, embed=embed)
        await asyncio.sleep(1)
        os.remove(f"./storage/delete{one_time_int}.png")

    @commands.command(name="wasted", aliases=["gta"], description="A user's pfp, but with the GTA \"Wasted\" overlay")
    async def wasted(self, ctx, *, user: discord.Member = None):
        if user is None:
            user = ctx.author
        url = f"{self.wasted_url}{user.avatar_url}"
        one_time_int = otp_assets.get_otp(digits=4)
        async with ctx.typing():
            binary_data = await aiohttp_assets.aiohttp_get_binary(url)
            with open(f"./storage/wasted{one_time_int}.png", "wb") as writeFile:
                writeFile.write(binary_data)
            file = discord.File(f"./storage/wasted{one_time_int}.png", filename=f"wasted{one_time_int}.png")
            embed = discord.Embed(color=get_color.get_color(user), title=f"{user.display_name}, you died.")
            embed.set_image(url=f"attachment://wasted{one_time_int}.png")
            await ctx.reply(file=file, embed=embed)
        await asyncio.sleep(1)
        os.remove(f"./storage/wasted{one_time_int}.png")

    @commands.command(name="beautiful", description="compliment a user for their beauty.")
    async def beautiful(self, ctx, *, user: discord.Member = None):
        if user is None:
            user = ctx.author
        url = f"{self.beautiful_url}{user.avatar_url}"
        one_time_int = otp_assets.get_otp(digits=4)
        async with ctx.typing():
            binary_data = await aiohttp_assets.aiohttp_get_binary(url)
            with open(f"./storage/beautiful{one_time_int}.png", "wb") as writeFile:
                writeFile.write(binary_data)
            file = discord.File(f"./storage/beautiful{one_time_int}.png", filename=f"beautiful{one_time_int}.png")
            embed = discord.Embed(color=get_color.get_color(user), title=f"{user.display_name}, you're beautiful.")
            embed.set_image(url=f"attachment://beautiful{one_time_int}.png")
            await ctx.reply(file=file, embed=embed)
        await asyncio.sleep(1)
        os.remove(f"./storage/beautiful{one_time_int}.png")


def setup(bot):
    bot.add_cog(Attack(bot))
