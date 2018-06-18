import sys
import spotipy
import spotipy.util as util

scope = 'user-library-read'
spotifyObject = None

def getUserToken():


    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        print "Usage: %s username" % (sys.argv[0],)
        sys.exit()

    token = util.prompt_for_user_token(username, scope)

    global spotifyObject
    if token:
        spotifyObject = spotipy.Spotify(auth=token)
    else:
        print "Can't get token for", username
        sys.exit()

    # if token:
    #     spotifyObject = spotipy.Spotify(auth=token)
    #     results = spotifyObject.current_user_saved_tracks()
    #     for item in results['items']:
    #         track = item['track']
    #         print track['name'] + ' - ' + track['artists'][0]['name']

    return token

def findSpotifyURI(trackDict):
    results = spotifyObject.search(q='album:' + trackDict["album"], type='album')
    for item in results['albums']['items']:
        print item
        print "---"
        for key in item:
            print key
        print "---"
        print item['name'] + ' - ' + item['artists'][0]['name']

def main():
    token = getUserToken();
    testDict = {'album': 'Live In London', 'name': 'Dance Me To The End Of Love', 'arist': 'Leonard Cohen'}
    findSpotifyURI(testDict)

if __name__ == "__main__":
    main()
