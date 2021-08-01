import ast
import datetime

import aiohttp
import discord
from discord.ext import commands

from assets import time_calc


class CoronaTracking(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="coronastats", aliases=["covidstats"], description="Status of the Corona virus worldwide")
    async def corona_stats(self, ctx):
        track_url = "https://disease.sh/v3/covid-19/all"
        async with aiohttp.ClientSession() as session:
            async with session.get(track_url) as response:
                response_dict = (await response.content.read()).decode('utf-8')
        response_dict = ast.literal_eval(response_dict)
        time_unix = response_dict.get("updated") / 1000
        time_utcformat = datetime.datetime.utcfromtimestamp(time_unix)

        updated_date, updated_time = time_calc.parse_utc(str(time_utcformat))
        total_cases = response_dict.get("cases")
        today_cases = response_dict.get("todayCases")
        total_deaths = response_dict.get("deaths")
        today_deaths = response_dict.get("todayDeaths")
        total_recovered = response_dict.get("recovered")
        today_recovered = response_dict.get("todayRecovered")
        active_cases = response_dict.get("active")
        critical_cases = response_dict.get("critical")
        cases_per_million = response_dict.get("casesPerOneMillion")
        deaths_per_million = response_dict.get("deathsPerOneMillion")
        total_tests = response_dict.get("tests")
        world_population = response_dict.get("population")
        active_per_million = response_dict.get("activePerOneMillion")
        recovered_per_million = response_dict.get("recoveredPerOneMillion")
        critical_per_million = response_dict.get("criticalPerOneMillion")
        affected_countries = response_dict.get("affectedCountries")

        embed = discord.Embed(title="Covid-19 Stats Worldwide",
                              description=f"Updated **{updated_date}** at **{updated_time} UTC+0**",
                              color=discord.Color.dark_red())
        embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/8/82/SARS-CoV-2_without_background.png")
        embed.add_field(name="Total cases", value=total_cases, inline=True)
        embed.add_field(name="New Cases Today", value=today_cases, inline=True)
        embed.add_field(name="Cases per Million", value=cases_per_million, inline=True)

        embed.add_field(name="Total Deaths", value=total_deaths, inline=True)
        embed.add_field(name="Deaths Today", value=today_deaths, inline=True)
        embed.add_field(name="Deaths per Million", value=deaths_per_million, inline=True)

        embed.add_field(name="Active cases", value=active_cases, inline=True)
        embed.add_field(name="Active per Million", value=active_per_million, inline=True)

        embed.add_field(name="Critical Cases", value=critical_cases, inline=True)
        embed.add_field(name="Critical per Million", value=critical_per_million, inline=True)

        embed.add_field(name="Recovered", value=total_recovered, inline=True)
        embed.add_field(name="Recovered Today", value=today_recovered, inline=True)
        embed.add_field(name="Recovered per Million", value=recovered_per_million, inline=True)

        embed.add_field(name="Total Tests", value=total_tests, inline=True)

        embed.add_field(name="World Population", value=world_population, inline=True)
        
        embed.set_footer(text=f"Powered by disease.sh")

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(CoronaTracking(bot))
