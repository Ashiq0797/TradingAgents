import os
import psycopg2
from dotenv import load_dotenv
from datetime import datetime

# Load the .env file
load_dotenv()

# Get DB URI from environment
DB_URI = os.getenv("DB_URI")

try:
    # Connect to your Supabase PostgreSQL database
    conn = psycopg2.connect(DB_URI)
    cursor = conn.cursor()

    # Define the trade data to insert
    trade_data = {
        "asset": "NVDA",
        "action": "BUY",
        "confidence": 0.93,
        "reason": "Strong technicals and fundamentals",
        "price": 123.45,
        "created_at": datetime.utcnow()
    }

    # Execute the INSERT query
    cursor.execute("""
        INSERT INTO trades (asset, action, confidence, reason, price, created_at)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        trade_data["asset"],
        trade_data["action"],
        trade_data["confidence"],
        trade_data["reason"],
        trade_data["price"],
        trade_data["created_at"]
    ))

    # Commit and close
    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Trade successfully inserted into Supabase!")

except Exception as e:
    print("❌ Database connection failed:", e)
