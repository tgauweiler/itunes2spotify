import sys
import pprint
import time

import spotifyFunctions
import itunesFunctions

iTunes2spotifyMapping = {"Name": "track", "Artist": "artist", "Album": "album"}
# Shame-cube here
spotifyFunctions.iTunes2spotifyMapping = iTunes2spotifyMapping
itunesFunctions.iTunes2spotifyMapping = iTunes2spotifyMapping

def main():
    playlistName = itunesFunctions.iTunesXML2PlaylistName("liveinlondon.xml")
    tracks = itunesFunctions.itunesXML2PythonDict("liveinlondon.xml")

    spotifyFunctions.addTracksToPlaylist(playlistName, tracks)

if __name__ == "__main__":
    main()
