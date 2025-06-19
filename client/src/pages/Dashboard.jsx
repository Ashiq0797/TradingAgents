// src/pages/Dashboard.jsx
import React, { useState } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

const stockOptions = ["NVDA", "AAPL", "MSFT", "GOOGL", "TSLA"];

export default function Dashboard() {
  const [symbolInput, setSymbolInput] = useState("NVDA");
  const [dateInput, setDateInput] = useState("2025-06-17");
  const [forecast, setForecast] = useState("");
  const [summary, setSummary] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handlePredict = async () => {
    setError("");
    setForecast("");
    setSummary(null);
    setLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ symbol: symbolInput, date: dateInput }),
      });

      const data = await response.json();
      setLoading(false);

      if (data.error) throw new Error(data.error);

      setForecast(data.decision);
      if (data.summary) setSummary(data.summary);
    } catch (err) {
      setLoading(false);
      setError(err.message || "Something went wrong");
    }
  };

  const chartData = summary
    ? [
        { name: "Open", value: summary.open },
        { name: "High", value: summary.high },
        { name: "Low", value: summary.low },
        { name: "Close", value: summary.close },
      ]
    : [];

  return (
    <div style={{ maxWidth: "700px", margin: "40px auto", textAlign: "center" }}>
      <h1 className="mb-4">📈 TickerTrade Dashboard</h1>

      <div className="mb-3">
        <label>Stock Symbol:&nbsp;</label>
        <select
          value={symbolInput}
          onChange={(e) => setSymbolInput(e.target.value)}
          className="form-select"
        >
          {stockOptions.map((sym) => (
            <option key={sym} value={sym}>
              {sym}
            </option>
          ))}
        </select>
      </div>

      <div className="mb-3">
        <label>Date:&nbsp;</label>
        <input
          type="date"
          value={dateInput}
          onChange={(e) => setDateInput(e.target.value)}
          className="form-control"
        />
      </div>

      <button className="btn btn-primary" onClick={handlePredict}>
        {loading ? "Predicting..." : "Get Forecast"}
      </button>

      {forecast && (
        <>
          <h2 style={{ marginTop: "30px", fontSize: "22px" }}>
            ✅ Decision: <span style={{ color: "green" }}>{forecast}</span>
          </h2>

          {summary && (
            <div
              style={{
                marginTop: "20px",
                textAlign: "left",
                display: "inline-block",
              }}
            >
              <h3>Stock Summary</h3>
              <p>
                <strong>Open:</strong> {summary.open}
              </p>
              <p>
                <strong>High:</strong> {summary.high}
              </p>
              <p>
                <strong>Low:</strong> {summary.low}
              </p>
              <p>
                <strong>Close:</strong> {summary.close}
              </p>
              <p>
                <strong>Volume:</strong> {summary.volume}
              </p>
            </div>
          )}

          <div style={{ marginTop: "40px" }}>
            <h4>📉 Stock Price Chart</h4>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={chartData} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Line type="monotone" dataKey="value" stroke="#8884d8" strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </>
      )}

      {error && <p style={{ color: "red", marginTop: "20px" }}>{error}</p>}
    </div>
  );
}
