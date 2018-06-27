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
    if len(sys.argv) > 2:
        spotifyFunctions.username = sys.argv[1]
        playlistFilename = sys.argv[2]
    else:
        print "Usage: %s username playlist.xml" % (sys.argv[0],)
        sys.exit()

    playlistName = itunesFunctions.iTunesXML2PlaylistName(playlistFilename)
    tracks = itunesFunctions.itunesXML2PythonDict(playlistFilename)

    spotifyFunctions.addTracksToPlaylist(playlistName, tracks)

if __name__ == "__main__":
    main()
