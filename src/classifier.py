import onnxruntime as rt
import numpy as np

class ChronosClassifier:
    def __init__(self, model_path="models/svm.onnx"):
        self.session = rt.InferenceSession(model_path)
        self.input_name = self.session.get_inputs()[0].name

    def predict(self, feature_vector):
        # Prepare vector for ONNX (expects [batch_size, features])
        input_data = feature_vector.reshape(1, 21)
        
        # Run Offline Inference
        raw_result = self.session.run(None, {self.input_name: input_data})
        
        # Get probability of 'Real' (index 1)
        trust_score = float(raw_result[1][0][1]) 
        return trust_score