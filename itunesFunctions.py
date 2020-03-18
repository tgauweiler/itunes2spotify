import sys
import plistlib
import logging

iTunes2spotifyMapping = None


def itunesXML2PythonDict(playlistFile):
    root = plistlib.readPlist(playlistFile)
    tracks = root["Tracks"]
    playlist = root["Playlists"][0]["Playlist Items"]

    playlistArr = []

    for num, trackDict in enumerate(playlist):
        trackID = str(trackDict["Track ID"])
        simpleTrackDict = {}
        for key, value in iTunes2spotifyMapping.items():
            simpleTrackDict[value] = ""
            if key in tracks[trackID]:
                simpleTrackDict[value] = tracks[trackID][key]
        playlistArr.append(simpleTrackDict)

    return playlistArr


def iTunesXML2PlaylistName(playlistFile):
    root = plistlib.readPlist(playlistFile)
    playlistName = root['Playlists'][0]['Name']
    return playlistName


def main():
    p = iTunesXML2PlaylistName("liveinlondon.xml")


if __name__ == "__main__":
    main()
