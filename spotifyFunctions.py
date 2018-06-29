import sys
import pprint
import shelve
import time

import random

import spotipy
import spotipy.util as util

spotifyObject = None
username = ""
iTunes2spotifyMapping = None

uriCache = None
uriFilename = ".uricache"

maxSongsPerAddTracksCall = 20
jankyRateLimitingWaitTime = 2000 # milliseconds
jankyRateLimitingLastRequestTime = None

maxRetryAttempts = 3

def getUserToken():
    global username

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
    searchString = s.encode('ascii','ignore')
    return searchString

# Check if we already have the URI.  When we don't retreive, cache, while
# rate-limiting so Spotify doesn't get cranky
def tracks2SpotifyURIs( tracks ):
    global uriCache, uriFilename
    if uriCache is None:
        uriCache = shelve.open(uriFilename)

    results = []
    for t in tracks:
        ## Attempt to search by all criteria
        songURI = track2SpotifyURIs(t, uriCache)

        ## Attempt to search by just track + Artist
        if songURI is None:
            t2 = t
            t2.pop('album')
            searchString = trackDict2SpotifySearchString(t2)
            songURI = track2SpotifyURIs(t2, uriCache)

        if songURI is not None:
            results.append(songURI)
            uriCache.sync()

    uriCache.close()
    return results

def track2SpotifyURIs(track, cache):
    searchString = trackDict2SpotifySearchString(track)
    songURI = None
    if searchString in cache:
        songURI = cache[searchString]
        return

    jankyRateLimiting()
    songURI = findSpotifyURI(track)
    if songURI is not None:
        cache[searchString] = songURI

    return songURI

# Make sure we don't hammer Spotify
def jankyRateLimiting():
    global jankyRateLimitingLastRequestTime
    now = int(round(time.time() * 1000))

    if jankyRateLimitingLastRequestTime is None:
        jankyRateLimitingLastRequestTime = now
        return

    timeSince = now - jankyRateLimitingLastRequestTime
    jankyRateLimitingLastRequestTime = now

    if timeSince < jankyRateLimitingWaitTime:
        waitTime = (jankyRateLimitingWaitTime - timeSince)/1000.0
        print "Waiting %2.3f" % waitTime
        time.sleep( waitTime )


def findSpotifyURI(trackDict):
    searchString = trackDict2SpotifySearchString(trackDict)
    print "Looking for '%s'..." % searchString
    try:
        results = spotifyObject.search(q=searchString, type='track')
    except:
        print("Unexpected error:", sys.exc_info()[0])
        print "E: MISSING: Couldn't find '%s'" % searchString
        return None
    if results['tracks']['total'] == 0:
        print "E: MISSING: Couldn't find '%s'" % searchString
        return None
    return results['tracks']['items'][0]['uri']

def createPlaylist(playlistName):
    print "Created playlist '%s'" % playlistName
    playlistObject = spotifyObject.user_playlist_create(username, playlistName, public=False)
    return playlistObject["id"]

def chunker(seq, size):
    return (seq[pos:pos + size] for pos in xrange(0, len(seq), size))

def addSpotifyURIstoPlaylist(playlistId, songUris):
    for group in chunker(songUris, maxSongsPerAddTracksCall):
        results = None
        attempts = 0
        while attempts < maxRetryAttempts:
            attempts += 1
            jankyRateLimiting()
            print "Adding tracks to playlist (%d)..." % attempts
            try:
                results = spotifyObject.user_playlist_add_tracks(username, playlistId, group)
                break
            except:
                print("E: Unexpected error:", sys.exc_info()[0])

def addTracksToPlaylist(playlistName, tracks):
    getUserToken()
    songUris = tracks2SpotifyURIs(tracks)
    playlistId = createPlaylist(playlistName)

    addSpotifyURIstoPlaylist(playlistId, songUris)
