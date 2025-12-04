import numpy as np
import os
import tensorflow as tf
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D, LSTM, TimeDistributed, Input, BatchNormalization

# --- CONFIGURATION ---
BASE_PATH = 'mira/script/'
EPOCHS = 20
BATCH_SIZE = 8

def load_data(name):
    """Safely loads numpy arrays if they exist."""
    x_path = os.path.join(BASE_PATH, f'X_{name}.npy')
    y_path = os.path.join(BASE_PATH, f'y_{name}.npy')
    
    if os.path.exists(x_path) and os.path.exists(y_path):
        print(f"[{name.upper()}] Data found. Loading...")
        X = np.load(x_path)
        y = np.load(y_path)
        return X, y
    else:
        print(f"[{name.upper()}] Data NOT found. Skipping model.")
        return None, None

def build_tabular_model(input_dim):
    """The Logic Brain (Dense Neural Network)"""
    model = Sequential([
        Dense(64, activation='relu', input_shape=(input_dim,)),
        BatchNormalization(),
        Dropout(0.3),
        Dense(32, activation='relu'),
        Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

def build_video_model(input_shape):
    """The Visual Brain (Time-Distributed CNN + LSTM)"""
    # input_shape = (10 frames, 64 height, 64 width, 3 channels)
    model = Sequential([
        # Spatial Feature Extraction (Process each frame)
        TimeDistributed(Conv2D(32, (3, 3), activation='relu'), input_shape=input_shape),
        TimeDistributed(MaxPooling2D((2, 2))),
        TimeDistributed(Flatten()),
        
        # Temporal Analysis (Process the sequence of frames)
        LSTM(64, return_sequences=False),
        Dropout(0.4),
        
        Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

def build_audio_model(input_shape):
    """The Auditory Brain (2D CNN for Spectrograms/MFCCs)"""
    # input_shape = (13 MFCCs, 130 Time Steps, 1 Channel)
    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', padding='same', input_shape=input_shape),
        MaxPooling2D((2, 2)),
        Dropout(0.2),
        
        Conv2D(64, (3, 3), activation='relu', padding='same'),
        MaxPooling2D((2, 2)),
        Flatten(),
        
        Dense(32, activation='relu'),
        Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

def train_mira_core():
    print("--- MIRA AI: TRAINING PROTOCOL INITIATED ---")
    
    # 1. Train Tabular Model
    X_tab, y_tab = load_data('tab')
    if X_tab is not None:
        print(f"Training Logic Model on {X_tab.shape} samples...")
        model_tab = build_tabular_model(X_tab.shape[1])
        model_tab.fit(X_tab, y_tab, epochs=EPOCHS, batch_size=BATCH_SIZE, verbose=1)
        model_tab.save(os.path.join(BASE_PATH, 'mira_tab.h5'))
        print(">> Logic Model Saved.")

    # 2. Train Video Model
    X_vid, y_vid = load_data('video')
    if X_vid is not None:
        print(f"Training Visual Model on {X_vid.shape} samples...")
        # Shape: (N, 10, 64, 64, 3)
        model_vid = build_video_model((10, 64, 64, 3)) 
        model_vid.fit(X_vid, y_vid, epochs=EPOCHS, batch_size=4, verbose=1)
        model_vid.save(os.path.join(BASE_PATH, 'mira_video.h5'))
        print(">> Visual Model Saved.")

    # 3. Train Audio Model
    X_aud, y_aud = load_data('audio')
    if X_aud is not None:
        print(f"Training Auditory Model on {X_aud.shape} samples...")
        # Shape: (N, 13, 130, 1)
        model_aud = build_audio_model((13, 130, 1))
        model_aud.fit(X_aud, y_aud, epochs=EPOCHS, batch_size=BATCH_SIZE, verbose=1)
        model_aud.save(os.path.join(BASE_PATH, 'mira_audio.h5'))
        print(">> Auditory Model Saved.")

    print("\n--- TRAINING COMPLETE. BRAINS SAVED. ---")

if __name__ == "__main__":
    train_mira_core()