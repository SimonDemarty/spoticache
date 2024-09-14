import track

class album:
    def __init__(self, spotify_id = None, name=None, artists=None, image=None, genre=None, release_date=None):
        self.spotify_id = spotify_id
        self.name = name
        self.artists = artists
        self.image = image
        self.tracklist = []
        self.genre = genre
        self.release_date = release_date
    
    def add_track(self, track2add):
        # tracklist contains elements of type "track"
        # with supposedly ordered track.track_number ordered

        if self.tracklist == [] :
            self.tracklist.append(track2add)

        else :
            if track2add.track_number < self.tracklist[0].track_number :
                self.tracklist.insert(0, track2add)

            elif track2add.track_number > self.tracklist[-1].track_number :
                self.tracklist.append(track2add)

            else :
                for track_idx, track in enumerate(self.tracklist[:-1]) :
                    if track.track_number < track2add.track_number and track2add.track_number < self.tracklist[track_idx+1].track_number :
                        self.tracklist.insert(track_idx+1, track2add)
            
def album_idx(albums, spotify_id) :

    album_in_list = False
    for album_idx, album in enumerate(albums) :
        if album.spotify_id == spotify_id :
            return album_idx
    return -1

def album_lists_equals(albums_test, albums_ref):

    updated_ref = []

    for album in albums_test :
        idx = album_idx(albums_ref, album.spotify_id)
        if idx == -1 :
            updated_ref.append(album)
    
    return updated_ref.extend(albums_ref)
