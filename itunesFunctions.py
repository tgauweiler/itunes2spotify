import sys
import plistlib


def itunesDict2python(playlistFile):
    keyMapping = {"Name": "name", "Artist": "arist", "Album": "album"}

    root = plistlib.readPlist(playlistFile)
    tracks = root["Tracks"]
    playlist = root["Playlists"][0]["Playlist Items"]

    playlistArr = []

    for num, trackDict in enumerate(playlist):
        trackID = str(trackDict["Track ID"])
        simpleTrackDict = {};
        for key, value in keyMapping.iteritems():
            simpleTrackDict[value] = ""
            if key in tracks[trackID]:
                simpleTrackDict[value] = tracks[trackID][key]
        playlistArr.append(simpleTrackDict)

    return playlistArr

def main():
    p = itunesDict2python("liveinlondon.xml")
    print p

if __name__ == "__main__":
    main()
