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
    playlistName = itunesFunctions.iTunesXML2PlaylistName("liveinlondon.xml")
    tracks = itunesFunctions.itunesXML2PythonDict("liveinlondon.xml")

    token = spotifyFunctions.getUserToken();
    songURIs = spotifyFunctions.tracks2SpotifyURIs(tracks)
    pprint.pprint(songURIs)
    # playlistId = spotifyFunctions.createPlaylist(playlistName)
    # songID = spotifyFunctions.findSpotifyURI(testDict)
    # spotifyFunctions.addSpotifyURIstoPlaylist(playlistId, [ songID ])


def NOTmain():
    playlistName = "Test " + str(int(time.time()))
    print playlistName
    testDict = {'album': 'Live In London', 'track': 'Dance Me To The End Of Love', 'artist': 'Leonard Cohen'}

if __name__ == "__main__":
    main()
