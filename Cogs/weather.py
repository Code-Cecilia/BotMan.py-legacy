import json

import discord
from discord.ext import commands

from assets import get_color, aiohttp_assets


def get_time_info(user_id: int):
    with open("./storage/time_files/time_tz.json") as timeFile:
        data = json.load(timeFile)
        timezone = data.get(str(user_id))
        return timezone


def get_embed_from_weather_dict(result: dict):
    longitude = result.get("coord").get('lon')
    latitude = result.get("coord").get('lat')

    weather = result.get("weather")[0].get("main")
    icon = result.get("weather")[0].get("icon")
    actual_temp = int(result.get("main").get("temp") - 273.15)
    feels_like = int(result.get("main").get("feels_like") - 273.15)
    temp_min, temp_max = int(result.get("main").get("temp_min") - 273.15), \
                         int(result.get("main").get("temp_max") - 273.15)
    humidity = result.get("main").get("humidity")

    country_code = result.get("sys").get("country")
    name = result.get("name")

    return name, latitude, longitude, icon, weather, actual_temp, feels_like, temp_min, temp_max, humidity, country_code


class Weather(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

        with open("config.json", "r") as configFile:
            data = json.load(configFile)
            self.apikey = data.get("weather_api_key")
            self.weather_url = "https://api.openweathermap.org/data/2.5/weather?q={cityName}&appid={apiKey}"
            self.weather_icon_url = "https://openweathermap.org/img/wn/{code}@2x.png"
        with open("./storage/weather.json", "r") as weatherFile:
            self.weatherData = json.load(weatherFile)

        if self.apikey is None:
            raise ValueError  # stop the cog from loading

    @commands.command(name="weather", aliases=["temperature"],
                      description="Get the weather information for your location or another member")
    async def weather_user(self, ctx, *, user: discord.Member = None):
        gotten_from_tz = False
        if user is None:
            user = ctx.author
        weather_zone = self.weatherData.get(str(user.id))
        if weather_zone is None:
            weather_zone = str(get_time_info(user.id)).split("/")
            if len(weather_zone) == 1:
                return await ctx.send("It seems you have not set your region. "
                                      "You can set your region using the `setweatherlocation` command.")
            weather_zone = weather_zone[-1]
            gotten_from_tz = True
        result = await aiohttp_assets.aiohttp_get(
            url=self.weather_url.format(cityName=weather_zone, apiKey=self.apikey))
        result = json.loads(result)
        if str(result.get("cod")) == "404":
            return await ctx.send("The city was not found. "
                                  "Please update your city using the `setweatherlocation` command")
        name, latitude, longitude, icon, weather, \
            actual_temp, feels_like, temp_min, temp_max, \
            humidity, country_code = get_embed_from_weather_dict(result)

        embed = discord.Embed(title=f"{name}, where {user.display_name} is",
                              description=f"{longitude}_N_, {latitude}_E_",
                              color=get_color.get_color(user))
        embed.add_field(name="Weather", value=weather, inline=True)
        embed.add_field(name="Temperature", value=f"Actual: **{actual_temp}°C**\n"
                                                  f"Feels Like: **{feels_like}°C**", inline=True)
        embed.add_field(name="Min/Max", value=f"Min: **{temp_min}°C**\n"
                                              f"Max: **{temp_max}°C**", inline=True)
        embed.add_field(name="Humidity", value=f"{humidity}%", inline=True)
        embed.add_field(name="Country Code", value=country_code)
        if icon:
            embed.set_thumbnail(url=self.weather_icon_url.format(code=icon))
        if gotten_from_tz:
            embed.set_footer(text="Location fetched from user's timezone info")
        await ctx.send(embed=embed)

    @commands.command(name="setweatherlocation", aliases=["weatherlocation"],
                      description="Sets the location to use for weather info")
    async def set_weather_location(self, ctx, location):
        message = await ctx.send(f"Checking if **{location}** is a valid location...")
        result = await aiohttp_assets.aiohttp_get(self.weather_url.format(cityName=location, apiKey=self.apikey))
        result = (json.loads(result))
        if result.get("message") is not None:
            return await message.edit(content=f"The API I use encounted an error : **{result.get('message')}**")
        self.weatherData[str(ctx.author.id)] = result.get("name")
        with open("./storage/weather.json", "w") as writeFile:
            json.dump(self.weatherData, writeFile)
        await message.edit(content=f"Location set to **{result.get('name')}** successfully!")

    @commands.command(name="locationweather", aliases=["lweather", "weatherl"],
                      description="Gets weather information for a specific city.")
    async def weather_from_city(self, ctx, city):
        message = await ctx.send(f"Gathering weather info for **{city}**...")
        result = await aiohttp_assets.aiohttp_get(url=self.weather_url.format(cityName=city, apiKey=self.apikey))
        result = json.loads(result)
        if result.get("message") is not None:
            return await message.edit(content=f"The API I use encountered an error: **{result.get('message')}**")
        name, latitude, longitude, icon, weather, \
            actual_temp, feels_like, temp_min, temp_max, \
            humidity, country_code = get_embed_from_weather_dict(result)

        embed = discord.Embed(title=f"{name}'s weather info",
                              description=f"{longitude}_N_, {latitude}_E_",
                              color=get_color.get_color(ctx.author))
        embed.add_field(name="Weather", value=weather, inline=True)
        embed.add_field(name="Temperature", value=f"Actual: **{actual_temp}°C**\n"
                                                  f"Feels Like: **{feels_like}°C**", inline=True)
        embed.add_field(name="Min/Max", value=f"Min: **{temp_min}°C**\n"
                                              f"Max: **{temp_max}°C**", inline=True)
        embed.add_field(name="Humidity", value=f"{humidity}%", inline=True)
        embed.add_field(name="Country Code", value=country_code)
        if icon:
            embed.set_thumbnail(url=self.weather_icon_url.format(code=icon))
        await message.edit(embed=embed, content=None)


def setup(bot):
    bot.add_cog(Weather(bot))
