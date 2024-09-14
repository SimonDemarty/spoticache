# Dependencies ================================================================
import os
import sys
from dotenv import load_dotenv, dotenv_values
import copy
import pickle

import subprocess
import requests

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from pytube import YouTube, Search
import youtube_dl

import track
import album
import music_tag

# Load environment variables ==================================================
load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")

print("SPOTIFY_CLIENT_ID:       %s"%(SPOTIFY_CLIENT_ID))
print("SPOTIFY_CLIENT_SECRET:   %s"%(SPOTIFY_CLIENT_SECRET))
print("SPOTIFY_REDIRECT_URI:    %s"%(SPOTIFY_REDIRECT_URI))

# Initiate Spotify connection =================================================

# cf. https://developer.spotify.com/documentation/web-api/concepts/scopes
scope="playlist-read-private,playlist-read-collaborative,user-library-read"

auth_manager = SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope=scope
)
sp = spotipy.Spotify(auth_manager=auth_manager)
sp2 = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
))

# Get music information from spotify ==========================================

print("Analyzing librairy...")

# Get user
user = sp.me()

# Get all saved tracks
saved_tracks = []

iteration = 0
browse_all_saved_tracks = False
while not browse_all_saved_tracks:

    offset = iteration*20
    results=sp.current_user_saved_tracks(offset=offset)

    for idx, item in enumerate(results['items']):

        my_track = track.track()
        my_track.init_from_playlist(item)
        my_track.display()

        saved_tracks.append(my_track)
        

    iteration += 1
    if len(results['items']) < 20 :
        browse_all_saved_tracks = True

# Get all tracks from saved albums
saved_album_tracks = []
spotify_ids = []

iteration = 0
browse_all_saved_albums = False
while not browse_all_saved_albums:

    offset = iteration*20
    results = sp.current_user_saved_albums(offset=offset)

    # loop over albums
    for idx, item in enumerate(results['items']) :

        # loop over tracks
        musics = item['album']['tracks']['items']
        for music in musics :
            spotify_ids.append(music['id'])        

    iteration += 1
    if len(results['items']) < 20 :
        browse_all_saved_albums = True

# Get right form for musics in albums
for i in range(0, len(spotify_ids), 50) :

    all_tracks = sp2.tracks(spotify_ids[i:i+50])

    for idx, item in enumerate(all_tracks['tracks']) :

        my_track = track.track()
        my_track.init_from_album(item)
        my_track.display()

        saved_album_tracks.append(my_track)

# Get all tracks from playlists
saved_playlist_tracks = []

iteration = 0
browse_all_saved_playlists = False
while not browse_all_saved_playlists:

    offset = iteration*50
    results=sp.current_user_playlists(offset=offset)

    for idx, item in enumerate(results['items']):

        spotify_id = item['id']
        name = item['name']

        iteration_pl = 0
        browse_all_tracks_in_playlist = False
        while not browse_all_tracks_in_playlist :

            offset = iteration_pl*100
            playlist = sp.playlist_tracks(spotify_id, offset=offset)

            for a_track_id, a_track in enumerate(playlist['items']):

                my_track = track.track()
                my_track.init_from_playlist(a_track)
                my_track.display()

                saved_playlist_tracks.append(my_track)

            iteration_pl += 1
            if len(playlist['items']) < 100 :
                browse_all_tracks_in_playlist = True        

    iteration += 1
    if len(results['items']) < 50 :
        browse_all_saved_playlists = True


print("Saved liked tracks:        " + str(len(saved_tracks)))
print("Saved tracks in albums:    " + str(len(saved_album_tracks)))
print("Saved tracks in playlists: " + str(len(saved_playlist_tracks)))

print("Library analyzed.")

# Organize Library ============================================================

print("Removing doubles...")

# Add everything to same array and remove doubles
all_tracks = saved_album_tracks # Start wuth albums tracks

# Remove doubles
tracks2add = saved_tracks
tracks2add.extend(saved_playlist_tracks)
for track2add in tracks2add:
    
    already_in = False
    for track in all_tracks :
        if track2add.spotify_id == track.spotify_id :
            already_in = True
            break

    if not already_in :
        all_tracks.append(track2add)

