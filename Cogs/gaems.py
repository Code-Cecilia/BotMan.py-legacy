import asyncio
import random

from discord.ext import commands

number_list = ["1", "2", "3", "4", "5", "6", "7", "8", "9", '10']


class Gaems(commands.Cog, description="A collection of games. "
                                      "They _are_ good games, but don't expect something like **Cyberpunk 2077**..."):

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


def setup(bot):
    bot.add_cog(Gaems(bot))
