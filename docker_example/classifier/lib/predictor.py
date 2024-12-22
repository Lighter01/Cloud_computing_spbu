from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

import pickle

def get_model(path):
    with open(path, 'rb') as f:
        model = pickle.load(f)
        
    return model

def predict(data, model):
    X = [data['sepal_length'], data['sepal_width'], data['petal_length'], data['petal_width']]
    X = [X]
    print(X)
    return model.predict(X)[0]
