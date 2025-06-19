// src/pages/Home.jsx
import React, { useEffect, useState } from "react";
import { Card, Button, Row, Col } from "react-bootstrap";
import { FaExchangeAlt, FaChartLine, FaServer, FaSun, FaMoon } from "react-icons/fa";

export default function Home() {
  const [totalTrades, setTotalTrades] = useState(0);
  const [darkMode, setDarkMode] = useState(false);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/trades")
      .then((res) => res.json())
      .then((data) => setTotalTrades(data.length))
      .catch(() => setTotalTrades(0));
  }, []);

  useEffect(() => {
    document.body.className = darkMode ? "bg-dark text-light" : "bg-light text-dark";
    document.documentElement.style.backgroundColor = darkMode ? "#212529" : "#f8f9fa"; // fallback for full height
  }, [darkMode]);

  const cardBg = darkMode ? "dark" : "light";

  return (
    <div style={{ padding: "2rem", minHeight: "100vh" }}>
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2><FaChartLine /> TickerTrade Home</h2>
        <Button
          variant={darkMode ? "light" : "dark"}
          onClick={() => setDarkMode(!darkMode)}
        >
          {darkMode ? <FaSun /> : <FaMoon />} {darkMode ? "Light" : "Dark"} Mode
        </Button>
      </div>

      <Row className="mb-4">
        <Col md={4}>
          <Card bg={cardBg} text={darkMode ? "light" : "dark"}>
            <Card.Body>
              <Card.Title><FaExchangeAlt /> Total Trades</Card.Title>
              <Card.Text style={{ fontSize: "24px" }}>{totalTrades}</Card.Text>
            </Card.Body>
          </Card>
        </Col>
        <Col md={4}>
          <Card bg={cardBg} text={darkMode ? "light" : "dark"}>
            <Card.Body>
              <Card.Title><FaChartLine /> Trends</Card.Title>
              <Card.Text>Check the Dashboard for predictions.</Card.Text>
            </Card.Body>
          </Card>
        </Col>
        <Col md={4}>
          <Card bg={cardBg} text={darkMode ? "light" : "dark"}>
            <Card.Body>
              <Card.Title><FaServer /> System Status</Card.Title>
              <Card.Text><span className="text-success">●</span> Online</Card.Text>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </div>
  );
}
