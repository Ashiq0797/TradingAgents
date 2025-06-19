# server/chatbot.py
from flask import Blueprint, request, jsonify
import requests

chatbot_bp = Blueprint("chatbot", __name__)

# Sample static context - ideally this should come dynamically from your app later
SYSTEM_CONTEXT = """
You are a smart assistant for a stock trading app called TradingAgent.
You help users understand stock movements, LSTM-based forecasts,
portfolio insights, and trading decisions in a friendly and accurate way.
Do not give generic answers — respond as if you know the app's functions.
"""

@chatbot_bp.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message", "")

        # Combine system context with user message
        full_prompt = f"{SYSTEM_CONTEXT}\nUser: {user_message}\nAssistant:"

        response = requests.post("http://localhost:11434/api/generate", json={
            "model": "mistral",
            "prompt": full_prompt,
            "stream": False
        })

        result = response.json()
        return jsonify({"response": result.get("response", "No reply")})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
