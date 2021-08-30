import asyncio
import random

import discord


def get_otp(digits=4):
    otp = ""
    for x in range(digits):
        otp += random.randint(0, 9)
    return otp


async def send_waitfor_otp(ctx, bot):
    final_otp = get_otp()
    embed = discord.Embed(title=f"{ctx.author.display_name}, please enter the OTP given below to confirm this action.",
                          description=f"**{final_otp}**", color=ctx.author.color)
    embed.set_footer(text="Timeout: 15 seconds")
    await ctx.send(embed=embed)
    try:
        message_otp = await bot.wait_for("message", check=lambda message: message.author == ctx.author,
                                         timeout=15)
        if str(message_otp.content) == final_otp:
            await message_otp.add_reaction("✅")
            return True
        else:
            await ctx.send("Incorrect OTP - Aborting...")
    except asyncio.TimeoutError:
        await ctx.send("Timed out - Aborting...")
        return False
