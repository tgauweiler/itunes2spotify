import sys
import pprint
import shelve
import time

import spotipy
import spotipy.util as util

spotifyObject = None
username = ""
iTunes2spotifyMapping = None

uriCache = None
uriFilename = ".uricache"

def getUserToken():
    global username

    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        print "Usage: %s username" % (sys.argv[0],)
        sys.exit()

    scope = 'user-library-read playlist-modify-private'
    token = util.prompt_for_user_token(username, scope)

    global spotifyObject
    if token:
        spotifyObject = spotipy.Spotify(auth=token)
    else:
        print "Can't get token for", username
        sys.exit()

    return token

def trackDict2SpotifySearchString(trackDict):
    s = ""
    for ituneKey, spotifyKey in iTunes2spotifyMapping.items():
        if spotifyKey in trackDict:
            s += spotifyKey + ':"' + trackDict[spotifyKey] + '" '
    return s

# Check if we already have the URI.  When we don't retreive, cache, while
# rate-limiting so Spotify doesn't get cranky
def tracks2SpotifyURIs( tracks ):
    global uriCache, uriFilename
    if uriCache is None:
        uriCache = shelve.open(uriFilename)

    results = []
    for t in tracks:
        searchString = trackDict2SpotifySearchString(t)
        if searchString in uriCache:
            print "In cache - %s" % searchString
            results.append(uriCache[searchString])
        else:
            print "Fetching - %s" % searchString
            time.sleep(.5)
            songURI = findSpotifyURI(t)
            results.append(songURI)
            uriCache[ searchString ] = songURI
    uriCache.close()
    return results


def findSpotifyURI(trackDict):
    searchString = trackDict2SpotifySearchString(trackDict)
    results = spotifyObject.search(q=searchString, type='track')
    return results['tracks']['items'][0]['uri']

def createPlaylist(playListName):
    playlistObject = spotifyObject.user_playlist_create(username, playListName, public=False)
    return playlistObject["id"]

def addSpotifyURIstoPlaylist(playlistID, songIDs):
    results = spotifyObject.user_playlist_add_tracks(username, playlistID, songIDs)
    pprint.pprint( results )