print("Saved tracks w/o doubles:  " + str(len(all_tracks)))
print("Doubles removed.")

# Create albums
print("Creating albums...")

all_albums = []
for track in all_tracks:

    # Album never encountered
    album_idx = album.album_idx(all_albums, track.album_id)

    # Album never encountered
    if album_idx == -1 :
        my_album = album.album(
            spotify_id = track.album_id,
            name = track.album_name,
            artists = track.album_artists_name,
            image = track.album_image,
            release_date = track.album_release_date
        )
    # Album already exists
    else :
        my_album = all_albums.pop(album_idx)

    # add music to album, and place album in index 0 for performance
    my_album.add_track(track)
    all_albums.insert(0, my_album)

print("Albums created.")

# Load previous pickes
# print("loading previous pickes...")

# with open('all_albums.pickle', 'rb') as handle :
#     all_albums_previous = pickle.load(handle)

# with open('all_tracks.pickle', 'rb') as handle :
#     all_tracks_previous = pickle.load(handle)

print("Previous pickle loaded.")

# Fixing difference
print("Fixing differences...")

# TODO:

print("Differences fixed.")

# Store all information in pickle =============================================
print("Storing data in pickles...")

with open('all_albums.pickle', 'wb') as handle:
    pickle.dump(all_albums, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open('all_tracks.pickle', 'wb') as handle :
    pickle.dump(all_tracks, handle, protocol=pickle.HIGHEST_PROTOCOL)

print("Data stored.")

# Download musics that are not already downloaded =============================
print("Downloading...")

output_folder = os.path.join(sys.argv[1], "spoticache")

if not os.path.isdir(output_folder) :
    os.mkdir(output_folder)

for album_nb, album in enumerate(all_albums):

    print("album: " + str(album_nb) + "/" + str(len(all_albums)))

    album_path = os.path.join(output_folder, ", ".join(album.artists).replace("/", "|") + "/" + album.name.replace("/", "|"))
    
    if not os.path.isdir(album_path) :
        os.makedirs(album_path)

        img_data = requests.get(album.image).content
        with open(os.path.join(album_path,'thumbnail.jpg'), 'wb') as handler:
            handler.write(img_data)

    for track in album.tracklist :

        # perform search
        search_string = track.name + " " + " ".join(track.artists_names)
        search = Search(search_string)
        
        # choix ytaudio
        # TODO: choose more accurately
        audio = search.results[0]
        
        # create yt object
        audio_url = audio.watch_url
        audio_ytid = audio_url.split("=")[1]
        # print(audio_ytid)
        #  yt-dlp -q -o wit -f ba izGwDsrQ1eQ
        

        # actually dl
        try:

            # dl
            subprocess.run([
                "yt-dlp",
                "-q",
                "-o", os.path.join(album_path, (track.name).replace("/", "|")) + "",
                "-f",
                "ba",
                audio_ytid
            ])

            # convert audio and encode
            subprocess.run([
                "ffmpeg",
                "-i", os.path.join(album_path, (track.name).replace("/", "|")) + "",
                "-q:a", "0",
                "-map", "0:a",
                os.path.join(album_path, (track.name).replace("/", "|")) + ".mp3"
            ])

            # delete video
            subprocess.run([
                "rm", os.path.join(album_path, (track.name).replace("/", "|")) + ""
            ])

            # add metadata:
            file = music_tag.load_file(os.path.join(album_path, (track.name).replace("/", "|")) + ".mp3")
            file['tracktitle'] = track.name
            file['album'] = track.album_name
            file['albumartist'] = ", ".join(track.album_artists_name)
            file['artist'] = ", ".join(track.artists_names)
            file['discnumber'] = int(track.disc_number)
            file['tracknumber'] = int(track.track_number)
            file['isrc'] = track.isrc
            file['artwork'] = img_data

            file.save()

        except Exception as e:
            print(e)

print("Downloaded.")