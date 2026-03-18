"""
Spotify Integration Module
Uses Spotipy to fetch mood-based song recommendations via Spotify Web API.
Credentials are loaded from the .env file.
"""

import os
from recommendation.mood_mapper import get_mapping

try:
    import spotipy
    from spotipy.oauth2 import SpotifyClientCredentials
    SPOTIPY_AVAILABLE = True
except ImportError:
    SPOTIPY_AVAILABLE = False
    print("[Spotify] spotipy not installed. Run: pip install spotipy")

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

CLIENT_ID     = os.getenv("SPOTIFY_CLIENT_ID", "0f87384ae53043d788857502fdda098d")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET", "e92ccda9d8494589aea858b9ef7af15a")
REDIRECT_URI  = os.getenv("SPOTIFY_REDIRECT_URI", "https://localhost:8888/callback")


# ── Mock data fallback ───────────────────────────────────────────────────────
MOCK_TRACKS = {
    "happy": [
        {"name": "Happy", "artist": "Pharrell Williams", "album": "G I R L", "preview_url": None, "spotify_url": "https://open.spotify.com/track/60nZcImufyMA1MKQY3dcCH", "image": "https://i.scdn.co/image/ab67616d0000b2732e8ed79e177ff6011076f5f0", "duration": "3:53"},
        {"name": "Uptown Funk", "artist": "Mark Ronson ft. Bruno Mars", "album": "Uptown Special", "preview_url": None, "spotify_url": "https://open.spotify.com/track/32OlwWuMpZ6b0aN2RZOeMS", "image": "https://i.scdn.co/image/ab67616d0000b273e419ccba0baa8bd3f3de8b9b", "duration": "4:30"},
        {"name": "Can't Stop the Feeling", "artist": "Justin Timberlake", "album": "Trolls OST", "preview_url": None, "spotify_url": "https://open.spotify.com/track/1WkMMavIMc4JZ8cfMmxHkI", "image": "https://i.scdn.co/image/ab67616d0000b27381b78f1b5cc52b7b29fe86e2", "duration": "3:56"},
        {"name": "Good as Hell", "artist": "Lizzo", "album": "Cuz I Love You", "preview_url": None, "spotify_url": "https://open.spotify.com/track/6KgBpzTuTRPebChN0VTyzV", "image": "https://i.scdn.co/image/ab67616d0000b273f3cb5e80c9da97de3b1b7277", "duration": "2:39"},
        {"name": "Shake It Off", "artist": "Taylor Swift", "album": "1989", "preview_url": None, "spotify_url": "https://open.spotify.com/track/0cqRj7pUJDkTCEsJkx8snD", "image": "https://i.scdn.co/image/ab67616d0000b273e787cffec20aa2a396a61647", "duration": "3:39"},
    ],
    "sad": [
        {"name": "The Night We Met", "artist": "Lord Huron", "album": "Strange Trails", "preview_url": None, "spotify_url": "https://open.spotify.com/track/0pvTNxHAj4XBNZoa8CXWHI", "image": "https://i.scdn.co/image/ab67616d0000b273d1e58e8e0c52c0b8f7c3e3b5", "duration": "3:28"},
        {"name": "Someone Like You", "artist": "Adele", "album": "21", "preview_url": None, "spotify_url": "https://open.spotify.com/track/1zwMYTA5nlNjZxYrvBB2pV", "image": "https://i.scdn.co/image/ab67616d0000b2732118bf9b198b05a95ded6300", "duration": "4:45"},
        {"name": "Fix You", "artist": "Coldplay", "album": "X&Y", "preview_url": None, "spotify_url": "https://open.spotify.com/track/7LVHVU3tWfcxj5aiPFEW4Q", "image": "https://i.scdn.co/image/ab67616d0000b2730b3698b7f92a0b413a4a0bac", "duration": "4:55"},
        {"name": "Skinny Love", "artist": "Bon Iver", "album": "For Emma, Forever Ago", "preview_url": None, "spotify_url": "https://open.spotify.com/track/1eBFKuwWuAnWqBdzkKcPiN", "image": "https://i.scdn.co/image/ab67616d0000b2730d2e4f3bad8e00ad20bc67af", "duration": "3:58"},
        {"name": "Liability", "artist": "Lorde", "album": "Melodrama", "preview_url": None, "spotify_url": "https://open.spotify.com/track/6mi8tMSP2ZEzaUJBNPBWn7", "image": "https://i.scdn.co/image/ab67616d0000b273b4e4fbed0e80d0e3c4b24cef", "duration": "3:38"},
    ],
    "angry": [
        {"name": "Break Stuff", "artist": "Limp Bizkit", "album": "Significant Other", "preview_url": None, "spotify_url": "https://open.spotify.com/track/5d7MDPauR8KoNkEzGSVmqY", "image": "https://i.scdn.co/image/ab67616d0000b2732a71e54b8cfb0bd2d98f6898", "duration": "2:46"},
        {"name": "Killing in the Name", "artist": "Rage Against The Machine", "album": "RATM", "preview_url": None, "spotify_url": "https://open.spotify.com/track/59WN2psjkt1tyaxjspN8fp", "image": "https://i.scdn.co/image/ab67616d0000b273d12b30b9ef8e1d4dfd9dbd4c", "duration": "5:14"},
        {"name": "Numb", "artist": "Linkin Park", "album": "Meteora", "preview_url": None, "spotify_url": "https://open.spotify.com/track/3vbEelR0jc8f7a0tLDicDt", "image": "https://i.scdn.co/image/ab67616d0000b2738deb7ee7e01c0cf7adec6928", "duration": "3:05"},
        {"name": "In the End", "artist": "Linkin Park", "album": "Hybrid Theory", "preview_url": None, "spotify_url": "https://open.spotify.com/track/60a0Rd6pjrkxjPbaKzXjfq", "image": "https://i.scdn.co/image/ab67616d0000b273fcb9b9a6e8ea0b479a4c7d05", "duration": "3:36"},
        {"name": "Du Hast", "artist": "Rammstein", "album": "Sehnsucht", "preview_url": None, "spotify_url": "https://open.spotify.com/track/2jBMqstNBqpVuFXhJOTKiQ", "image": "https://i.scdn.co/image/ab67616d0000b2736a0ea7e35c4e1e57e52cd08f", "duration": "3:55"},
    ],
    "neutral": [
        {"name": "Redbone", "artist": "Childish Gambino", "album": "Awaken, My Love!", "preview_url": None, "spotify_url": "https://open.spotify.com/track/0wXuerDYiBnERgIpbb3JBR", "image": "https://i.scdn.co/image/ab67616d0000b27372f7fed4e45a6b2abe1a6f27", "duration": "5:26"},
        {"name": "Electric Feel", "artist": "MGMT", "album": "Oracular Spectacular", "preview_url": None, "spotify_url": "https://open.spotify.com/track/3FtYbEfBqAlGDPZZlZOLhE", "image": "https://i.scdn.co/image/ab67616d0000b27358ce2bcd5cf3ac63fac3b9e5", "duration": "3:49"},
        {"name": "Coffee", "artist": "beabadoobee", "album": "Fake It Flowers", "preview_url": None, "spotify_url": "https://open.spotify.com/track/4zbCpABxKr3JVGRKbcXfcn", "image": "https://i.scdn.co/image/ab67616d0000b273c3a23a28c0afab8bc24e2fe9", "duration": "1:52"},
        {"name": "Sunset Lover", "artist": "Petit Biscuit", "album": "Presence", "preview_url": None, "spotify_url": "https://open.spotify.com/track/3C5G4PgBVvWbxkU6gLlbGp", "image": "https://i.scdn.co/image/ab67616d0000b273f2f92c55e5acdf4649671db3", "duration": "3:40"},
        {"name": "Chill Pill", "artist": "JVKE", "album": "This is What Heartbreak Feels Like", "preview_url": None, "spotify_url": "https://open.spotify.com/track/4uLU6hMCjMI75M1A2tKUQC", "image": "https://i.scdn.co/image/ab67616d0000b2739c9c34f26028c7ca74fc20d4", "duration": "2:42"},
    ],
    "fear": [
        {"name": "Breathe Me", "artist": "Sia", "album": "Colour the Small One", "preview_url": None, "spotify_url": "https://open.spotify.com/track/2VEZx7NWsZ1D0eJ4uv5Fym", "image": "https://i.scdn.co/image/ab67616d0000b273f5fec81e5b48c3c3a6b3e3f8", "duration": "4:33"},
        {"name": "Mad World", "artist": "Gary Jules", "album": "Trading Snakeoil for Wolftickets", "preview_url": None, "spotify_url": "https://open.spotify.com/track/3JOVTQ5h8HyvI3Uu4Yd9bX", "image": "https://i.scdn.co/image/ab67616d0000b2738e7be375f63c6e8a7f0cbf11", "duration": "3:08"},
        {"name": "Holocene", "artist": "Bon Iver", "album": "Bon Iver, Bon Iver", "preview_url": None, "spotify_url": "https://open.spotify.com/track/3SRpqv1dOJcJbGmSzOiAZ5", "image": "https://i.scdn.co/image/ab67616d0000b2738af0e9a0e3e2ac1ddb66e8ce", "duration": "5:37"},
        {"name": "Skinny", "artist": "Billie Eilish", "album": "HIT ME HARD AND SOFT", "preview_url": None, "spotify_url": "https://open.spotify.com/track/4Vy8oYDrGDdXFxRqIjMmrr", "image": "https://i.scdn.co/image/ab67616d0000b273e2e352d89826aef6dbd5ff8f", "duration": "4:30"},
        {"name": "Comptine d'un autre été", "artist": "Yann Tiersen", "album": "Amélie OST", "preview_url": None, "spotify_url": "https://open.spotify.com/track/1YLSg9p9V7mMhwYcxD2mNq", "image": "https://i.scdn.co/image/ab67616d0000b2737b5a2a0f6bc5b17b9e6a3a9e", "duration": "2:22"},
    ],
    "surprise": [
        {"name": "Blinding Lights", "artist": "The Weeknd", "album": "After Hours", "preview_url": None, "spotify_url": "https://open.spotify.com/track/0VjIjW4GlUZAMYd2vXMi3b", "image": "https://i.scdn.co/image/ab67616d0000b2738863bc11d2aa12b54f5aeb36", "duration": "3:20"},
        {"name": "Levitating", "artist": "Dua Lipa", "album": "Future Nostalgia", "preview_url": None, "spotify_url": "https://open.spotify.com/track/463CkQjx2Zk1yXoBuierM9", "image": "https://i.scdn.co/image/ab67616d0000b27312bc4f12220d159d571841a2", "duration": "3:23"},
        {"name": "As It Was", "artist": "Harry Styles", "album": "Harry's House", "preview_url": None, "spotify_url": "https://open.spotify.com/track/4Dvkj6JhhA12EX05fT7y2e", "image": "https://i.scdn.co/image/ab67616d0000b2732e8ed79e177ff6011076f5f0", "duration": "2:37"},
        {"name": "Dynamite", "artist": "BTS", "album": "Dynamite", "preview_url": None, "spotify_url": "https://open.spotify.com/track/5QDLhrAOJJdNAmCTJ8xMyW", "image": "https://i.scdn.co/image/ab67616d0000b27382e9b2ef3e9f4bd04ec32c8a", "duration": "3:19"},
        {"name": "STAY", "artist": "The Kid LAROI & Justin Bieber", "album": "STAY", "preview_url": None, "spotify_url": "https://open.spotify.com/track/5PjdY0CKGZdEuoNab3yDmX", "image": "https://i.scdn.co/image/ab67616d0000b2730fbba3fdecf08af24a6ddba5", "duration": "2:21"},
    ],
    "disgust": [
        {"name": "Alright", "artist": "Kendrick Lamar", "album": "To Pimp a Butterfly", "preview_url": None, "spotify_url": "https://open.spotify.com/track/3iVcZ5G6tvkXZkZKlMpIUs", "image": "https://i.scdn.co/image/ab67616d0000b273cdb645498cd9d5a38e49e5c3", "duration": "3:39"},
        {"name": "The Sound of Silence", "artist": "Simon & Garfunkel", "album": "Wednesday Morning, 3 A.M.", "preview_url": None, "spotify_url": "https://open.spotify.com/track/3YfS47QufnLDFA71FUsgCM", "image": "https://i.scdn.co/image/ab67616d0000b273e2b4c02b2dfce7e1c9e0dcb9", "duration": "3:05"},
        {"name": "Hurt", "artist": "Johnny Cash", "album": "American IV", "preview_url": None, "spotify_url": "https://open.spotify.com/track/28cngnBdFgZGhAJ1bqQDiB", "image": "https://i.scdn.co/image/ab67616d0000b2731aa3c1de72048e42bd282c89", "duration": "3:38"},
        {"name": "Eleanor Rigby", "artist": "The Beatles", "album": "Revolver", "preview_url": None, "spotify_url": "https://open.spotify.com/track/7yCPMGgQcPIhGa9Gg4NFDA", "image": "https://i.scdn.co/image/ab67616d0000b273dc30583ba717007b00cceb25", "duration": "2:07"},
        {"name": "God's Plan", "artist": "Drake", "album": "Scary Hours", "preview_url": None, "spotify_url": "https://open.spotify.com/track/6DCZcSspjsKoFjzjrWoCdn", "image": "https://i.scdn.co/image/ab67616d0000b27312f4a6a2c2e8d3a7d3f2b1b3", "duration": "3:18"},
    ],
}


