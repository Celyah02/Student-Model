# 🎓 Student Performance Prediction API

A Django REST API powered by a machine learning regression model that predicts a student’s **Performance Index** using academic and lifestyle data. This project demonstrates a complete ML workflow from data handling to production deployment.

---

## 🚀 What This Project Does

- Trains a machine learning model using historical student data
- Stores student records in a database
- Exposes a REST API to predict performance for new inputs
- Deploys the API using Gunicorn and Nginx

---

## 🧠 Machine Learning Overview

- **Problem Type:** Supervised Learning (Regression)
- **Algorithm:** Random Forest Regressor
- **Target Variable:** Performance Index

### Input Features
- Hours Studied  
- Previous Scores  
- Extracurricular Activities  
- Sleep Hours  
- Sample Question Papers Practiced  

The trained model is saved using `joblib` and reused for fast predictions.

---

## ⚙️ Tech Stack

- **Backend:** Django, Django REST Framework  
- **ML:** Scikit-learn, Pandas, NumPy  
- **Database:** SQLite (dev), PostgreSQL (prod)  
- **Deployment:** Gunicorn, Nginx  

---

## 🛠️ Setup & Run

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Load dataset
python manage.py shell
from performance.load_data import run
run()

# Train model
from performance.train_model import train
train()

# Start server
python manage.py runserver

🔮 Prediction API

Endpoint

POST /api/predict/


Request Body

{
  "hours_studied": 6,
  "previous_scores": 78,
  "extracurricular": true,
  "sleep_hours": 7,
  "sample_papers": 3
}


Response

{
  "predicted_performance_index": 72.45
}

🌍 Deployment Notes

Store the trained model (model.pkl) securely

Use PostgreSQL for production

Serve Django with Gunicorn behind Nginx

📌 Future Improvements

Add model evaluation metrics

Input validation and error handling

Frontend dashboard for predictions

Docker-based deployment

🧑‍💻 Author

FURAHA NIYONGIRA Celia
Machine Learning & Backend Developer
