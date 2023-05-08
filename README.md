# spotify-sxm
Replicate SXM stations to Spotify by grabbing the most recent tracks for a given channel via the xmplaylist API. Next, it leverages the spotipy package to detect incoming duplicates (check list of current tracks vs recently played) and then adds the fresh tracks.


# Installation
 ```pip install git+https://github.com/AustinHarley/spotify-sxm.git```

 # Usage
 
 ```
 from spotifysxm.functions import SXMify
 sxm = SXMify(
    spotify_client_id = "",
    spotify_client_secret = "",
    spotify_refresh_token = "",
    slack_token = ""
)

station_info = {
    "sxm_station_id": "", #name in url from xmplaylist.com
    "sxm_station_name": "", #friendly name
    "spotify_playlist_id": "", #id of your spotify playlist
    "spotify_playlist_name": "", #friendly name
    "excluded_spotify_ids": [] #ids of spotify tracks that you want to block
}

playlist_update = sxm.update_playlist(station_info)
```