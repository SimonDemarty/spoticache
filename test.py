from __future__ import unicode_literals

import sys
import pickle
import os
import subprocess
import requests

from pytube import YouTube, Search

import music_tag

import youtube_dl


with open('all_albums.pickle', 'rb') as handle :
    all_albums = pickle.load(handle)
with open('all_tracks.pickle', 'rb') as handle :
    all_tracks = pickle.load(handle)

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