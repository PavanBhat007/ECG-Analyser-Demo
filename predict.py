import pickle
import numpy as np

model_path = './model.sav'

def predict(features):
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
        
    print("Model loaded successfully!")
    feature_values = np.array([float(value) for value in features.values()], dtype=np.float64).reshape(1, -1)
    
    prediction = model.predict(feature_values)
    print(prediction)
    return prediction
