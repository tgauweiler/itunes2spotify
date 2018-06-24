import sys
import pprint
import time

import spotifyFunctions
import itunesFunctions

spotifyObject = None
username = ""


iTunes2spotifyMapping = {"Name": "track", "Artist": "artist", "Album": "album"}
# Shame-cube here
spotifyFunctions.iTunes2spotifyMapping = iTunes2spotifyMapping
itunesFunctions.iTunes2spotifyMapping = iTunes2spotifyMapping

def main():
    token = spotifyFunctions.getUserToken();

    playlistName = "Test " + str(int(time.time()))
    print playlistName
    playlistId = spotifyFunctions.createPlaylist(playlistName)

    testDict = {'album': 'Live In London', 'track': 'Dance Me To The End Of Love', 'artist': 'Leonard Cohen'}
    songID = spotifyFunctions.findSpotifyURI(testDict)
    spotifyFunctions.addSpotifyURIstoPlaylist(playlistId, [ songID ])

if __name__ == "__main__":
    main()
