# TickerTrade: AI-Powered Trading Agent Platform

## 🌐 Overview

TickerTrade is a full-stack AI-powered trading platform designed to forecast stock prices using LSTM neural networks and assist users via an integrated chatbot powered by a large language model (LLM).

### 📊 Features

- LSTM-based stock price forecasting (trained with TensorFlow)
- Real-time chart visualization using React and Recharts
- Chatbot with LLM inference via Ollama (using `mistral` model)
- Toggle for historical data (30-day and 90-day)
- Export forecasts to CSV
- Modern, Bootstrap-based responsive UI

---

## 📆 Tech Stack

### Frontend

- **React** (with Hooks)
- **Bootstrap 5** for styling
- **Recharts** for charting

### Backend

- **Python 3.12**
- **Flask** for RestAPI routing
- **TensorFlow 2.19.0** (LSTM forecasting)
- **PostgreSQL** for database
- **Firebase** (auxiliary support, future extension)

### AI/ML & Inference

- **TensorFlow** for time-series LSTM training
- **Ollama** with `mistral` for LLM chatbot
- No LangChain used; direct model inference

### Infrastructure

- **Docker**
- **Docker Compose**
- **CUDA 12.9** and **cuDNN** (optional for GPU acceleration)

---

## 📅 Installation (Local Dev)

### 1. Clone Repository

```bash
git clone https://github.com/Ashiq0797/TradingAgents.git
cd TradingAgents

Python Setup (Optional: Use virtualenv):

cd server
python -m venv venv
venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt 

Train LSTM Models:
python train_lstm_models.py

Run Flask API:
python main.py

React Frontend:

cd client
npm install
npm start

Future Enhancements:
LLM fine-tuning on financial knowledge

LangChain integration for multi-agent logic

Portfolio tracking and strategy simulation

CI/CD pipeline with GitHub Actions and Docker Hub
