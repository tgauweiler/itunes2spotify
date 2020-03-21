import sys
import shelve
import time
import logging
import random

import spotipy
import spotipy.util as util

spotifyObject = None
username = ""
iTunes2spotifyMapping = None

uriCache = None
uriFilename = ".uricache"

maxSongsPerAddTracksCall = 20
jankyRateLimitingWaitTime = 2000  # milliseconds
jankyRateLimitingLastRequestTime = None

maxRetryAttempts = 3
totalSongs = 0
totalSongsNotFound = 0


def getUserToken():
    global username, spotifyObject

    scope = 'user-library-read playlist-modify-private'
    # token = util.prompt_for_user_token(username, scope)

    sp_oauth = spotipy.SpotifyOAuth(scope=scope, username=username)
    spotifyObject = spotipy.Spotify(auth_manager=sp_oauth)

    # if token:
    #     spotifyObject = spotipy.Spotify(auth=token)
    # else:
    #     logging.error(f"Can't get token for {username}")
    #     sys.exit()


def trackDict2SpotifySearchString(trackDict):
    s = ""
    for ituneKey, spotifyKey in iTunes2spotifyMapping.items():
        if spotifyKey in trackDict:
            s += spotifyKey + ':"' + trackDict[spotifyKey] + '" '
    # searchString = s.encode('ascii', 'ignore')
    searchString = s
    return searchString

# Check if we already have the URI.  When we don't retreive, cache, while
# rate-limiting so Spotify doesn't get cranky


def tracks2SpotifyURIs(tracks):
    global uriCache, uriFilename, totalSongs, totalSongsNotFound
    if uriCache is None:
        uriCache = shelve.open(uriFilename)

    results = []
    for t in tracks:
        totalSongs += 1
        # Attempt to search by all criteria
        songURI = track2SpotifyURIs(t, uriCache)
        searchString = trackDict2SpotifySearchString(t)

        # Attempt to search by just track + Artist
        if songURI is None:
            t2 = t
            t2.pop('album')
            songURI = track2SpotifyURIs(t2, uriCache)
            if songURI is not None:
                logging.warning("I: Fallback on '%s'" % searchString)

        if songURI is not None:
            results.append(songURI)
            uriCache.sync()
        else:
            totalSongsNotFound += 1
            logging.error("MISSING: Couldn't find '%s'" % searchString)

    uriCache.close()
    return results


def track2SpotifyURIs(track, cache):
    songURI = None
    searchString = str(trackDict2SpotifySearchString(track))
    if searchString in list(cache.keys()):
        songURI = cache[searchString]
        return songURI

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
        time.sleep(waitTime)


def findSpotifyURI(trackDict):
    searchString = trackDict2SpotifySearchString(trackDict)
    attempts = 0
    while attempts < maxRetryAttempts:
        attempts += 1
        logging.debug("Looking for '%s'... (%d)" % (searchString, attempts))
        try:
            results = spotifyObject.search(q=searchString, type='track')
            break
        except:
            logging.error("Unexpected error:", sys.exc_info()[0])
            return None

    if results['tracks']['total'] == 0:
        return None
    return results['tracks']['items'][0]['uri']


def createPlaylist(playlistName):
    logging.info("Created playlist '%s'" % playlistName)
    playlistObject = spotifyObject.user_playlist_create(username, playlistName, public=False)
    return playlistObject["id"]


def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))


def addSpotifyURIstoPlaylist(playlistId, songUris):
    for group in chunker(songUris, maxSongsPerAddTracksCall):
        results = None
        attempts = 0
        while attempts < maxRetryAttempts:
            attempts += 1
            jankyRateLimiting()
            logging.info("Adding %d tracks to playlist (%d)...", len(group), attempts)
            try:
                results = spotifyObject.user_playlist_add_tracks(username, playlistId, group)
                break
            except:
                logging.error("Unexpected error:", sys.exc_info()[0])


def addTracksToPlaylist(playlistName, tracks):
    global totalSongs, totalSongsNotFound
    getUserToken()
    songUris = tracks2SpotifyURIs(tracks)
    logging.info(f"#Songs: {totalSongs} with not found #songs: {totalSongsNotFound}")
    playlistId = createPlaylist(playlistName)

    addSpotifyURIstoPlaylist(playlistId, songUris)
