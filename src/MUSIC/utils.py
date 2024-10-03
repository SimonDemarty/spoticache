# Packages Dependencies ========================================================

import os
from dotenv import load_dotenv

import logging
from src.API import spotify

# Initialisation ===============================================================

load_dotenv()
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")

# Actual classes ===============================================================

class track:
    def __init__(self):
        pass

    def init_from_playlist(self, spotify_track):

        self.spotify_JSON = spotify_track

        # Track information
        self.spotify_id = spotify_track['track']['id']

        self.isrc = spotify_track['track']['external_ids']['isrc'] if 'isrc' in spotify_track['track']['external_ids'] else None

        self.name = spotify_track['track']['name']

        self.duration = spotify_track['track']['duration_ms']

        self.artists_spotify_ids = [artist['id'] for artist in spotify_track['track']['artists']]
        self.artists_names = [artist['name'] for artist in spotify_track['track']['artists']]


        # Album information
        self.album_id = spotify_track['track']['album']['id']

        self.album_type = spotify_track['track']['album']['album_type']
        self.album_type2 = spotify_track['track']['album']['type']

        self.album_name = spotify_track['track']['album']['name']
        self.album_release_date = spotify_track['track']['album']['release_date']
        self.album_image = spotify_track['track']['album']['images'][0]['url']

        self.disc_number = spotify_track['track']['disc_number']
        self.track_number = spotify_track['track']['track_number']

        self.album_artists_spotify_ids = [artist['id'] for artist in spotify_track['track']['album']['artists']]
        self.album_artists_name = [artist['name'] for artist in spotify_track['track']['album']['artists']]

    def init_from_album(self, spotify_track):

        self.spotify_JSON = spotify_track

        # Track information
        self.spotify_id = spotify_track['id']

        self.isrc = spotify_track['external_ids']['isrc'] if 'isrc' in spotify_track['external_ids'] else None

        self.name = spotify_track['name']

        self.duration = spotify_track['duration_ms']

        self.artists_spotify_ids = [artist['id'] for artist in spotify_track['artists']]
        self.artists_names = [artist['name'] for artist in spotify_track['artists']]


        # Album information
        self.album_id = spotify_track['album']['id']

        self.album_type = spotify_track['album']['album_type']
        self.album_type2 = spotify_track['album']['type']

        self.album_name = spotify_track['album']['name']
        self.album_release_date = spotify_track['album']['release_date']
        self.album_image = spotify_track['album']['images'][0]['url']

        self.disc_number = spotify_track['disc_number']
        self.track_number = spotify_track['track_number']

        self.album_artists_spotify_ids = [artist['id'] for artist in spotify_track['album']['artists']]
        self.album_artists_name = [artist['name'] for artist in spotify_track['album']['artists']]

class album:
    def __init__(self):
        pass

class librairy:
    def __init__(self):

        logging.info("Creating Spotify Clients...")
        self.spotify_client = spotify.spotify_client(
            client_id=SPOTIFY_CLIENT_ID,
            client_secret=SPOTIFY_CLIENT_SECRET,
            url=SPOTIFY_REDIRECT_URI
        )

        self.albums = []

    def get_spotify_tracks(self):
        logging.info("Gathering saved tracks...")

        saved_tracks = []

        iteration = 0
        browse_all_saved_tracks = False
        while not browse_all_saved_tracks:

            offset = iteration * 20
            results = self.spotify_client.sp.current_user_saved_tracks(offset=offset)

            for idx, item in enumerate(results['items']):
                my_track = track()
                my_track.init_from_playlist(item)

                saved_tracks.append(my_track)

            iteration += 1
            if len(results['items']) < 20:
                browse_all_saved_tracks = True

        # TODO: add saved tracks in the right form into the albums list

    def get_spotify_albums(self):
        logging.info("Gathering saved albums...")

        saved_album_tracks = []
        spotify_ids = []

        iteration = 0
        browse_all_saved_albums = False
        while not browse_all_saved_albums:

            offset = iteration * 20
            results = self.spotify_client.sp.current_user_saved_albums(offset=offset)

            # loop over albums
            for idx, item in enumerate(results['items']):

                # loop over tracks
                musics = item['album']['tracks']['items']
                for music in musics:
                    spotify_ids.append(music['id'])

            iteration += 1
            if len(results['items']) < 20:
                browse_all_saved_albums = True

        for i in range(0, len(spotify_ids), 50):

            all_tracks = self.spotify_client.sp2.tracks(spotify_ids[i:i + 50])

            for idx, item in enumerate(all_tracks['tracks']):
                my_track = track()
                my_track.init_from_album(item)

                saved_album_tracks.append(my_track)

        # TODO: add saved albums in the right form into the albums list

    def get_spotify_playlist(self):
        logging.info("Gathering saved playlists...")

        saved_playlist_tracks = []

        iteration = 0
        browse_all_saved_playlists = False
        while not browse_all_saved_playlists:

            offset = iteration * 50
            results = self.spotify_client.sp.current_user_playlists(offset=offset)

            for idx, item in enumerate(results['items']):

                spotify_id = item['id']
                name = item['name']

                iteration_pl = 0
                browse_all_tracks_in_playlist = False
                while not browse_all_tracks_in_playlist:

                    offset = iteration_pl * 100
                    playlist = self.spotify_client.sp.playlist_tracks(spotify_id, offset=offset)

                    for a_track_id, a_track in enumerate(playlist['items']):
                        my_track = track()
                        my_track.init_from_playlist(a_track)

                        saved_playlist_tracks.append(my_track)

                    iteration_pl += 1
                    if len(playlist['items']) < 100:
                        browse_all_tracks_in_playlist = True

            iteration += 1
            if len(results['items']) < 50:
                browse_all_saved_playlists = True

        # TODO: add saved playlists in the right form into the albums list