class SpotifyRecommender:
    def __init__(self):
        self.sp = None
        self._connect()

    def _connect(self):
        if not SPOTIPY_AVAILABLE:
            print("[Spotify] spotipy not installed — using mock data.")
            return
        try:
            auth = SpotifyClientCredentials(
                client_id=CLIENT_ID,
                client_secret=CLIENT_SECRET
            )
            self.sp = spotipy.Spotify(auth_manager=auth)
            # Quick connection test
            self.sp.search(q="test", limit=1, type="track")
            print("[Spotify] ✅ Connected successfully with your credentials!")
        except Exception as e:
            print(f"[Spotify] ⚠️  Connection failed: {e}")
            print("[Spotify] Falling back to mock data.")
            self.sp = None

    def is_connected(self):
        return self.sp is not None

    def get_tracks_for_emotion(self, emotion: str, limit: int = 8) -> list:
        if self.sp:
            return self._fetch_from_spotify(emotion, limit)
        return self._get_mock_tracks(emotion)

    def _fetch_from_spotify(self, emotion: str, limit: int) -> list:
        mapping = get_mapping(emotion)
        try:
            results = self.sp.recommendations(
                seed_genres=mapping['seed_genres'][:2],
                min_valence=mapping.get('min_valence', 0.0),
                max_valence=mapping.get('max_valence', 1.0),
                min_energy=mapping.get('min_energy', 0.0),
                max_energy=mapping.get('max_energy', 1.0),
                limit=limit
            )
            tracks = []
            for t in results['tracks']:
                ms = t['duration_ms']
                tracks.append({
                    'name':        t['name'],
                    'artist':      ', '.join(a['name'] for a in t['artists']),
                    'album':       t['album']['name'],
                    'preview_url': t['preview_url'],
                    'spotify_url': t['external_urls']['spotify'],
                    'image':       t['album']['images'][0]['url'] if t['album']['images'] else '',
                    'duration':    f"{ms//60000}:{(ms%60000)//1000:02d}"
                })
            return tracks
        except Exception as e:
            print(f"[Spotify Fetch Error] {e}")
            return self._get_mock_tracks(emotion)

    def _get_mock_tracks(self, emotion: str) -> list:
        return MOCK_TRACKS.get(emotion.lower(), MOCK_TRACKS['neutral'])