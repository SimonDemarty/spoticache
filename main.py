# Dependencies ================================================================
import os
from dotenv import load_dotenv, dotenv_values
import copy

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


# Actual code =================================================================

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

        my_track = track.track(item)
        my_track.display()

        saved_tracks.append(my_track)
        

    iteration += 1
    if len(results['items']) < 20 :
        browse_all_saved_tracks = True
