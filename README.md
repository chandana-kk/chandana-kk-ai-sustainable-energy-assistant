# Smart Energy AI

**AI-Based Web Application for Home Electricity Usage Prediction and Optimization**

A production-ready full-stack smart energy management platform built for final-year AIML engineering projects, portfolio showcases, and research demonstrations.

![Stack](https://img.shields.io/badge/React-19-61DAFB)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688)
![MongoDB](https://img.shields.io/badge/MongoDB-7-47A248)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.18-FF6F00)

## Features

- JWT authentication (login, signup, forgot password)
- Real-time simulated energy monitoring via WebSocket
- LSTM energy prediction & XGBoost optimization recommendations
- NILM-style appliance-level usage estimation
- Multilingual UI (English, Kannada, Hindi, Tamil, Telugu)
- Dark/light mode with glassmorphism dashboard
- Alerts, carbon footprint, PDF reports, AI chatbot
- Admin panel & IoT/MQTT placeholders for ESP32 + SCT-013

## Project Structure

```
smart-energy-ai/
├── frontend/          # React + Tailwind + Framer Motion + Recharts
├── backend/           # FastAPI + Motor (MongoDB)
├── ml_models/         # LSTM, XGBoost training scripts
├── database/          # Schemas & seed scripts
├── .env.example
└── README.md
```

## Prerequisites

- Node.js 18+
- Python 3.10+
- MongoDB 6+ (local or Atlas)

## Quick Start

### 1. Clone & configure

```bash
cp .env.example .env
# Edit MongoDB URL and JWT secret
```

### 2. Backend

```bash
cd backend
python -m venv venv
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate
pip install -r requirements.txt
python run.py
```

API docs: http://localhost:8000/docs

### 3. Train ML models (optional, fallback logic works without)

```bash
cd ml_models
python train_lstm.py
python train_optimizer.py
```

### 4. Seed demo data

```bash
cd database
python seed.py
```

Demo user: `demo@smartenergy.ai` / `demo123`

Create admin: `POST http://localhost:8000/api/v1/admin/seed-admin`

### 5. Frontend

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173

## Environment Variables

| Variable | Description |
|----------|-------------|
| `MONGODB_URL` | MongoDB connection string |
| `JWT_SECRET_KEY` | Secret for JWT signing |
| `CORS_ORIGINS` | Allowed frontend origins |
| `VITE_API_BASE_URL` | Frontend API base URL |

## API Overview

| Endpoint | Description |
|----------|-------------|
| `POST /api/v1/auth/register` | User registration |
| `POST /api/v1/auth/login` | Login |
| `GET /api/v1/energy/live` | Live energy snapshot |
| `GET /api/v1/predictions/{horizon}` | AI predictions |
| `GET /api/v1/recommendations` | Optimization tips |
| `GET /api/v1/alerts` | Smart alerts |
| `WS /ws/energy` | Real-time WebSocket stream |
| `GET /api/v1/settings/report/pdf` | Download PDF report |

## Future Hardware Integration

- MQTT broker config in `.env` (`MQTT_ENABLED=true`)
- `POST /api/v1/iot/readings` for ESP32 sensor data
- WebSocket already streams simulated data; swap with hardware feed

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | React, TypeScript, Tailwind CSS, Framer Motion, Recharts, i18next |
| Backend | FastAPI, Motor, Pydantic, JWT |
| Database | MongoDB |
| ML | TensorFlow (LSTM), XGBoost, Scikit-learn |

## License

MIT — Built for academic and portfolio use.

## Author

Final Year AIML Engineering Project — Smart Sustainable Energy Management
