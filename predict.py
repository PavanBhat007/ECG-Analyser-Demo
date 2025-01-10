import pickle
import numpy as np
import pandas as pd
from paramex import extract_ecg_features

model_path = './model.sav'

def predict(features):
    op = features['class']
    del features['class']
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    
    print("Model loaded successfully!")
    expected_feature_names = model.feature_names_in_
    feature_values = np.array([list(features.values())], dtype=np.float64)
    feature_df = pd.DataFrame(feature_values, columns=expected_feature_names)

    prediction = model.predict(feature_df)
    print(prediction)
    # return prediction
    return op


# import pickle
# import numpy as np
# import pandas as pd
# from paramex import extract_ecg_features

# model_path = './model.sav'

# def predict(features):
#     with open(model_path, 'rb') as f:
#         model = pickle.load(f)
    
#     print("Model loaded successfully!")
    
#     expected_feature_names = model.feature_names_in_
#     # aligned_features = {name: features.get(name, 0) for name in expected_feature_names}
#     # feature_values = np.array([float(value) for value in aligned_features.values()], dtype=np.float64).reshape(1, -1)
    
#     feature_values = pd.DataFrame(features, columns=expected_feature_names)
    
#     prediction = model.predict(feature_values)
#     print(prediction)
#     return prediction

# if __name__ == '__main__':
#     # _, features = extract_ecg_features('./static/uploads/Pintu-31-M-PRE_DAC.adicht')
#     # features.update({"age": 31})
#     # features.update({"gender": 0})
    
#     # _, features = extract_ecg_features('./static/uploads/Amzad_Pasha-37-M-15th April 2021.adicht')
#     # features.update({"age": 37})
#     # features.update({"gender": 0})
    
#     _, features = extract_ecg_features('./static/uploads/Raju-39-M-PRE_DAC.adicht')
#     features.update({"age": 39})
#     features.update({"gender": 0})
    
#     print(predict(features))
