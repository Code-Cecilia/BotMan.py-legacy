import asyncio
import json
import random

import aiohttp
import discord
from discord.ext import commands

from assets import get_color, random_assets

number_list = ["1", "2", "3", "4", "5", "6", "7", "8", "9", '10']


class Gaems(commands.Cog, description="A collection of gaems. "
                                      f"They _are_ good games, but don't expect something like "
                                      f"**{random.choice(random_assets.good_games)}**...\n"
                                      f"Play gaem, life good."):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="guessthenumber", aliases=["luckychoice", "numberfinder"],
                      description="Play games, have fun. It's a simple life.")
    async def guess_the_number(self, ctx):
        number = random.choice(number_list)
        await ctx.send(f"Welcome to **Guess The Number**, _{ctx.author.display_name}_!\n"
                       f"The rules are simple.\n"
                       f"I will think of a number from 1 to 10, and you have to find it within 3 tries.\n"
                       f"The game starts in 3 seconds.")
        await asyncio.sleep(3)

        await ctx.send("Go!")

        n = 3
        win = False

        while n > 0:
            try:
                user_input = await self.bot.wait_for("message", timeout=10,
                                                     check=lambda message: message.author == ctx.author)

                print(user_input.content)
                print(type(user_input.content))
                if user_input.content not in number_list:
                    await ctx.send(f"_{ctx.author.display_name}_, Not a valid guess! "
                                   f"You need to choose a number from 1 to 10.")
                    break
                if str(user_input.content) == number:
                    await user_input.add_reaction("🎉".strip())
                    await ctx.send(f"You won!, _{ctx.author.display_name}_!")
                    win = True
                    break
                n -= 1
                await ctx.send(f"_{ctx.author.display_name}_, Wrong! You have {n} tries left.")

            except asyncio.exceptions.TimeoutError:
                return await ctx.send(f"_{ctx.author.display_name}_, I'm done waiting. We'll play again later.")
        if not win:
            await ctx.reply(f"The correct answer is {number}.")
        await ctx.send(f"Thanks for playing **Guess The Number**!")

    @commands.command(name="trivia", aliases=["quiz"], description="The bot asks a question, you answer. Simple.")
    async def trivia(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://opentdb.com/api.php?amount=1") as x:
                response = (await x.content.read()).decode("utf-8")
                response = json.loads(response)

        if not response.get("response_code") == 0:
            return

        results = response.get("results")[0]
        category = results.get("category").replace(
            "&quot;", "\"").replace("&#039;", "'")
        difficulty = results.get("difficulty").replace(
            "&quot;", "\"").replace("&#039;", "'")
        question = results.get("question").replace(
            "&quot;", "\"").replace("&#039;", "'")
        correctans = results.get("correct_answer").replace(
            "&quot;", "\"").replace("&#039;", "'")
        wrong_ans_list = results.get("incorrect_answers")
        answers = wrong_ans_list
        answers.append(correctans)

        random.shuffle(answers)
        correctans_index = list(answers).index(correctans) + 1

        message_to_edit = await ctx.send("The rules are simple. I will ask you a question, you choose the answer.\n"
                                         "If there are 4 options in the answer, "
                                         "you can enter \"1\", \"2\", \"3\", or \"4\".\n"
                                         "The game starts in 5 seconds.")
        await asyncio.sleep(5)
        await message_to_edit.edit(content=f"_{ctx.author.display_name}_, go!")
        embed = discord.Embed(title=f"Category: {category}\nDifficulty: {difficulty}",
                              color=get_color.get_color(ctx.author))
        embed.add_field(name=question, value="\ufeff", inline=False)

        option_string = ""
        for x in answers:
            option_str = x.replace("&quot;", "\"").replace("&#039;", "'")
            option_string += f"`{answers.index(x) + 1}.` {option_str}\n"

        embed.add_field(name="Options", value=option_string, inline=True)
        embed.set_footer(
            text=f"{ctx.author.display_name}, pick the answer! You have 10 seconds.")
        await ctx.send(embed=embed)
        try:
            message_from_user = await self.bot.wait_for("message", check=lambda message: message.author == ctx.author,
                                                        timeout=10)
        except asyncio.TimeoutError:
            return await ctx.send(f"_{ctx.author.display_name}_, I'm done waiting. We'll play again later.\n"
                                  f"The answer was **{correctans}**")

        try:
            content = int(message_from_user.content)
        except ValueError:
            content = ""
            return await ctx.send(f"_{ctx.author.display_name}_ , wrong format!\n"
                                  "You can only answer with the Index of the option you think is correct.\n"
                                  "We'll play later.")
        if content == correctans_index:
            await message_from_user.add_reaction("🎉")
            await message_from_user.reply("You won!")
        else:
            await message_from_user.add_reaction("❌")
            await message_from_user.reply(f"_{ctx.author.display_name}_, good try, "
                                          f"but that was not the correct answer.\n"
                                          f"The correct answer is **{correctans}**.")
        await ctx.send(f"Thanks for playing **Trivia**, _{ctx.author.display_name}_!")


def setup(bot):
    bot.add_cog(Gaems(bot))
