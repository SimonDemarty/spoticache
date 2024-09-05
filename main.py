# Dependencies ================================================================
import os
from dotenv import load_dotenv, dotenv_values
import copy
import pickle

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

import track

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

# Organize Library ============================================================

# Make sure albums are created

# Store all information in pickle =============================================

# Download musics that are not already downloaded =============================