"""
Emotion Detection Module
Uses DeepFace for real-time facial emotion recognition.
Falls back to a mock detector if DeepFace is not installed.
"""

import cv2
import numpy as np

try:
    from deepface import DeepFace
    DEEPFACE_AVAILABLE = True
    print("[EmotionDetector] DeepFace loaded successfully.")
except ImportError:
    DEEPFACE_AVAILABLE = False
    print("[EmotionDetector] DeepFace not found. Using mock detector.")


EMOTIONS = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']


class EmotionDetector:
    def __init__(self):
        self.use_deepface = DEEPFACE_AVAILABLE

    def detect(self, frame):
        """
        Detect dominant emotion from an image frame.

        Returns:
            tuple: (dominant_emotion: str, confidence: float, all_emotions: dict)
        """
        if self.use_deepface:
            return self._detect_deepface(frame)
        else:
            return self._detect_mock(frame)

    def _detect_deepface(self, frame):
        try:
            result = DeepFace.analyze(
                frame,
                actions=['emotion'],
                enforce_detection=False,
                silent=True
            )
            if isinstance(result, list):
                result = result[0]

            emotion_scores = result['emotion']
            dominant = result['dominant_emotion']
            confidence = emotion_scores[dominant]

            # normalize scores to percentages
            all_emotions = {k: round(v, 1) for k, v in emotion_scores.items()}

            return dominant, confidence, all_emotions

        except Exception as e:
            print(f"[DeepFace Error] {e}")
            return self._detect_mock(frame)

    def _detect_mock(self, frame):
        """Simulates emotion detection for testing without DeepFace."""
        import random
        scores = {e: round(random.uniform(2, 20), 1) for e in EMOTIONS}
        dominant = max(scores, key=scores.get)
        scores[dominant] = round(random.uniform(50, 85), 1)
        return dominant, scores[dominant], scores
