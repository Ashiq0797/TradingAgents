import os 
import yfinance as yf
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import pandas as pd


def get_model_path(symbol):
    base_path = os.path.join(os.path.dirname(__file__), "models")
    return os.path.join(base_path, f"{symbol}_lstm.keras")

import yfinance as yf

def fetch_lstm_data(symbol, period="3mo", interval="1d"):
    data = yf.download(symbol, period=period, interval=interval)

    # ✅ FLATTEN multi-level columns
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    return data


def fetch_stock_data(symbol="NVDA", period="90d", interval="1d"):
    """
    Fetches stock data from Yahoo Finance for the given symbol.
    Increased period to ensure enough data for LSTM sequence generation.
    """
    data = yf.download(symbol, period=period, interval=interval)
    return data

def scale_data(data):
    """
    Scales the data using MinMaxScaler.
    """
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled = scaler.fit_transform(data)
    return scaled, scaler

def sequence_data(data, seq_length=60):
    """
    Generates sequences of length `seq_length` from the scaled data.
    """
    X, y = [], []
    for i in range(len(data) - seq_length):
        X.append(data[i:i + seq_length])
        y.append(data[i + seq_length])
    return np.array(X), np.array(y)

def prepare_lstm_input(df, method="standard"):
    if df.shape[0] < 60:
        raise ValueError("Not enough data to prepare input (need 60 rows)")

    close_prices = df["Close"].values[-60:].reshape(-1, 1)

    if method == "standard":
        mean = np.mean(close_prices)
        std = np.std(close_prices)
        if std == 0:
            raise ValueError("Standard deviation is zero.")
        scaled = (close_prices - mean) / std
        X_input = scaled.reshape((1, 60, 1))
        return X_input, mean, std

    elif method == "minmax":
        from sklearn.preprocessing import MinMaxScaler
        scaler = MinMaxScaler(feature_range=(0, 1))
        scaled = scaler.fit_transform(close_prices)
        X_input = scaled.reshape((1, 60, 1))
        return X_input, scaler

    else:
        raise ValueError("Invalid method. Choose 'standard' or 'minmax'")
