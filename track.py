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
        

    def display(self) :
        artists = ""
        for artist in self.artists_names[:-1]:
            artists +=  artist + ", "
        artists += self.artists_names[-1]

        duration = str(int((self.duration/(1000*60*60))%24)) + ":" + str(int((self.duration/(1000*60))%60)) + ":" + str(int((self.duration/1000)%60))

        print(artists + " - " + self.name + " - " + self.album_name + " - " + duration + " - " + str(self.isrc) + " - " + self.spotify_id)