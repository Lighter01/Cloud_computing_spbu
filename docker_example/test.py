import pandas as pd
import pickle
import time
from tqdm.notebook import tqdm

from sklearn.datasets import load_iris # Ирисы Фишера
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline


with open('classifier/lib/models/model.pkl', 'rb') as f:
    new_model = pickle.load(f)

target_names = load_iris()['target_names']
X = load_iris()['data']
y = pd.Series(load_iris()['target']).apply(lambda x: target_names[x])

if __name__ == "__main__":
    print(new_model.predict(X))