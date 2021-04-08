import requests
from pprint import pprint
import csv

# import csv
# import json
# from datetime import datetime
# import datetime
# import sqlite3
DATABASE_LOCATION = "sqlite:///my_played_tracks.sqlite"
USER_ID = input('Write User ID to see playlists: ').lower()
# your Spotify username
TOKEN = "BQBs83dKJPDDb15CHCiduTTHE1Xn3ZVwzWPMYGr09SNtf8Vrp1QSXTnEv_nHJMA9wvovcCZekk5aeFW0ryyRIOnjJAyxDZj8in2GAA9HurX0-0xlVqT5M29NlA--aNiSLFSYl-4kmQ6Pi9-gWqHgox_DNuy8IjRwTnWq6EKM0LhaIokW2SArDclF9tH8Dmooq_C2URcSkZFx3iY4N_SIjdejKJ08UHCRNtTXf6Hv7-QvahGDWLL83er5RgJ3l5shXKTFjlmZPxqtfOIRER20-9y77Q"


# Generate your token here: https://developer.spotify.com/console/get-playlists/
# Spotify Account can be created here: https://www.spotify.com/uk/home/
def spotify():
    # Extract part of the ETL process
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(TOKEN)
    }
    # Download all playlists saved by user
    r = requests.get("https://api.spotify.com/v1/users/{user_id}/playlists".format(user_id=USER_ID), headers=headers)
    data = r.json()  # dictionary and list in javascript
    # Writing data with PrettyPrint format to spotify.txt
    with open('spotify.txt', 'wt', encoding='utf-8') as out:
        pprint(data, stream=out)
    # Extracting relevant data: playlist name and playlist URI to get the Playlist ID needed for getting tracks in playlist later
    # E.g. 'uri': 'spotify:playlist:1KEfw7XdJUylTHgeqWEw67' --> playlist ID: 1KEfw7XdJUylTHgeqWEw67
    playlist_names = []
    playlist_uri = []
    for playlist in data['items']:
        playlist_names.append(playlist['name'])
        playlist_uri.append(playlist['uri'])
    pprint(playlist_names)
    # pprint(playlist_uri)
    # Extracting playlist ID from playlist URI
    playlist_id = []
    for uri in playlist_uri:
        playlist_id.append(uri[17:49])
    # pprint(playlist_id)
    # Creating dictionary to store playlist name and corresponding playlist ID
    playlist_dict = {}
    for key in playlist_names:
        for value in playlist_id:
            playlist_dict[key] = value
            playlist_id.remove(value)
            break
    # print(playlist_dict)
    # Ask user which playlist's items they want to see
    which_playlist = input('Choose a playlist to see its songs (case sensitive): ')
    chosen_playlist = playlist_dict[which_playlist]
    # print(chosen_playlist)
    # Request data for playlist items i.e. songs/tracks
    response = requests.get(
        'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'.format(playlist_id=chosen_playlist),
        headers=headers)
    playlist_items = response.json()  # dictionary and list in javascript
    # pprint(playlist_items)
    # Writing playlist_items data with PrettyPrint format to playlist_songs.txt
    with open('playlist_songs.txt', 'wt', encoding='utf-8') as out:
        pprint(playlist_items, stream=out)
    playlist_items_length = len(playlist_items)
    print(playlist_items_length)
    # pprint(playlist_items['items'][0]['track']['album']['artists'][0]['name'])
    artist = []
    album = []
    track = []
    for song in playlist_items['items']:
        artist.append(song['track']['album']['artists'][0]['name'])
        album.append(song['track']['album']['name'])
        track.append(song['track']['name'])
    # pprint(artist)
    # pprint(album)
    # pprint(track)
    song_list = [{'Song': sng, 'Artist': art, 'Album': alb} for sng, art, alb in zip(track, artist, album)]
    print(song_list)
    keys = song_list[0].keys()
    with open('songs_in_playlist.csv', 'w+', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(song_list)


spotify()
