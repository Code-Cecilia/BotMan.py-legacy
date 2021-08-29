import ast
import asyncio
import os
import random

import discord
from discord.ext import commands

from assets import aiohttp_assets, get_color
from assets import random_assets as rand_ass


class Attack(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.spank_url = "https://api.devs-hub.xyz/spank?"
        self.hitler_url = "https://api.devs-hub.xyz/hitler?image="
        self.grab_url = "https://api.devs-hub.xyz/grab?image="
        self.trigger_url = "https://api.devs-hub.xyz/trigger?image="
        self.delete_url = "https://api.devs-hub.xyz/delete?image="

    @commands.command(name='eat', description='Eat a member, install fear!')
    async def eat_func_actual(self, ctx, user: discord.Member):
        await ctx.send(rand_ass.eat_func(ctx.author, user, self.bot))

    @commands.command(name='drink', description='Beware, you might spill the user you\'re trying to drink.')
    async def drink_func(self, ctx, user: discord.Member):
        await ctx.send(rand_ass.drink_func(ctx.author, user, self.bot))

    @commands.command(name='hug', description='Try hugging yourself.')
    async def hug_func(self, ctx, user: discord.Member):
        await ctx.send(rand_ass.hug_func(ctx.author, user, self.bot))

    @commands.command(name='pet', description='Pets whoever you mention. Exceptions may exist.')
    async def pet_func(self, ctx, user: discord.Member):
        await ctx.send(rand_ass.pet_func(ctx.author, user, self.bot))

    @commands.command(name="spank", description="Spank a user.")
    async def spank(self, ctx, member: discord.Member = None):
        one_time_int = "".join([str(random.randint(0, 9)), str(random.randint(0, 9)),
                                str(random.randint(0, 9)), str(random.randint(0, 9))])
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

            embed = discord.Embed(title=f"{ctx.author.display_name}, You just spanked {member.name}!",
                                  color=get_color.get_color(member))
            embed.set_image(url=f"attachment://spank{one_time_int}.png")
            await ctx.reply(file=file, embed=embed)
        await asyncio.sleep(1)
        os.remove(f"./storage/spank{one_time_int}.png")

    @commands.command(name="hitler", description="Breaking news! [user] is worse than Hitler!")
    async def hitler(self, ctx, member: discord.Member = None):
        one_time_int = "".join([str(random.randint(0, 9)), str(random.randint(0, 9)),
                                str(random.randint(0, 9)), str(random.randint(0, 9))])
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

    @commands.command(name="grab", description="Enter an image URL with a face, get a grabbing image.")
    async def grab(self, ctx, image_url=None):
        one_time_int = "".join([str(random.randint(0, 9)), str(random.randint(0, 9)),
                                str(random.randint(0, 9)), str(random.randint(0, 9))])
        #  random 4 digit int so multiple requests dont overwrite the file
        if image_url is None:
            if not ctx.message.attachments:
                return await ctx.send("Please attach an image or provide an image URL for this command to work.")
            image_url = ctx.message.attachments[0]
        grab_url = f"{self.grab_url}{image_url}"
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
    async def trigger(self, ctx, member: discord.Member = None):
        one_time_int = "".join([str(random.randint(0, 9)), str(random.randint(0, 9)),
                                str(random.randint(0, 9)), str(random.randint(0, 9))])
        #  random 4 digit int so multiple requests dont overwrite the file
        if member is None:
            member = ctx.author
        grab_url = f"{self.trigger_url}{member.avatar_url}"
        async with ctx.typing():
            binary_data = await aiohttp_assets.aiohttp_get_binary(grab_url)
            with open(f"./storage/trigger{one_time_int}.png", "wb") as writeFile:
                writeFile.write(binary_data)
            file = discord.File(f"./storage/trigger{one_time_int}.png", filename=f"trigger{one_time_int}.png")

            embed = discord.Embed(color=get_color.get_color(ctx.author))
            embed.set_image(url=f"attachment://trigger{one_time_int}.png")
            await ctx.reply(file=file, embed=embed)
        await asyncio.sleep(1)
        os.remove(f"./storage/trigger{one_time_int}.png")

    @commands.command(name="delete", description="Delete a member. Begone, filthy mortal!")
    async def delete_user(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author

        one_time_int = "".join([str(random.randint(0, 9)), str(random.randint(0, 9)),
                                str(random.randint(0, 9)), str(random.randint(0, 9))])
        #  random 4 digit int so multiple requests dont overwrite the file
        dark = random.choice(["true", "false"])
        grab_url = f"{self.delete_url}{user.avatar_url}?darkmode={dark}"
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


def setup(bot):
    bot.add_cog(Attack(bot))
