# Dependencies =================================================================

# Environment
# import os
# from dotenv import load_dotenv

# Information
import logging

# APIs
from API import spotify
from MUSIC.utils import librairy

# Initialisation ===============================================================

logging.basicConfig(
    level=logging.INFO,
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M:%S"
)



# Different API Connections ====================================================
# logging.info("Connecting to APIs...")

# logging.info("Creating YouTube Client...")
# TODO

# Music Information Collection =================================================

logging.info("initiating User Library...")
librairy = librairy()

logging.info("Gathering Users Spotify Tracks...")

librairy.get_spotify_tracks()
librairy.get_spotify_albums()
librairy.get_spotify_playlist()