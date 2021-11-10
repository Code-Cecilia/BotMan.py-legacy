import json

import discord
import spotipy
from discord.ext import commands
from spotipy.oauth2 import SpotifyClientCredentials

from assets import get_color, spotify_search


class Spotify(commands.Cog, description="A category for viewing information related to Spotify. This **IS NOT** used"
                                        " for playing music."):
    def __init__(self, bot):
        self.bot = bot
        with open("./spotify_details.json", "r") as spotifyDetails:
            data = json.load(spotifyDetails)
            self.client_id = data.get("client_id")
            self.client_secret = data.get("client_secret")
            self.spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=self.client_id,
                                                                                 client_secret=self.client_secret))

    @commands.command(name="artist", aliases=["spotifyartist"], description="Gives information on an artist.")
    async def spotify_artist(self, ctx, *, search_term: commands.clean_content):
        try:
            name, artist_id, artist_url, picture, genres, followers = spotify_search.search_artist(str(search_term))
        except ValueError:
            return await ctx.send(f"Oops! Looks like **{search_term}** doesn't exist in Spotify's database!")
        embed = discord.Embed(title=f"Found artist - {name}", color=get_color.get_color(ctx.author))
        embed.description = "__**Genres**__\n" + ", ".join(genres)
        embed.add_field(name="Spotify URL", value=f"__[Link]({artist_url})__", inline=True)
        embed.add_field(name="Followers", value=followers, inline=True)
        embed.set_thumbnail(url=picture)
        embed.set_footer(text=f"Artist ID - {artist_id}")

        track_name, track_url = spotify_search.get_artist_top_track(artist_id)
        embed.add_field(name="Artist's top track/album", value=f"__[{track_name}]({track_url})__", inline=False)
        related_list = spotify_search.get_related_artist(artist_id)
        related_string = ""
        for x in range(len(related_list) - 1):
            name = list(related_list[x].keys())[0]
            url = list(related_list[x].values())[0]
            related_string += f", __[{name}]({url})__"
        if not related_string == "":
            embed.add_field(name="Related Artists", value=related_string[1:], inline=False)
        await ctx.send(embed=embed)

    @commands.command(name="spotifycategories")
    async def spotify_categories(self, ctx, country_code: commands.clean_content = None):
        category_list = self.spotify.categories(country=country_code)
        list_tobe_iterated = (category_list.get("categories").get("items"))
        embed = discord.Embed(title="Top 25 Categories",
                              color=get_color.get_color(ctx.author))
        for x in list_tobe_iterated:
            embed.add_field(name=x.get("name"), value=f"__[Link To Logo]({x.get('icons')[0].get('url')})__",
                            inline=False)
        embed.set_thumbnail(url=list_tobe_iterated[0].get('icons')[0].get('url'))
        await ctx.send(embed=embed)

    @commands.command(name="toptrack", aliases=["toptracks"],
                      description="Get's an artist's top track(s) from the Spotify database.")
    async def top_tracks(self, ctx, *, artist_name: str):
        try:
            name, artist_id, artist_url, picture, genres, followers = spotify_search.search_artist(str(artist_name))
        except ValueError:
            return await ctx.send(f"Oops! Looks like **{artist_name}** doesn't exist in Spotify's database!")
        top_tracks = spotify_search.get_artist_tracks(artist_id)
        embed = discord.Embed(title=f"Top track(s) of {name}", color=get_color.get_color(ctx.author))
        embed.set_thumbnail(url=picture)
        description_text = ""
        for key, value in top_tracks.items():
            description_text += f"\n__[{key}]({value})__"
        embed.description = description_text
        embed.add_field(name="Artist URL", value=f"__[Link]({artist_url})__", inline=False)
        embed.set_footer(text=f"Artist ID: {artist_id}")
        await ctx.send(embed=embed)

    @commands.command(name="artistsearch", aliases=["searchartist"],
                      description="Returns search results for an artist name")
    async def artist_search(self, ctx, *, artist_name):
        """Returns information about a Spotify artist. This is not a music player command."""
        try:
            result_dict, top_artist = spotify_search.artist_results(artist_name)
        except ValueError:  # raise ValueError implemented in the function
            return await ctx.send(f"Uh-oh! Looks like **{artist_name}** doesn't exist in Spotify's database!")
        top_result_text = f"Top Result: __[{top_artist.get('name')}]({top_artist.get('url')})__"
        embed = discord.Embed(title=f"Results for {artist_name}", description=top_result_text,
                              color=get_color.get_color(ctx.author))

        result_text = ""
        n = 0  # count number of artists
        for name, url in result_dict.items():
            if n >= 10:  # dont include more than 20 results
                break
            result_text += f"\n__[{name}]({url})__"
            n += 1
        embed.add_field(name="All Results", value=result_text, inline=False)
        embed.set_thumbnail(url=top_artist.get("picture"))
        await ctx.send(embed=embed)

    @commands.command(name="album")
    async def album_info(self, ctx, *, search_term: commands.clean_content):
        """Returns information about a Spotify album. This is not a music player command."""
        try:
            album_name, album_url, album_id, artist_dict, \
                total_tracks, release_date, markets, thumbnail = spotify_search.search_album(str(search_term))
        except ValueError:
            return await ctx.send(f"Uh-oh! Looks like **{search_term}** isn't a valid album!")
        artists = "**Artists**\n"
        for name, url in artist_dict.items():
            artists += f"__[{name}]({url})__, "
        artists = artists[:-2]  # remove last comma
        embed = discord.Embed(title=f"Found Album - {album_name}", description=artists,
                              color=get_color.get_color(ctx.author))
        embed.add_field(name="Album URL", value=f"__[Link]({album_url})__", inline=True)
        embed.add_field(name="Release Date", value=release_date, inline=True)
        embed.add_field(name="Total Tracks", value=total_tracks, inline=True)
        embed.add_field(name="Availability", value=f"{markets} {'countries' if int(markets) != 1 else 'country'}", inline=True)
        embed.set_footer(text=f"Album ID: {album_id}")
        embed.set_thumbnail(url=thumbnail)
        await ctx.send(embed=embed)

    @commands.command(name="track", aliases=["trackinfo"])
    async def track_info(self, ctx, *, search_term: commands.clean_content):
        """Returns information about a Spotify track. This is not a music player command."""
        try:
            track_name, track_url, track_id, artist_dict, \
            thumbnail, release_date, markets = spotify_search.search_track(str(search_term))
        except ValueError:
            return await ctx.send(f"Uh-oh! Looks like **{search_term}** isn't a valid track!")
        artists = "**Artists**\n"
        for name, url in artist_dict.items():
            artists += f"__[{name}]({url})__, "
        artists = artists[:-2]  # remove last comma
        embed = discord.Embed(title=f"Found Track - {track_name}", description=artists,
                              color=get_color.get_color(ctx.author))
        embed.add_field(name="Track URL", value=f"__[Link]({track_url})__", inline=True)
        embed.add_field(name="Release Date", value=release_date, inline=True)
        embed.add_field(name="Availability", value=f"{markets} {'countries' if int(markets) != 1 else 'country'}",
                        inline=True)
        embed.set_footer(text=f"Track ID: {track_id}")
        print(thumbnail)
        embed.set_thumbnail(url=thumbnail)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Spotify(bot))
