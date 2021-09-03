import json

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

with open("./spotify_details.json", "r") as spotifyDetails:
    data = json.load(spotifyDetails)
    client_id = data.get("client_id")
    client_secret = data.get("client_secret")

spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id,
                                                                client_secret=client_secret))


def search_artist(search_term: str):
    results = spotify.search(q=f"artist:{search_term}", type="artist")
    items = results['artists']['items']
    if len(items) == 0:
        raise ValueError
    name = items[0].get("name")
    artist_url = items[0].get("external_urls").get("spotify")
    followers = items[0].get("followers").get("total")
    genres = items[0].get("genres")
    genres.sort()
    artist_id = items[0].get("id")
    picture = items[0].get("images")[0].get("url")

    return name, artist_id, artist_url, picture, genres, followers


def artist_results(search_term: str):
    result_dict = {}
    results = spotify.search(q=f"artist:{search_term}", type="artist")
    items = results['artists']['items']
    if len(items) == 0:
        raise ValueError
    for x in range(len(items)):
        name = items[x].get("name")
        artist_url = items[x].get("external_urls").get("spotify")
        result_dict[name] = artist_url
    top_artist = {"name": items[0].get("name"), "url": items[0].get("external_urls").get("spotify"),
                  "picture": items[0].get("images")[0].get("url")}

    return result_dict, top_artist

def get_artist_top_track(artist_id: str):
    artist_top_songs = spotify.artist_top_tracks(artist_id)
    artist_top_songs = artist_top_songs.get("tracks")[0]

    track_name = (artist_top_songs.get("album").get("name"))
    track_url = (artist_top_songs.get("external_urls").get("spotify"))
    return track_name, track_url


def get_artist_tracks(artist_id: str):
    artist_top_songs = spotify.artist_top_tracks(artist_id)
    result_dict = {}
    for x in range(len(artist_top_songs)):
        artist_top_songs = artist_top_songs.get("tracks")[x]

        track_name = (artist_top_songs.get("album").get("name"))
        track_url = (artist_top_songs.get("external_urls").get("spotify"))
        result_dict[track_name] = track_url
    return result_dict


def get_related_artist(artist_id: str):
    artists = spotify.artist_related_artists(artist_id=artist_id)
    return_list = []
    for x in artists.get("artists")[:4]:
        return_list.append({x.get("name"): x.get("external_urls").get("spotify")})

    return return_list
