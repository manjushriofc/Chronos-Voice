import librosa
import numpy as np
import os

def extract_21d_features(audio_path):
    # Check if path is valid to prevent hanging
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"File not found: {audio_path}")

    # Load audio (limited to 3s for faster processing)
    y, sr = librosa.load(audio_path, sr=16000, duration=3.0)
    
    # 1. 13 MFCCs
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    mfccs_mean = np.mean(mfccs.T, axis=0)
    
    # 2. Pitch and Jitter - Normalizing for stable human voices
    pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
    pitch_values = pitches[pitches > 0]
    
    # Preventing 0.0 results to avoid robotic flagging
    f0 = np.mean(pitch_values) if len(pitch_values) > 0 else 100.0
    jitter = np.mean(np.abs(np.diff(pitch_values))) if len(pitch_values) > 1 else 0.001
    
    # 3. Spectral Metrics
    zcr = np.mean(librosa.feature.zero_crossing_rate(y))
    rms = np.mean(librosa.feature.rms(y=y))
    spec_con = np.mean(librosa.feature.spectral_contrast(y=y, sr=sr).T, axis=0) 
    
    # Combine into the 21D Vector
    vector = np.hstack([mfccs_mean, [f0, jitter, zcr, rms], spec_con[:4]])
    
    metrics = {
        "mfcc_std": float(np.std(mfccs)),
        "pitch": float(f0),
        "jitter": float(jitter)
    }
    return vector.astype(np.float32), metrics