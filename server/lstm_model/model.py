# server/lstm_model/model.py
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler
import joblib
import os

def train_lstm_model(data_path, save_path="server/lstm_model"):
    df = pd.read_csv(data_path)
    df['Close'] = df['Close'].astype(float)

    # Normalize
    scaler = MinMaxScaler()
    scaled = scaler.fit_transform(df[['Close']])
    joblib.dump(scaler, os.path.join(save_path, "scaler.pkl"))

    X, y = [], []
    sequence_len = 60
    for i in range(sequence_len, len(scaled)):
        X.append(scaled[i-sequence_len:i])
        y.append(scaled[i])

    X, y = np.array(X), np.array(y)

    model = Sequential([
        LSTM(50, return_sequences=True, input_shape=(X.shape[1], 1)),
        LSTM(50),
        Dense(1)
    ])

    model.compile(optimizer="adam", loss="mean_squared_error")
    model.fit(X, y, epochs=10, batch_size=32)

    model.save(os.path.join(save_path, "lstm_model.h5"))
