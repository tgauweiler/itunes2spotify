# itunes2spotify

Migrate an iTunes playlist to Spotify.

1. Create a new [Spotify Application](https://developer.spotify.com/dashboard/applications).
2. Create a callback url for it (doesn't have to be really callable. I used `https://localhost/callback`).
3. Get the client id and client secret for it.
3. Set the environment variables:

```sh
export SPOTIPY_CLIENT_ID='xxxxx'
export SPOTIPY_CLIENT_SECRET='xxxxx'
export SPOTIPY_REDIRECT_URI='http://localhost/callback'
```

4. Install
```sh
pip install -r requirements.txt
python itunes2spotify.py username playlist.xml
```
Tested with python 3.7.
