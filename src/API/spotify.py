import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

class spotify_client:
    def __init__(self, client_id, client_secret, url):
        scope = "playlist-read-private,playlist-read-collaborative,user-library-read"

        self.auth_manager = SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=url,
            scope=scope
        )

        self.sp = spotipy.Spotify(auth_manager=self.auth_manager)

        self.sp2 = spotipy.Spotify(
            auth_manager=SpotifyClientCredentials(
            client_id=client_id,
            client_secret=client_secret,
        ))

        self.user = self.sp.me()