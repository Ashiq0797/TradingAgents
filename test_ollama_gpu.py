import os
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
from .utils import fetch_stock_data, scale_data, sequence_data

# Use path-safe separator and absolute model directory
MODEL_DIR = os.path.join("server", "lstm_model", "models")

def predict_next_close(symbol):
    model_filename = f"{symbol.upper()}_lstm.keras"
    model_path = os.path.join(MODEL_DIR, model_filename)

    print("🔍 Looking for:", model_path)

    if not os.path.isfile(model_path):
        raise FileNotFoundError("LSTM model not trained yet. Please train first.")

    # Fetch recent stock data
    df = fetch_stock_data(symbol)
    if df is None or len(df) < 61:
        raise ValueError("Not enough stock data available for prediction.")

    if "Close" not in df.columns:
        raise ValueError("'Close' column missing in stock data.")

    close_prices = df["Close"].values.reshape(-1, 1)
    scaled, scaler = scale_data(close_prices)
    x_seq, _ = sequence_data(scaled, seq_length=60)

    if len(x_seq) == 0:
        raise ValueError("Not enough data to form a prediction sequence.")

    x = x_seq[-1:]  # last 60-day window

    # Load and predict
    model = load_model(model_path, compile=False)
    prediction = model.predict(x)
    if prediction.shape[0] == 0:
        raise ValueError("Prediction failed. Model returned empty output.")

    predicted_price = scaler.inverse_transform(prediction)[0][0]

    # Return last 30 close prices for chart
    historical = list(zip(df.tail(30).index.strftime("%Y-%m-%d"), df["Close"].tail(30)))
    return round(float(predicted_price), 2), historical
