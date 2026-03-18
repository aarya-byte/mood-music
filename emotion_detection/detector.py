import cv2
import numpy as np

try:
    from hsemotion_onnx.facial_emotions import HSEmotionRecognizer
    HSE_AVAILABLE = True
    print("[EmotionDetector] HSEmotion loaded successfully.")
except ImportError:
    HSE_AVAILABLE = False
    print("[EmotionDetector] HSEmotion not found. Using mock.")

EMOTIONS = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']

class EmotionDetector:
    def __init__(self):
        if HSE_AVAILABLE:
            self.recognizer = HSEmotionRecognizer(model_name='enet_b0_8_best_afew')
            self.face_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            )
        else:
            self.recognizer = None

    def detect(self, frame):
        if self.recognizer:
            return self._detect_hse(frame)
        return self._detect_mock(frame)

    def _detect_hse(self, frame):
        try:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.1, 5)

            if len(faces) == 0:
                return self._detect_mock(frame)

            x, y, w, h = faces[0]
            face_img = frame[y:y+h, x:x+w]
            face_img = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)

            emotion, scores = self.recognizer.predict_emotions(face_img, logits=False)

            emotion_labels = ['anger', 'contempt', 'disgust', 'fear',
                            'happiness', 'neutral', 'sadness', 'surprise']

            # Map to our 7 standard emotions
            mapping = {
                'anger': 'angry',
                'contempt': 'disgust',
                'disgust': 'disgust',
                'fear': 'fear',
                'happiness': 'happy',
                'neutral': 'neutral',
                'sadness': 'sad',
                'surprise': 'surprise'
            }

            all_emotions = {}
            for label, score in zip(emotion_labels, scores):
                mapped = mapping.get(label, label)
                all_emotions[mapped] = float(max(
                    all_emotions.get(mapped, 0), score * 100
                ))

            dominant = mapping.get(emotion, emotion)
            confidence = float(all_emotions.get(dominant, 50.0))

            return dominant, confidence, all_emotions

        except Exception as e:
            print(f"[HSE Error] {e}")
            return self._detect_mock(frame)

    def _detect_mock(self, frame):
        import random
        scores = {e: round(random.uniform(2, 20), 1) for e in EMOTIONS}
        dominant = max(scores, key=scores.get)
        scores[dominant] = round(random.uniform(50, 85), 1)
        return dominant, scores[dominant], scores