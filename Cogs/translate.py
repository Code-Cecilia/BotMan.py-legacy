import asyncio

import discord
from discord.ext import commands
import googletrans
from googletrans import Translator

from assets import list_funcs


class Translate(commands.Cog, description='A set of commands that uses the google translate API'):

    def __init__(self, bot):
        self.bot = bot
        self.translator = Translator()
        self.lang_dict = googletrans.LANGUAGES
        self.lang_code_dict = googletrans.LANGCODES

    @commands.command(name='translate', aliases=['tr'], description='Translate from one language to the other.\n'
                                                                    'Usage: `bm-translate Hola es en` --> '
                                                                    'translates from spanish to english\n'
                                                                    '`bm-translate Hola en` --> '
                                                                    'translates by detecting the language')
    async def translate(self, ctx, *, text):
        split_text = text.split(' ')
        dest_lang = split_text[-1]
        src_lang = split_text[-2]
        if len(src_lang) != 2:
            src_lang = None

        if src_lang is not None:
            split_text.pop(-1)  # removing the to_language entry
            split_text.pop(-1)  # removing the from_language entry
            to_translate = " ".join(split_text)
            try:
                result = self.translator.translate(to_translate, src=src_lang, dest=dest_lang)
            except ValueError:
                return await ctx.send('Improper format. Check the help command for the correct format(s).')
        else:
            split_text.pop(-1)
            to_translate = " ".join(split_text)
            try:
                result = self.translator.translate(to_translate, dest=dest_lang)
            except ValueError:
                return await ctx.send('Improper format. Check the help command for the correct format(s).')
        from_lang = str(self.lang_dict.get(result.src)).title()
        dest_lang = str(self.lang_dict.get(result.dest)).title()
        final_string = f"{from_lang} --> {dest_lang}"

        embed = discord.Embed(title=f"{ctx.author.display_name}, your translation is:", color=discord.Color.random())
        embed.description = result.text
        embed.set_footer(text=f"{final_string} | Powered by Google Translate")
        await ctx.send(embed=embed)

    @commands.command(name='langcodes', aliases=['languagecodes', 'listlanguagecodes', 'listlangcodes'],
                      description='List the language codes for use in the translate command.')
    async def get_lang_codes(self, ctx):
        chunk_list = list(list_funcs.chunks(list(self.lang_code_dict.keys()), 27))
        try:
            await ctx.author.send("List of language codes")
            await ctx.message.add_reaction("📭")
        except:
            return await ctx.reply('Could not send message to you. Please enable PMs and try again.')
        n = 0
        for top_list in chunk_list:
            string = ""
            for x in top_list:
                value = self.lang_code_dict.get(x)
                string += f"\n{x} - {value}"
                n += 1
            await asyncio.sleep(1)
            await ctx.author.send(string)
        await ctx.author.send(f'Total: {n} entries.')

    @commands.command(name="detectlang", description="Detects the language from a sentence given as argument.")
    async def detect_lang(self, ctx, *, sentence):
        result = self.translator.detect(sentence)
        confidence = (round(result.confidence * 100))
        lang_name = self.lang_dict.get(result.lang).title()

        embed = discord.Embed(title=f'Detected language! - {lang_name}', description=f"Text: **{sentence}**",
                              color=discord.Color.random())
        embed.set_footer(text=f"Confidence: {confidence}%")

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Translate(bot))
