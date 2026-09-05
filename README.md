# 🚗 Driver Activity Monitoring AI

### AI-powered Driver Behaviour Analysis using Machine Learning

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://driver-activity-monitoring-ai.streamlit.app/)

## 🌐 Live Demo

👉 https://driver-activity-monitoring-ai.streamlit.app/

---

## 📌 Project Overview

Driver Activity Monitoring AI is a machine learning-based application designed to analyze driving sensor data and identify driver behaviour patterns.

The system uses motion sensor data such as acceleration and gyroscope measurements and classifies driving behaviour into three categories:

- 🟢 NORMAL
- 🟡 SLOW
- 🔴 AGGRESSIVE

The trained XGBoost model is integrated into an interactive Streamlit dashboard where users can upload driving sensor data and receive predictions, safety analysis, visual insights, recommendations, and downloadable reports.

---

## 🎯 Objective

The main objective of this project is to transform raw driving sensor data into understandable driver behaviour insights.

Instead of providing only a machine learning prediction, the application presents the results through an interactive dashboard with:

- Driver behaviour classification
- Safety score
- Driver grade
- Behaviour distribution
- Sensor visualization
- Statistical analysis
- AI-driven recommendations
- Prediction timeline
- Detailed prediction report
- CSV export
- PDF report generation

---

## 🧠 Machine Learning

The project uses **XGBoost** for driver behaviour classification.

### Input Features

The model uses motion sensor features including:

- `AccX`
- `AccY`
- `AccZ`
- `GyroX`
- `GyroY`
- `GyroZ`

### Prediction Classes

| Class | Meaning |
|---|---|
| 🟢 NORMAL | Stable driving behaviour |
| 🟡 SLOW | Slow or cautious driving behaviour |
| 🔴 AGGRESSIVE | Potentially unsafe or aggressive driving behaviour |

The trained model and supporting preprocessing/configuration files are stored in the `model/` directory.

---

## ⚙️ How It Works

```text
Driving Sensor Data
        ↓
CSV Upload
        ↓
Data Preparation
        ↓
Feature Engineering
        ↓
Trained XGBoost Model
        ↓
Driver Behaviour Prediction
        ↓
NORMAL / SLOW / AGGRESSIVE
        ↓
Dashboard Analysis
        ↓
Safety Score + Grade + Insights
        ↓
CSV / PDF Reports