# 🛡️ AI-Based Network Intrusion Detection System (NIDS)

An AI-powered Network Intrusion Detection System (NIDS) developed using Machine Learning and Deep Learning techniques to detect and classify malicious network traffic. The application is built with **Python** and **Streamlit** and provides an interactive dashboard for cybersecurity analysis.

---

## 📌 Project Overview

This project analyzes network traffic data and predicts whether a connection is **Normal** or belongs to a specific cyber attack category using multiple AI models.

The dashboard allows users to:

- Upload network traffic datasets
- Detect malicious traffic
- Compare multiple AI models
- Visualize attack statistics
- Explain predictions using SHAP Explainable AI
- Download prediction reports

---

## 🚀 Features

✅ Interactive Streamlit Dashboard

✅ Multiple AI Models
- XGBoost
- Random Forest
- CNN-LSTM

✅ Network Attack Detection

✅ Confidence Score for Every Prediction

✅ Attack Type Distribution Graph

✅ SHAP Explainable AI Visualization

✅ CSV Report Download

---

## 📂 Dataset

**Dataset Used**

- NSL-KDD Dataset

The dataset contains 41 network traffic features and various attack classes used for training and evaluation.

---

## 🧠 Machine Learning Models

| Model | Purpose |
|--------|----------|
| Random Forest | Traditional ML baseline |
| XGBoost | High-performance gradient boosting model |
| CNN-LSTM | Deep Learning sequential classifier |

---

## 🛠️ Technologies Used

- Python 3.x
- Streamlit
- Scikit-Learn
- TensorFlow / Keras
- XGBoost
- Pandas
- NumPy
- Matplotlib
- SHAP
- Joblib

---

## 📁 Project Structure

```
AI-NIDS/
│
├── models/
│   ├── random_forest_model.pkl
│   ├── xgboost_model.pkl
│   ├── cnn_lstm_model.keras
│   ├── scaler.pkl
│   ├── target_encoder.pkl
│   └── feature_names.pkl
│
├── app.py
├── requirements.txt
├── README.md
└── sample_data.csv
```

---

## ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/Santunudas/nids_dashbord.git
```

Move into the project directory

```bash
cd nids_dashbord
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
streamlit run app.py
```

---

## 📷 Dashboard

The dashboard provides:

- CSV Upload
- Traffic Preview
- Attack Detection
- Prediction Confidence
- Attack Distribution Charts
- SHAP Explainability
- CSV Download

---

## 📊 Output

The system predicts:

- Normal Traffic
- DoS Attack
- Probe Attack
- R2L Attack
- U2R Attack

Along with confidence scores for every prediction.

---

## 🎯 Future Improvements

- Real-time Packet Capture using Scapy
- Live Traffic Monitoring
- Wireshark Integration
- Email Alert System
- SIEM Integration
- Threat Intelligence API
- User Authentication
- Cloud Deployment (AWS / Azure)

---

## 👨‍💻 Author

**Santunu Das**

B.Tech in Artificial Intelligence & Machine Learning

Interested in:
- Artificial Intelligence
- Cybersecurity
- Machine Learning
- Network Security

GitHub:
https://github.com/Santunudas

---

## 📄 License

This project is developed for educational and research purposes.

---

## ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub.
