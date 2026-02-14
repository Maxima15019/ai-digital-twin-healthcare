# 🧠 AI Digital Twin Healthcare System

🚀 Live App:  
https://ai-digital-twin-healthcare-9zikzct2mqdsvwy48yx8qd.streamlit.app/

GitHub Repository:  
https://github.com/Maxima15019/ai-digital-twin-healthcare

---

## 📌 Overview

The AI Digital Twin Healthcare System is a Machine Learning–based web application that predicts the risk of major chronic diseases:

- Diabetes
- Heart Disease
- Hypertension

The system creates a virtual “Digital Twin” of a patient using health parameters and applies trained ML models to estimate disease risk in real-time.

This project demonstrates the practical implementation of AI in preventive healthcare.

---

## 🎯 Problem Statement

Chronic diseases like diabetes and cardiovascular disorders are increasing globally. Early detection is critical but often inaccessible or delayed.

This project aims to:

- Provide early disease risk prediction
- Enable preventive healthcare awareness
- Demonstrate AI-based healthcare analytics
- Deploy ML models in a real-world web application

---

## 🏗️ System Architecture

1. User enters health parameters
2. Data is preprocessed using trained scalers
3. Disease-specific ML model predicts probability
4. Risk category is displayed (Low / Medium / High)
5. Data is stored in SQLite database

---

## 🛠️ Technologies Used

- Python
- NumPy
- Pandas
- Scikit-learn
- Streamlit
- SQLite
- Pickle / Joblib

---

## 🤖 Machine Learning Implementation

Separate trained models are used for:

- Diabetes Prediction
- Heart Disease Prediction
- Hypertension Prediction

Evaluation Metrics:

- Accuracy
- Precision
- Recall
- F1 Score
- ROC-AUC

The models are serialized using pickle/joblib and integrated into a real-time Streamlit web application.

---

## 📂 Project Structure

AI-Digital-Twin-Healthcare/
│
├── web_app.py
├── diabetes_model.pkl
├── diabetes_scaler.pkl
├── heart_model.pkl
├── heart_scaler.pkl
├── hypertension_model.pkl
├── hypertension_scaler.pkl
├── requirement.txt
└── README.md

---

## ⚙️ How to Run Locally

### 1️⃣ Clone Repository
git clone https://github.com/Maxima15019/ai-digital-twin-healthcare.git

### 2️⃣ Install Dependencies
pip install -r requirement.txt

### 3️⃣ Run Streamlit App
streamlit run web_app.py

---

## 💡 Key Features

✔ Multi-disease prediction  
✔ Digital Twin healthcare concept  
✔ Real-time risk scoring  
✔ Data preprocessing with scalers  
✔ SQLite database integration  
✔ Cloud deployment via Streamlit  

---

## 🔮 Future Enhancements

- Deep Learning integration
- Explainable AI (SHAP)
- Doctor dashboard
- Cloud database (AWS/Firebase)
- REST API for hospital integration
- IoT wearable device integration

---

## 🎓 Academic Context

This project was developed as an advanced Machine Learning major project to demonstrate real-world AI deployment in healthcare analytics.

---

## 👨‍💻 Author

Maxima15019  
BCA Student  
AI & Machine Learning Enthusiast  

---

⭐ If you found this project useful, consider giving it a star!
