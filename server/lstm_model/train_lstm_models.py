import os
import yfinance as yf
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import joblib

# Save directory (relative to the root project folder)
MODEL_DIR = os.path.join("server", "lstm_model", "models")
os.makedirs(MODEL_DIR, exist_ok=True)

# Config
symbols = ["NVDA", "AAPL", "MSFT", "GOOGL", "TSLA"]
sequence_length = 60


def fetch_data(symbol):
    df = yf.download(symbol, start="2018-01-01", progress=False)
    if "Close" not in df:
        raise ValueError(f"No 'Close' data for {symbol}")
    return df[["Close"]]


def prepare_sequences(data):
    scaler = MinMaxScaler()
    scaled = scaler.fit_transform(data)

    X, y = [], []
    for i in range(sequence_length, len(scaled)):
        X.append(scaled[i - sequence_length:i])
        y.append(scaled[i])
    return np.array(X), np.array(y), scaler


def build_model(input_shape):
    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=input_shape))
    model.add(LSTM(50))
    model.add(Dense(1))
    model.compile(optimizer="adam", loss="mse")
    return model


if __name__ == "__main__":
    for symbol in symbols:
        try:
            print(f"\nTraining model for {symbol}...")
            data = fetch_data(symbol)
            X, y, scaler = prepare_sequences(data)

            model = build_model((X.shape[1], 1))
            model.fit(X, y, epochs=20, batch_size=32, verbose=0)

            model_path = os.path.join(MODEL_DIR, f"{symbol}_lstm.keras")
            scaler_path = os.path.join(MODEL_DIR, f"{symbol}_scaler.save")

            model.save(model_path)
            joblib.dump(scaler, scaler_path)

            print(f"✅ Saved model: {model_path}")
            print(f"✅ Saved scaler: {scaler_path}")
        except Exception as e:
            print(f"❌ Failed for {symbol}: {e}")
