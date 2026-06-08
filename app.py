'''
pip3 install googleapiclient
pip3 install spotipy
'''

from googleapiclient.discovery import build
import spotipy
from spotipy.oauth2 import SpotifyOAuth

YOUTUBE_API_KEY = "api_key"

SPOTIFY_CLIENT_ID = "client_id"
SPOTIFY_CLIENT_SECRET = "secret_id"
SPOTIFY_REDIRECT_URI = "http://127.0.0.1:8888/callback"

PLAYLIST_ID = "playlist id of you tube"


youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=SPOTIFY_REDIRECT_URI,
        scope="playlist-modify-private playlist-modify-public"
    )
)

tracks = []
next_page_token = None

while True:
    response = youtube.playlistItems().list(
        part="snippet",
        playlistId=PLAYLIST_ID,
        maxResults=50,
        pageToken=next_page_token
    ).execute()

    for item in response["items"]:
        title = item["snippet"]["title"]
        tracks.append(title)

    next_page_token = response.get("nextPageToken")

    if not next_page_token:
        break

playlist = sp.current_user_playlist_create(

    name="Imported from YouTube",

    public=False

)

spotify_tracks = []

for track in tracks:
    result = sp.search(q=track, type="track", limit=1)

    if result["tracks"]["items"]:
        spotify_tracks.append(
            result["tracks"]["items"][0]["uri"]
        )
        print("FOUND:", track)
    else:
        print("MISS :", track)

for i in range(0, len(spotify_tracks), 100):
    sp.playlist_add_items(
        playlist["id"],
        spotify_tracks[i:i+100]
    )

print("Done!")
