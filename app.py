"""
AI Mood-Based Music Recommendation System
Main Flask Application
"""

from flask import Flask, render_template, jsonify, request
import cv2
import base64
import numpy as np
import os
from emotion_detection.detector import EmotionDetector
from recommendation.spotify_client import SpotifyRecommender

app = Flask(__name__)

detector = EmotionDetector()
spotify = SpotifyRecommender()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detect-emotion', methods=['POST'])
def detect_emotion():
    try:
        data = request.get_json()
        image_data = data['image'].split(',')[1]
        img_bytes = base64.b64decode(image_data)
        np_arr = np.frombuffer(img_bytes, np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        emotion, confidence, all_emotions = detector.detect(frame)

        # Fix: convert float32 to plain Python float for JSON
        emotion = str(emotion)
        confidence = float(confidence)
        all_emotions = {str(k): float(v) for k, v in all_emotions.items()}

        return jsonify({
            'success': True,
            'emotion': emotion,
            'confidence': round(confidence, 2),
            'all_emotions': all_emotions
        })
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)})

@app.route('/get-recommendations', methods=['POST'])
def get_recommendations():
    try:
        data = request.get_json()
        emotion = data.get('emotion', 'neutral')
        tracks = spotify.get_tracks_for_emotion(emotion)
        return jsonify({
            'success': True,
            'emotion': emotion,
            'tracks': tracks
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/health')
def health():
    return jsonify({'status': 'ok', 'spotify_connected': spotify.is_connected()})

if __name__ == '__main__':
    app.run(debug=True, port=5000)