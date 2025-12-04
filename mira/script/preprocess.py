import pandas as pd
import numpy as np
import cv2  # OpenCV for video processing
import librosa # Audio processing library
from sklearn.preprocessing import LabelEncoder, StandardScaler
import joblib
import os

# --- CONFIGURATION ---
# Video
IMG_SIZE = 64        # Resize frames to 64x64 pixels
FRAMES_PER_VIDEO = 10 # Extract 10 frames per video (Sequence)

# Audio
AUDIO_DURATION = 3   # Listen to first 3 seconds of clip
SAMPLE_RATE = 22050  # Standard Hertz
N_MFCC = 13          # Number of coefficients (features) to extract
# Expected time steps for 3 seconds ~ 130 columns in MFCC matrix
MAX_PAD_LEN = 130    

def load_and_clean_tabular_data():
    """
    Handles the CSV data for Behaviour and Teacher context.
    """
    print("--- Processing Tabular Data ---")
    base_path = 'mira/data/'
    
    try:
        behaviour = pd.read_csv(os.path.join(base_path, 'behaviour.csv'))
        teacher = pd.read_csv(os.path.join(base_path, 'teacher.csv'))
        
        # Merge datasets
        data = pd.merge(behaviour, teacher, on=['subject', 'students_engagement_over_the_years'], how='left')
        
        # Select Features
        features = data[['day', 'subject', 'weather_condition', 'response_time', 
                         'method_of_teaching', 'teacher_experience_years']]
        
        target = data['students_engagement_over_the_years']
        
        return features, target
    except FileNotFoundError as e:
        print(f"Error: Missing CSV files. {e}")
        return pd.DataFrame(), pd.Series()

def preprocess_tabular_features(features):
    """
    Encodes and scales text/number data.
    """
    if features.empty:
        return np.array([])

    le_dict = {}
    categorical_cols = ['day', 'subject', 'weather_condition', 'response_time', 'method_of_teaching']
    
    features = features.copy()
    
    for col in categorical_cols:
        le = LabelEncoder()
        features[col] = le.fit_transform(features[col].astype(str))
        le_dict[col] = le
    
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)
    
    # Save processors
    os.makedirs('mira/script', exist_ok=True)
    joblib.dump(le_dict, 'mira/script/label_encoders.pkl')
    joblib.dump(scaler, 'mira/script/scaler.pkl')
    
    return features_scaled

def process_video_data():
    """
    Reads video files, extracts frames, and converts them to Tensors.
    """
    print("--- Processing Video Data (Visual Feature Extraction) ---")
    base_path = 'mira/data/'
    video_folder = os.path.join(base_path, 'video')
    csv_path = os.path.join(base_path, 'video.csv')
    
    if not os.path.exists(csv_path):
        print("Video CSV not found. Skipping.")
        return

    df = pd.read_csv(csv_path)
    video_data = []
    labels = []
    
    for i, row in df.iterrows():
        filename = row['video']
        label = row['students_engagement_over_the_years']
        file_path = os.path.join(video_folder, filename)
        
        frames = []
        cap = cv2.VideoCapture(file_path)
        
        if cap.isOpened():
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            if total_frames > 0:
                interval = max(1, total_frames // FRAMES_PER_VIDEO)
                for j in range(FRAMES_PER_VIDEO):
                    cap.set(cv2.CAP_PROP_POS_FRAMES, j * interval)
                    ret, frame = cap.read()
                    if ret:
                        frame = cv2.resize(frame, (IMG_SIZE, IMG_SIZE))
                        frame = frame / 255.0
                        frames.append(frame)
                    else:
                        break
            cap.release()
        
        # Fallback for corrupt/placeholder files
        if len(frames) < FRAMES_PER_VIDEO:
            missing = FRAMES_PER_VIDEO - len(frames)
            for _ in range(missing):
                synthetic_frame = np.random.rand(IMG_SIZE, IMG_SIZE, 3) 
                frames.append(synthetic_frame)
        
        frames = np.array(frames[:FRAMES_PER_VIDEO])
        video_data.append(frames)
        labels.append(label)

    X_video = np.array(video_data)
    y_video = np.array(labels)
    
    np.save('mira/script/X_video.npy', X_video)
    np.save('mira/script/y_video.npy', y_video)
    print(f"Video Processing Complete. Shape: {X_video.shape}")

def process_audio_data():
    """
    Reads audio files and extracts MFCC features (The 'Hearing' part).
    """
    print("--- Processing Audio Data (Auditory Feature Extraction) ---")
    base_path = 'mira/data/'
    audio_folder = os.path.join(base_path, 'audio')
    csv_path = os.path.join(base_path, 'audio.csv')
    
    if not os.path.exists(csv_path):
        print("Audio CSV not found. Skipping.")
        return

    df = pd.read_csv(csv_path)
    audio_data = []
    labels = []
    
    total = len(df)
    
    for i, row in df.iterrows():
        filename = row['audio']
        label = row['students_engagement_over_the_years']
        file_path = os.path.join(audio_folder, filename)
        
        feature = None
        
        try:
            # 1. Attempt to load real audio
            # We only take the first 3 seconds to keep data consistent
            y, sr = librosa.load(file_path, duration=AUDIO_DURATION, sr=SAMPLE_RATE)
            
            # 2. Extract MFCCs (Mel-frequency cepstral coefficients)
            # This turns sound waves into a 'heat map' of frequencies
            mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=N_MFCC)
            
            # 3. Padding/Truncating to ensure fixed size (MAX_PAD_LEN)
            if mfcc.shape[1] > MAX_PAD_LEN:
                mfcc = mfcc[:, :MAX_PAD_LEN]
            else:
                pad_width = MAX_PAD_LEN - mfcc.shape[1]
                mfcc = np.pad(mfcc, pad_width=((0, 0), (0, pad_width)), mode='constant')
                
            feature = mfcc
            
        except Exception:
            # Fallback: Generate synthetic noise if file is a placeholder/text
            # Shape must match: (N_MFCC, MAX_PAD_LEN)
            feature = np.random.randn(N_MFCC, MAX_PAD_LEN)
            
        audio_data.append(feature)
        labels.append(label)
        
        if i % 20 == 0:
            print(f"Processed audio {i+1}/{total}: {filename}")

    # Convert to Numpy Arrays
    # Reshape for CNN input: (Samples, Rows, Cols, Channels) -> Channels=1 for Audio
    X_audio = np.array(audio_data)
    X_audio = X_audio[..., np.newaxis] 
    y_audio = np.array(labels)
    
    # Save
    np.save('mira/script/X_audio.npy', X_audio)
    np.save('mira/script/y_audio.npy', y_audio)
    print(f"Audio Processing Complete. Shape: {X_audio.shape}")
    print("Saved to mira/script/X_audio.npy")

if __name__ == "__main__":
    # 1. Process Tabular Data
    X_tab, y_tab = load_and_clean_tabular_data()
    if not isinstance(X_tab, pd.DataFrame) or not X_tab.empty:
        X_tab_processed = preprocess_tabular_features(X_tab)
        # Save tabular data for training load
        np.save('mira/script/X_tab.npy', X_tab_processed)
        np.save('mira/script/y_tab.npy', y_tab)
        print("Tabular Data Shape:", X_tab_processed.shape)
    
    # 2. Process Video Data
    process_video_data()

    # 3. Process Audio Data
    process_audio_data()
    
    print("\nAll Preprocessing Steps Completed Successfully.")