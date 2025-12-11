# Enterprise Email Classification & PII System

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.95-green)
![Streamlit](https://img.shields.io/badge/Streamlit-1.22-red)
![Status](https://img.shields.io/badge/Status-Production-success)

A full-stack AI application designed for enterprise IT support. It automatically classifies incoming emails (Incident vs. Request) and sanitizes sensitive data (PII) to ensure GDPR compliance before processing.

**Live Frontend:** [https://email-classifier-frontend-3n97.onrender.com/](https://email-classifier-frontend-3n97.onrender.com/)  
**Live API Docs:** [https://email-classifier-pro.onrender.com/docs](https://email-classifier-pro.onrender.com/docs)

---

## System Architecture

The project follows a secure microservices architecture:

1.  **Frontend (Streamlit):** User-facing dashboard for submitting emails and visualizing confidence scores.
2.  **API Gateway (FastAPI):** A secure REST API protected by Bearer Token Authentication.
3.  **PII Shield (Spacy + Regex):** A preprocessing layer that detects and masks Credit Cards, Phone Numbers, and Names.
4.  **Inference Engine (Scikit-Learn):** A TF-IDF + Multinomial Naive Bayes model trained on 24,000+ enterprise emails.

---

## Key Features

* **Multilingual Support:** Trained on mixed English/German datasets.
* **Privacy-First:** Automatically redacts phone numbers, emails, and names using NER (Named Entity Recognition).
* **Enterprise Security:** API endpoints are secured via `Authorization: Bearer <SECRET_KEY>`.
* **Real-time Confidence:** Returns a confidence score (0-100%) to help humans decide when to intervene.
* **Stateless Deployment:** Dockerized and deployed via Render for auto-scaling.

---

## Tech Stack

* **Language:** Python 3.11
* **ML Framework:** Scikit-Learn, Pandas, Joblib
* **NLP:** Spacy (`en_core_web_sm`), Regular Expressions
* **Backend:** FastAPI, Uvicorn, Pydantic
* **Frontend:** Streamlit
* **Infrastructure:** Render (Cloud PaaS)

---

## Local Installation

Follow these steps to run the system on your machine.

### 1. Clone the Repository
```bash
git clone [https://github.com/allwin107/email-classifier-pro.git](https://github.com/YOUR_USERNAME/email-classifier-pro.git)
cd email-classifier-pro
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 4. Set Up Secrets
Create a .env file in the root directory:
```bash
API_SECRET=your_secret_key
API_URL=[http://127.0.0.1:8000](http://127.0.0.1:8000)
API_KEY=your_secret_key
```

### 5. Run the Application

Terminal 1 (Backend):
```bash
uvicorn app.main:app --reload
```
Terminal 2 (Frontend):
```bash
streamlit run app/frontend.py
```

## API Documentation

You can test the API using the automatic Swagger UI at /docs.

Endpoint: `POST /classify`

Headers: `Authorization: Bearer <API_SECRET>`

Request Body:
```bash
{
  "text": "My laptop screen is broken. Call me at 555-0199."
}
```

Response:
```bash
{
  "original_text": "My laptop screen is broken. Call me at 555-0199.",
  "masked_text": "My laptop screen is broken. Call me at [PHONE].",
  "category": "Incident",
  "confidence_score": 0.92
}
```

## Project Structure

email-classifier-pro/
├── app/
│   ├── main.py          # FastAPI Backend Entrypoint
│   ├── frontend.py      # Streamlit Dashboard
│   ├── pii_masker.py    # Privacy Logic (Regex + Spacy)
│   └── train_model.py   # ML Training Pipeline
├── data/
│   └── enterprise_emails.csv  # Training Dataset (Ignored in Git)
├── models/
│   └── email_classifier.pkl   # Serialized Model
├── .env                 # Secrets (Ignored in Git)
├── requirements.txt     # Dependency List
└── README.md            # Documentation

# License
This project is licensed under the MIT License - see the LICENSE file for details.