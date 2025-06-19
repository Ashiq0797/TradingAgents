// src/pages/Notifications.jsx
import React, { useEffect, useState } from "react";

export default function Notifications() {
  const [trades, setTrades] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    fetch("http://127.0.0.1:5000/trades?symbol=NVDA")
      .then(res => res.json())
      .then(data => {
        if (data.error) throw new Error(data.error);
        setTrades(data);
      })
      .catch(err => setError(err.message || "Failed to load notifications"));
  }, []);

  return (
    <div className="container">
      <h2 className="mb-4">🔔 Trade Notifications</h2>
      {error && <div className="alert alert-danger">{error}</div>}
      {trades.length === 0 && !error && <p>No recent trades.</p>}

      {trades.map((trade, idx) => (
        <div className="alert alert-info" key={idx}>
          <strong>{trade.asset}</strong> — <em>{trade.action}</em> at{" "}
          {new Date(trade.created_at).toLocaleString()}
        </div>
      ))}
    </div>
  );
}
