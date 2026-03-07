import os
import numpy as np
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType
from src.features import extract_21d_features

# ABSOLUTE SYSTEM PATHS
BASE_DIR = r"C:\ChronosVoice"
DATA_DIR = os.path.join(BASE_DIR, "data")
MODEL_PATH = os.path.join(BASE_DIR, "models", "svm.onnx")

def load_dataset():
    X, y = [], []
    categories = {'ai_voice': 0, 'real_voice': 1}
    
    for category, label in categories.items():
        folder_path = os.path.join(DATA_DIR, category)
        if not os.path.exists(folder_path):
            continue
            
        print(f"📂 Scanning subfolders in: {category}")
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.lower().endswith(('.wav', '.mp3', '.mp4')):
                    file_path = os.path.join(root, file)
                    try:
                        vector, _ = extract_21d_features(file_path)
                        X.append(vector)
                        y.append(label)
                    except Exception as e:
                        pass # Skipping corrupt files
    return np.array(X), np.array(y)

def train_and_export():
    X, y = load_dataset()
    if len(X) == 0:
        print("🛑 Error: No data found. Check subfolder contents!")
        return

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # C=10.0 provides a tighter boundary to prevent False Positives
    model = SVC(kernel='rbf', probability=True, C=10.0, gamma='auto')
    model.fit(X_train, y_train)
    
    print(f"🎯 New Training Accuracy: {model.score(X_test, y_test) * 100:.2f}%")

    # Exporting updated svm.onnx
    initial_type = [('float_input', FloatTensorType([None, 21]))]
    onx = convert_sklearn(model, initial_types=initial_type, options={'zipmap': False})
    
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    with open(MODEL_PATH, "wb") as f:
        f.write(onx.SerializeToString())
    print(f"🚀 Success! Updated model saved at {MODEL_PATH}")

if __name__ == "__main__":
    train_and_export()