# 🎵 MoodTunes — AI Mood-Based Music Recommendation System

An intelligent system that detects your facial emotion in real time using deep learning,
then recommends perfectly matched songs via the Spotify API.

## Tech Stack
- **Python + Flask** — Backend web server
- **DeepFace (CNN)** — Real-time facial emotion recognition  
- **Spotipy** — Spotify Web API integration
- **Vanilla JS + CSS** — Frontend (no frameworks needed)

## Detected Emotions
`happy` `sad` `angry` `fear` `surprise` `neutral` `disgust`

---

## ⚡ Quick Start

### 1. Clone & Setup
```bash
cd mood-music
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Spotify API
```bash
cp .env.example .env
# Edit .env with your Spotify credentials
```

Get credentials at: https://developer.spotify.com/dashboard
- Create App → copy Client ID & Client Secret
- Add Redirect URI: `http://localhost:8888/callback`

### 3. Run
```bash
python app.py
```
Open: http://localhost:5000

---

## 📁 Project Structure
```
mood-music/
├── app.py                          # Flask server & API routes
├── requirements.txt
├── .env.example                    # Spotify credentials template
├── emotion_detection/
│   ├── detector.py                 # DeepFace emotion detection
│   └── train_cnn.py                # Custom CNN training (optional)
├── recommendation/
│   ├── spotify_client.py           # Spotify API + mock fallback
│   └── mood_mapper.py              # Emotion → music feature mapping
└── templates/
    └── index.html                  # Full UI
```

---

## 🧠 How It Works

```
Webcam Frame
     ↓
DeepFace CNN (FER-2013 trained)
     ↓
Dominant Emotion (e.g., "happy")
     ↓
Mood Mapper (valence, energy, genre)
     ↓
Spotify Recommendations API
     ↓
Song List with Cover Art + Links
```

---

## 🎓 Training Your Own CNN (Optional)
1. Download FER-2013 from Kaggle
2. Extract to `data/fer2013/`
3. Run: `python emotion_detection/train_cnn.py`

---

## 📝 Demo Mode
If Spotify credentials are not set, the app uses a built-in mock dataset
with real popular songs for each emotion. Perfect for demos!
