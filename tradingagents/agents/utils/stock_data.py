import yfinance as yf

def fetch_stock_summary(symbol: str):
    try:
        stock = yf.Ticker(symbol)
        hist = stock.history(period="1d")

        if hist.empty:
            return {"error": "No data found for symbol"}

        latest = hist.iloc[-1]
        return {
            "open": round(latest["Open"], 2),
            "high": round(latest["High"], 2),
            "low": round(latest["Low"], 2),
            "close": round(latest["Close"], 2),
            "volume": int(latest["Volume"]),
        }
    except Exception as e:
        return {"error": str(e)}
