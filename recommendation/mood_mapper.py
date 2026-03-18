"""
Mood to Music Mapping
Maps detected emotions to Spotify audio feature ranges and seed genres.
"""

# Spotify audio features reference:
#   valence   : 0.0 (sad/dark) → 1.0 (happy/bright)
#   energy    : 0.0 (slow/soft) → 1.0 (fast/loud)
#   danceability: how suitable for dancing

EMOTION_MUSIC_MAP = {
    "happy": {
        "seed_genres": ["pop", "dance", "funk"],
        "min_valence": 0.7,
        "max_valence": 1.0,
        "min_energy": 0.6,
        "max_energy": 1.0,
        "min_danceability": 0.6,
        "label": "Happy & Uplifting 🎉",
        "color": "#FFD700",
        "emoji": "😄"
    },
    "sad": {
        "seed_genres": ["acoustic", "sad", "indie"],
        "min_valence": 0.0,
        "max_valence": 0.35,
        "min_energy": 0.0,
        "max_energy": 0.45,
        "label": "Melancholic & Soulful 💙",
        "color": "#4A90D9",
        "emoji": "😢"
    },
    "angry": {
        "seed_genres": ["metal", "rock", "punk"],
        "min_valence": 0.0,
        "max_valence": 0.45,
        "min_energy": 0.75,
        "max_energy": 1.0,
        "label": "Intense & Powerful 🔥",
        "color": "#FF4136",
        "emoji": "😠"
    },
    "fear": {
        "seed_genres": ["ambient", "classical", "sleep"],
        "min_valence": 0.2,
        "max_valence": 0.5,
        "min_energy": 0.1,
        "max_energy": 0.45,
        "label": "Calm & Soothing 🌙",
        "color": "#7B68EE",
        "emoji": "😨"
    },
    "surprise": {
        "seed_genres": ["edm", "electronic", "dance"],
        "min_valence": 0.55,
        "max_valence": 1.0,
        "min_energy": 0.65,
        "max_energy": 1.0,
        "min_danceability": 0.65,
        "label": "Exciting & Electric ⚡",
        "color": "#FF69B4",
        "emoji": "😲"
    },
    "neutral": {
        "seed_genres": ["chill", "lo-fi", "indie-pop"],
        "min_valence": 0.35,
        "max_valence": 0.65,
        "min_energy": 0.25,
        "max_energy": 0.65,
        "label": "Chill & Balanced 🎵",
        "color": "#2ECC71",
        "emoji": "😐"
    },
    "disgust": {
        "seed_genres": ["blues", "soul", "r-n-b"],
        "min_valence": 0.1,
        "max_valence": 0.45,
        "min_energy": 0.3,
        "max_energy": 0.65,
        "label": "Bluesy & Raw 🎸",
        "color": "#8B4513",
        "emoji": "😤"
    }
}

def get_mapping(emotion: str) -> dict:
    emotion = emotion.lower().strip()
    return EMOTION_MUSIC_MAP.get(emotion, EMOTION_MUSIC_MAP["neutral"])
