import os
import pandas as pd
import numpy as np
import psycopg2
from datetime import datetime
from dotenv import load_dotenv
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import io
import csv

from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG
from tradingagents.agents.utils.stock_data import fetch_stock_summary
from server.chatbot import chatbot_bp
from server.lstm_model.predict import predict_next_close

# Load environment variables
load_dotenv()
DB_URI = os.getenv("DB_URI")

# Flask app setup
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.register_blueprint(chatbot_bp)

# Trading Agent setup
config = DEFAULT_CONFIG.copy()
config["deep_think_llm"] = "mistral"
config["quick_think_llm"] = "mistral"
config["max_debate_rounds"] = 1
config["online_tools"] = False
ta = TradingAgentsGraph(debug=False, config=config)

@app.route("/")
def home():
    return "✅ Trading Agent Backend is Running"

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json
        symbol = data.get("symbol", "NVDA")
        date = data.get("date", "2025-06-17")

        stock_summary = fetch_stock_summary(symbol)

        _, decision = ta.propagate(symbol, date)
        simulated_return = 0.1
        ta.reflect_and_remember(simulated_return)

        conn = psycopg2.connect(DB_URI)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO trades (asset, action, created_at)
            VALUES (%s, %s, %s)
        """, (
            symbol,
            decision,
            datetime.utcnow()
        ))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({
            "symbol": symbol,
            "date": date,
            "decision": decision,
            "summary": stock_summary
        })

    except Exception as e:
        import traceback
        print("🔥 Exception in /predict:")
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route("/trades", methods=["GET"])
def get_trades():
    try:
        symbol = request.args.get("symbol", "NVDA")
        conn = psycopg2.connect(DB_URI)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT asset, action, created_at
            FROM trades
            WHERE asset = %s
            ORDER BY created_at DESC
            LIMIT 100
        """, (symbol,))
        results = cursor.fetchall()
        cursor.close()
        conn.close()

        trades = [
            {"asset": row[0], "action": row[1], "created_at": row[2].isoformat()}
            for row in results
        ]
        return jsonify(trades)

    except Exception as e:
        import traceback
        print("🔥 Exception in /trades:")
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

# ✅ FIXED FORECAST ROUTE (corrected version — no params in definition)
@app.route("/forecast", methods=["POST"])
def forecast():
    try:
        data = request.json
        symbol = data.get("symbol", "NVDA")
        prediction = predict_next_close(symbol)
        return jsonify({"symbol": symbol, "next_close_prediction": prediction})
    except Exception as e:
        import traceback
        print("🔥 Exception in /forecast:")
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route("/lstm_forecast", methods=["POST"])
def lstm_forecast():
    data = request.get_json()
    symbol = data.get("symbol", "").upper()
    range_days = data.get("range", 30)

    print(f"Received symbol: {symbol}, range: {range_days}")

    try:
        prediction, history = predict_next_close(symbol, range_days)
        print("Prediction:", prediction)
        print("History:", history[:5])  # only show a few rows
        return jsonify({
            "prediction": prediction,
            "history": history
        })
    except Exception as e:
        print("🔥 Exception in /lstm_forecast:", e)
        return jsonify({"error": str(e)}), 500


@app.route("/export_csv", methods=["POST"])
def export_csv():
    try:
        data = request.get_json()
        symbol = data.get("symbol", "").upper()

        _, history = predict_next_close(symbol)

        if not history:
            raise ValueError("No history available for export.")

        df = pd.DataFrame(history, columns=["Date", "Close"])
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        csv_buffer.seek(0)

        return send_file(
            io.BytesIO(csv_buffer.getvalue().encode("utf-8")),
            mimetype="text/csv",
            download_name=f"{symbol}_forecast_history.csv",
            as_attachment=True
        )
    except Exception as e:
        import traceback
        print("🔥 Exception in /export_csv:")
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

# ✅ Flask app runner
if __name__ == "__main__":
    print("✅ Flask app is starting on http://localhost:5000 ...")
    app.run(debug=True, port=5000, use_reloader=False)
