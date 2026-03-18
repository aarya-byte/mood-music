import cv2
import numpy as np

try:
    from fer import FER
    FER_AVAILABLE = True
    print("[EmotionDetector] FER loaded successfully.")
except ImportError:
    FER_AVAILABLE = False
    print("[EmotionDetector] FER not found. Using mock detector.")

EMOTIONS = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']

class EmotionDetector:
    def __init__(self):
        self.detector = FER() if FER_AVAILABLE else None

    def detect(self, frame):
        if self.detector:
            return self._detect_fer(frame)
        return self._detect_mock(frame)

    def _detect_fer(self, frame):
        try:
            result = self.detector.detect_emotions(frame)
            if not result:
                return self._detect_mock(frame)
            emotions = result[0]['emotions']
            dominant = max(emotions, key=emotions.get)
            confidence = float(emotions[dominant]) * 100
            all_emotions = {k: float(v) * 100 for k, v in emotions.items()}
            return dominant, confidence, all_emotions
        except Exception as e:
            print(f"[FER Error] {e}")
            return self._detect_mock(frame)

    def _detect_mock(self, frame):
        import random
        scores = {e: round(random.uniform(2, 20), 1) for e in EMOTIONS}
        dominant = max(scores, key=scores.get)
        scores[dominant] = round(random.uniform(50, 85), 1)
        return dominant, scores[dominant], scores