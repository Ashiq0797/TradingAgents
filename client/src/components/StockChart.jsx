// src/components/StockChart.jsx
import React from "react";
import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  Title,
  Tooltip,
  Legend
} from "chart.js";

ChartJS.register(
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  Title,
  Tooltip,
  Legend
);

export default function StockChart({ dataPoints }) {
  const data = {
    labels: dataPoints.map((_, index) => `T${index + 1}`),
    datasets: [
      {
        label: "Price",
        data: dataPoints,
        fill: false,
        borderColor: "rgb(75, 192, 192)",
        tension: 0.1,
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: { position: "top" },
      title: { display: true, text: "Stock Price Over Time" },
    },
  };

  return <Line data={data} options={options} />;
}
