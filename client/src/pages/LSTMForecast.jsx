import React, { useState } from "react";
import axios from "axios";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
  ReferenceLine,
  Legend,
} from "recharts";

// ✅ Helper to get next forecast date
const getNextDate = (history) => {
  if (!history.length) return "";
  const lastDate = new Date(history[history.length - 1].date);
  lastDate.setDate(lastDate.getDate() + 1);
  return lastDate.toISOString().split("T")[0];
};

const LSTMForecast = () => {
  const [symbol, setSymbol] = useState("");
  const [price, setPrice] = useState(null);
  const [history, setHistory] = useState([]);
  const [error, setError] = useState("");
  const [range, setRange] = useState(30); // 30-day default

  const handleForecast = async () => {
    try {
      setError("");

      const response = await axios.post("http://localhost:5000/lstm_forecast", {
        symbol,
        range,
      });

      const { prediction, history } = response.data;

      console.log("Prediction from backend:", prediction);
      console.log("History from backend:", history);

      if (typeof prediction === "number" && !isNaN(prediction)) {
        setPrice(prediction);
      } else {
        console.warn("Prediction missing or invalid from backend");
        setPrice(null);
      }

      setHistory(history.map(([date, value]) => ({ date, value })));
    } catch (err) {
      console.error("Error fetching forecast:", err);
      setError("Failed to fetch forecast. Please try again.");
      setPrice(null);
      setHistory([]);
    }
  };

  const handleExportCSV = () => {
    if (!history.length) return;

    const csvRows = [
      ["Date", "Close"],
      ...history.map(({ date, value }) => [date, value])
    ];

    const blob = new Blob([csvRows.map(e => e.join(",")).join("\n")], {
      type: "text/csv"
    });

    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `${symbol}_forecast_history.csv`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="container mt-4">
      <h2 className="mb-3 d-flex align-items-center">
        <span role="img" aria-label="chart" className="me-2">📉</span> LSTM Forecast
      </h2>

      <div className="d-flex align-items-center mb-3 gap-2">
        <input
          type="text"
          className="form-control"
          placeholder="Stock Symbol"
          style={{ width: "200px" }}
          value={symbol}
          onChange={(e) => setSymbol(e.target.value)}
        />
        <button
          className="btn btn-success"
          onClick={handleForecast}
          disabled={!symbol}
        >
          Get LSTM Forecast
        </button>
        <button
          className="btn btn-primary"
          onClick={handleExportCSV}
          disabled={history.length === 0}
        >
          Export CSV
        </button>
      </div>

      <div className="mb-3">
        <span role="img" aria-label="range">📊</span> View Range:
        <input
          type="radio"
          className="form-check-input mx-2"
          name="range"
          checked={range === 30}
          onChange={() => setRange(30)}
        />
        <label className="me-3">30 Days</label>
        <input
          type="radio"
          className="form-check-input mx-2"
          name="range"
          checked={range === 90}
          onChange={() => setRange(90)}
        />
        <label>90 Days</label>
      </div>

      {error && <div className="alert alert-danger">{error}</div>}

      {typeof price === "number" && !isNaN(price) && (
        <div className="alert alert-success">
          Predicted next close price for <strong>{symbol.toUpperCase()}</strong>: ${Number(price).toFixed(2)}
        </div>
      )}

      {history.length > 0 && (
        <div className="mt-4">
          <h5 className="mb-3">
            <span role="img" aria-label="graph" className="me-2">📉</span> Recent {range}-Day Close Prices
          </h5>
          <ResponsiveContainer width="100%" height={300}>
  <LineChart data={history}>
    <CartesianGrid strokeDasharray="3 3" />
    <XAxis
      dataKey="date"
      angle={-45}
      textAnchor="end"
      height={80}
      interval={0}
      label={{
    value: "Date",
    position: "insideBottom",
    offset: -5,
    fill: "#555",
    fontSize: 14,
  }}
    />
    <YAxis
      domain={[
        (dataMin) => Math.floor(dataMin - 10),
        (dataMax) => Math.ceil(Math.max(dataMax, price ? price + 10 : dataMax))
      ]}
      label={{
      value: "Price",
      angle: -90,
      position: "insideLeft",
      offset: 0,
      fill: "#555",
      fontSize: 14,
    }}
    />
    <Tooltip />
    <Legend verticalAlign="top" height={36} />
    {/* Actual Close Price Line */}
    <Line
      type="monotone"
      dataKey="value"
      stroke="#82ca9d"
      strokeWidth={2}
      dot={{ r: 2 }}
      name="Close Price"
    />
    {/* Predicted Price Line as ReferenceLine (horizontal) */}
    {typeof price === "number" && !isNaN(price) && (
      <>
        <ReferenceLine
          y={price}
          stroke="#FF5733"
          strokeDasharray="5 5"
          label={{
            value: `Predicted: $${price.toFixed(2)}`,
            position: "right",
            fill: "#FF5733",
            fontSize: 12,
          }}
        />
        <ReferenceLine
          x={getNextDate(history)}
          stroke="#FF5733"
          strokeDasharray="5 5"
          label={{
            value: "Prediction Day",
            position: "top",
            fill: "#FF5733",
            fontSize: 12,
          }}
        />
      </>
    )}
  </LineChart>
</ResponsiveContainer>


        </div>
      )}
    </div>
  );
};

export default LSTMForecast;
