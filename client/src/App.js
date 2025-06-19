// src/App.js
import React from "react";
import logo from "./assets/tickertrade-logo.png";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import Home from "./pages/Home";
import Notifications from "./pages/Notifications";
import Chatbot from "./pages/Chatbot";
import LSTMForecast from "./pages/LSTMForecast";

function App() {
  return (
    <Router>
      <div className="container py-4">
        {/* Updated Navbar with larger logo */}
        <nav className="mb-4 d-flex align-items-center flex-wrap">
          <img
            src={logo}
            alt="TickerTrade Logo"
            style={{ width: "320px", height: "200px", marginRight: "20px" }}
          />

          <div className="d-flex flex-wrap align-items-center">
            <Link to="/" className="btn btn-outline-primary me-2 mb-2">Home</Link>
            <Link to="/dashboard" className="btn btn-outline-primary me-2 mb-2">Dashboard</Link>
            <Link to="/notifications" className="btn btn-outline-primary me-2 mb-2">Notifications</Link>
            <Link to="/chatbot" className="btn btn-outline-primary me-2 mb-2">Chatbot</Link>
            <Link to="/lstm" className="btn btn-outline-success mb-2">LSTM Forecast</Link>
          </div>
        </nav>

        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/notifications" element={<Notifications />} />
          <Route path="/chatbot" element={<Chatbot />} />
          <Route path="/lstm" element={<LSTMForecast />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
