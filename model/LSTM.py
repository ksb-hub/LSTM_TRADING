import numpy as np
import matplotlib.pyplot as plt
import preprocessing
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout


df = preprocessing.load_data()
preprocessing.drop_field(df)
preprocessing.dig_encode(df)
X_train, X_test, y_train, y_test = preprocessing.split_and_scale(df)

X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)
X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)

window_size = 21
batch_size = 32

model = Sequential()
model.add(LSTM(units=128, activation='relu', input_shape=(window_size, 1)))
model.add(Dropout(0.2))
model.add(Dense(units=1, activation='sigmoid'))

model.compile(loss="binary_crossentropy", optimizer="adam")
model.fit(X_train, y_train, epochs=50, batch_size=batch_size)

prediction = model.predict(X_test)

print(prediction)
