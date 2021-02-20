# -*- coding: utf-8 -*-
"""regresyon/ysa.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1wbgKhYUNUHOpRiEo027wRFTdpKrxarC7
"""

import pandas as pd
import numpy as np

df = pd.read_csv('IMDB-Movie-Data.csv')

df = df.sample(frac = 1)
df = df.reset_index()

df = df.fillna(0)

labels = df['Metascore']
df = df.drop('Metascore', axis=1)
df = df.drop('index', axis=1)
df = df.drop('Rank', axis=1)
df = df.drop('Title', axis=1)
df = df.drop('Genre', axis=1)
df = df.drop('Description', axis=1)
df = df.drop('Director', axis=1)
df = df.drop('Actors', axis=1)
df = df.astype(np.float32)


labels = np.array(labels)
labels.shape

features = df.iloc[:, 0:].values

for i in range(len(df.columns)):
    features[:,i] = list(map(lambda x: ((x-min(features[:,i])) / (max(features[:,i]) - min(features[:,i]))) , features[:,i]))

features = np.array(features)
features.shape

x_train = features[:int((labels.shape[0] * 80) / 100), :]
y_train = labels[:int((labels.shape[0] * 80) / 100)]
x_test = features[int((labels.shape[0] * 80) / 100):, :]
y_test = labels[int((labels.shape[0] * 80) / 100):]
x_train.shape

"""**Regresyon**"""

from sklearn.linear_model import LinearRegression

clf = LinearRegression().fit(x_train, y_train)

y_pred = clf.predict(x_test)

from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
r2_score(y_test,y_pred)

print('MAE  : ', mean_absolute_error(y_test, y_pred))
print('MSE  : ', mean_squared_error(y_test, y_pred))

"""**Yapay Sinir Ağları**"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from keras.models import Sequential
from keras.layers import Dense, Activation
from sklearn.preprocessing import StandardScaler

model = Sequential()
model.add(layers.Dense(8, activation="sigmoid", input_dim=5))
model.add(layers.Dense(16, activation="sigmoid"))
model.add(layers.Dense(32, activation="sigmoid"))
model.add(layers.Dense(64, activation="sigmoid"))
model.add(layers.Dense(128, activation="sigmoid"))
model.add(layers.Dense(64, activation="sigmoid"))
model.add(layers.Dense(1))

model.compile(loss='mean_squared_error', optimizer='adam', metrics=['mae'])

history = model.fit(x_train, y_train, batch_size=64, epochs=2500, validation_split=0.2)

import matplotlib.pyplot as plt
plt.plot(history.history['loss'])


plt.title('Model loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper left')
plt.show()

plt.plot(history.history['mae'])

plt.title('Model mae')
plt.ylabel('mae')
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper left')
plt.show()


print("Test (mse, mae): {}".format(model.evaluate(x=x_test, y=y_test, batch_size=64)))