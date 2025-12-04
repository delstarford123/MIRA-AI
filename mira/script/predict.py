import tensorflow as tf
import numpy as np
import pandas as pd
import joblib
import cv2
import librosa
import os

# --- CONSTANTS ---
IMG_SIZE = 64
FRAMES_PER_VIDEO = 10
AUDIO_DURATION = 3
SAMPLE_RATE = 22050
N_MFCC = 13
MAX_PAD_LEN = 130
BASE_SCRIPT_PATH = 'mira/script/'

class MiraPredictor:
    def __init__(self):
        print("Loading MIRA AI Models...")
        self.models = {}
        self.encoders = None
        self.scaler = None
        
        # 1. Load All Available Brains
        model_files = {
            'tab': 'mira_tab.h5',   # Logic
            'img': 'mira_img.h5',   # Static Images (NEW)
            'video': 'mira_video.h5', # Video
            'audio': 'mira_audio.h5'  # Audio
        }

        for key, filename in model_files.items():
            path = os.path.join(BASE_SCRIPT_PATH, filename)
            if os.path.exists(path):
                self.models[key] = tf.keras.models.load_model(path)
                print(f"Loaded {key.upper()} Brain.")
            else:
                print(f"Warning: {filename} not found. Skipping {key} mode.")

        # 2. Load Data Processors (Scalers)
        enc_path = os.path.join(BASE_SCRIPT_PATH, 'label_encoders.pkl')
        scaler_path = os.path.join(BASE_SCRIPT_PATH, 'scaler.pkl')

        if os.path.exists(enc_path):
            self.encoders = joblib.load(enc_path)
            self.scaler = joblib.load(scaler_path)

    def _preprocess_tabular(self, data_dict):
        if not self.encoders: return None
        df = pd.DataFrame([data_dict])
        for col, le in self.encoders.items():
            try:
                # Handle unknown categories safely
                if str(df[col].values[0]) in le.classes_:
                    df[col] = le.transform(df[col].astype(str))
                else:
                    df[col] = 0 # Default to first class if unknown
            except:
                df[col] = 0
        return self.scaler.transform(df)

    def _preprocess_image(self, img_path):
        """Reads a single image for the AI"""
        try:
            img = cv2.imread(img_path)
            if img is None: return None
            img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
            img = img / 255.0
            # Add batch dimension: (1, 64, 64, 3)
            return np.expand_dims(img, axis=0)
        except:
            return None

    def _preprocess_video(self, video_path):
        frames = []
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened(): return None
        
        total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        interval = max(1, total // FRAMES_PER_VIDEO)
        
        for j in range(FRAMES_PER_VIDEO):
            cap.set(cv2.CAP_PROP_POS_FRAMES, j * interval)
            ret, frame = cap.read()
            if ret:
                frame = cv2.resize(frame, (IMG_SIZE, IMG_SIZE))
                frame = frame / 255.0
                frames.append(frame)
            else: break
        cap.release()
        
        # Pad video if too short
        while len(frames) < FRAMES_PER_VIDEO:
            frames.append(np.zeros((IMG_SIZE, IMG_SIZE, 3)))
            
        return np.array([frames])

    def _preprocess_audio(self, audio_path):
        try:
            y, sr = librosa.load(audio_path, duration=AUDIO_DURATION, sr=SAMPLE_RATE)
            mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=N_MFCC)
            if mfcc.shape[1] > MAX_PAD_LEN: mfcc = mfcc[:, :MAX_PAD_LEN]
            else: mfcc = np.pad(mfcc, ((0,0),(0, MAX_PAD_LEN - mfcc.shape[1])), mode='constant')
            return mfcc.reshape(1, N_MFCC, MAX_PAD_LEN, 1)
        except: return None

    # --- UPDATED FUNCTION SIGNATURE HERE ---
    def predict_engagement(self, tabular_data=None, image_path=None, video_path=None, audio_path=None):
        """
        Calculates weighted engagement score based on available inputs.
        """
        scores = []
        weights = []

        # 1. Logic Prediction
        if tabular_data and 'tab' in self.models:
            input_vec = self._preprocess_tabular(tabular_data)
            if input_vec is not None:
                p = self.models['tab'].predict(input_vec, verbose=0)[0][0]
                scores.append(p)
                weights.append(0.2)

        # 2. Image Prediction (THIS WAS MISSING BEFORE)
        if image_path and 'img' in self.models and os.path.exists(image_path):
            input_img = self._preprocess_image(image_path)
            if input_img is not None:
                p = self.models['img'].predict(input_img, verbose=0)[0][0]
                scores.append(p)
                weights.append(0.4) # High weight for visual snapshot

        # 3. Video Prediction
        if video_path and 'video' in self.models and os.path.exists(video_path):
            input_vid = self._preprocess_video(video_path)
            if input_vid is not None:
                p = self.models['video'].predict(input_vid, verbose=0)[0][0]
                scores.append(p)
                weights.append(0.5)

        # 4. Audio Prediction
        if audio_path and 'audio' in self.models and os.path.exists(audio_path):
            input_aud = self._preprocess_audio(audio_path)
            if input_aud is not None:
                p = self.models['audio'].predict(input_aud, verbose=0)[0][0]
                scores.append(p)
                weights.append(0.3)

        if not scores: return 0.5, "NO_DATA / AI READY"

        final_score = np.average(scores, weights=weights)
        status = "IMPROVING/GOOD (1)" if final_score > 0.5 else "DETERIORATING (0)"
        return final_score, status

if __name__ == "__main__":
    ai = MiraPredictor()
    # Test just to be sure
    print("Test passed.")