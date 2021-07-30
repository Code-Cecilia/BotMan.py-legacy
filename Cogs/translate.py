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
        self.lang_list = list(googletrans.LANGUAGES.keys())

    @commands.command(name='translate', aliases=['tr'], description='Translate from one language to the other.\n'
                                                                    'Usage: `bm-translate Hola es en` --> '
                                                                    'translates from spanish to english\n'
                                                                    '`bm-translate Hola en` --> '
                                                                    'translates by detecting the language')
    async def translate(self, ctx, *, text):
        split_text = text.split()
        src_lang = split_text[-2].lower()
        dest_lang = split_text[-1].lower()

        if str(src_lang) in self.lang_list:
            has_src = True
        else:
            has_src = False

        if dest_lang not in self.lang_list:
            return await ctx.send(f"Could not find destination language `{dest_lang}`. "
                                  f"Use the `langcodes` command for a list of language codes.")

        split_text.pop(-1)  # remove destination lang
        if has_src:  # remove source lang if exists
            split_text.pop(-1)

        to_translate = " ".join(split_text)

        if has_src:
            result = self.translator.translate(
                to_translate, src=src_lang, dest=dest_lang)
        else:
            result = self.translator.translate(to_translate, dest=dest_lang)

        from_lang = str(self.lang_dict.get(str(result.src).lower())).title()
        # language name from language code ("es" would be "Spanish")
        to_lang = str(self.lang_dict.get(str(result.dest)).lower()).title()
        final_string = f"{from_lang} --> {to_lang}"

        embed = discord.Embed(
            title=f"{ctx.author.display_name}, your translation is:", color=discord.Color.random())
        embed.description = result.text
        embed.set_footer(text=f"{final_string} | Requested by {ctx.author}")
        await ctx.send(embed=embed)

    @commands.command(name='langcodes', aliases=['languagecodes', 'listlanguagecodes', 'listlangcodes'],
                      description='List the language codes for use in the translate command.')
    async def get_lang_codes(self, ctx):
        chunk_list = list(list_funcs.chunks(
            list(self.lang_code_dict.keys()), 25))
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

    @commands.command(name="detectlang", aliases=['detect', 'findlang'],
                      description="Detects the language from a sentence given as argument.")
    async def detect_lang(self, ctx, *, sentence):
        result = self.translator.detect(sentence)
        confidence = (round(result.confidence * 100))
        lang_name = self.lang_dict.get(result.lang).title()

        embed = discord.Embed(title=f'Detected language! - {lang_name}', description=f"Text entered: **{sentence}**",
                              color=discord.Color.random())
        embed.set_footer(text=f"Confidence: {confidence}%")

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Translate(bot))
