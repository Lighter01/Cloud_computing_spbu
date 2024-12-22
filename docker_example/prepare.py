import pandas as pd
import pickle
import time
from tqdm.notebook import tqdm

from sklearn.datasets import load_iris # Ирисы Фишера
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline


target_names = load_iris()['target_names']

X = load_iris()['data']
y = pd.Series(load_iris()['target']).apply(lambda x: target_names[x])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y)

pl = Pipeline([('scaler', StandardScaler()), 
               ('model', RandomForestClassifier())])

pl.fit(X_train, y_train)

with open('classifier/lib/models/model.pkl', 'wb') as file:
    pickle.dump(pl, file)