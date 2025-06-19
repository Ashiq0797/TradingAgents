import os
import pandas as pd
import numpy as np
import tensorflow as tf
from .utils import fetch_lstm_data, get_model_path
import traceback

def predict_next_close(symbol, range_days=30):
    try:
        symbol = symbol.upper()
        model_path = get_model_path(symbol)

        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model not found: {model_path}")

        model = tf.keras.models.load_model(model_path)

        df = fetch_lstm_data(symbol)
        print("📊 Raw fetched data:")
        print(df.head())

        if df.empty:
            raise ValueError("Fetched data is empty")

        if "Close" not in df.columns:
            raise ValueError("Missing 'Close' column in fetched data")

        # ✅ FIX: ensure proper Series input
        close_series = df["Close"]
        if isinstance(close_series, pd.DataFrame):
            close_series = close_series.squeeze()

        df["Close"] = pd.to_numeric(close_series, errors="coerce")
        df.dropna(subset=["Close"], inplace=True)

        if df.shape[0] < 60:
            raise ValueError("Not enough data to make prediction")

        closes = df["Close"].values[-60:]
        if len(closes) != 60:
            raise ValueError("Invalid number of closing prices")

        mean = np.mean(closes)
        std = np.std(closes)
        if std == 0:
            raise ValueError("Standard deviation is zero — can't scale")

        X_scaled = (closes - mean) / std
        X_input = np.array(X_scaled).reshape((1, 60, 1))

        prediction_scaled = model.predict(X_input)[0][0]
        prediction_value = float(prediction_scaled * std + mean)

        history_df = df.tail(range_days)
        history = list(zip(history_df.index.strftime("%Y-%m-%d"), history_df["Close"].tolist()))

        return round(prediction_value, 2), history

    except Exception as e:
        print("🔥 ERROR in predict_next_close()")
        traceback.print_exc()
        raise e
    