import requests
import spotipy
import slack_sdk


class SXMify:
    def __init__(
        self,
        spotify_client_id: str,
        spotify_client_secret: str,
        spotify_refresh_token: str,
        slack_token: str = "",
    ):
        self.spotify_client_id = spotify_client_id
        self.spotify_client_secret = spotify_client_secret
        self.spotify_refresh_token = spotify_refresh_token
        self.slack_token = slack_token
        if slack_token:
            self.slacker = slack_sdk.WebClient(token=slack_token)
        self.spotify_client = self.init_spotify_client()

    def init_spotify_client(self, redirect_uri="http://localhost:6969/callback"):
        scopes = "playlist-modify-public user-library-read"
        sp_oauth = spotipy.oauth2.SpotifyOAuth(
            client_id=self.spotify_client_id,
            client_secret=self.spotify_client_secret,
            redirect_uri=redirect_uri,
            scope=scopes,
        )
        token = sp_oauth.refresh_access_token(self.spotify_refresh_token)["access_token"]
        spotify_client = spotipy.Spotify(auth=token)
        return spotify_client

    def get_recently_played_tracks_by_station(self, sxm_station_id: str) -> list:
        station_data = requests.get(
            f"https://xmplaylist.com/api/station/{sxm_station_id}"
        ).json()
        recent_sxm_tracks = []
        for recent_track in station_data:
            if "spotify" in recent_track.keys():
                recent_sxm_tracks.append(recent_track["spotify"]["spotify_id"])
        return recent_sxm_tracks

    def get_tracks_by_playlist(self, spotify_playlist_id: str) -> list:
        playlist = self.spotify_client.playlist_tracks(spotify_playlist_id)
        tracks = []
        has_more_items = True
        offset = 0
        while has_more_items:
            for track in playlist["items"]:
                tracks.append(
                    {"id": track["track"]["id"], "name": track["track"]["name"]}
                )
            if playlist["next"]:
                offset += 100
                playlist = self.spotify_client.playlist_tracks(
                    spotify_playlist_id, offset=offset
                )
            else:
                has_more_items = False
        tracks = [t["id"] for t in tracks]
        return tracks

    def update_playlist(self, station_info: dict, exclude_live_songs: bool = True) -> list:
        recent_sxm_tracks = self.get_recently_played_tracks_by_station(
            station_info["sxm_station_id"]
        )
        if recent_sxm_tracks:
            current_tracks = self.get_tracks_by_playlist(
                station_info["spotify_playlist_id"]
            )
            tracks_to_add = [i for i in recent_sxm_tracks if i not in current_tracks]
            if tracks_to_add:

                if exclude_live_songs:
                    # we need the names from spotify in order to determine if it is trying to incorrectly add a live track
                    # sometimes the name displayed in the xmplaylist website can differ from the spotify track name
                    recent_sxm_tracks_sp_data = self.spotify_client.tracks(tracks_to_add)
                    tracks_to_add = [
                        track["id"]
                        for track in recent_sxm_tracks_sp_data["tracks"]
                        if "(live)" not in track["name"].lower()
                        and "- live" not in track["name"].lower()
                        and track["id"] not in station_info["excluded_spotify_ids"]
                    ]
                else:
                    tracks_to_add = [
                        track for track in tracks_to_add if track not in station_info["excluded_spotify_ids"]
                    ]
                if tracks_to_add:
                    _add_tracks = self.spotify_client.playlist_add_items(
                        station_info["spotify_playlist_id"], tracks_to_add
                    )
            return tracks_to_add
        else:
            return []
    def send_slack_update(self, station_info:dict, added_tracks:list, send_empty_update:bool = False) -> None:
        if added_tracks or (not added_tracks and send_empty_update):
            msg = f"`{station_info['sxm_station_name']}` :twisted_rightwards_arrows: `{station_info['spotify_playlist_name']}` *[+{len(added_tracks)}]*"
            self.slacker.chat_postMessage(
                channel="music",
                icon_emoji="headphones",
                text=msg,
                username="sxm-spotify-bot",
            )



