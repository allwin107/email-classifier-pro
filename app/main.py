import os
from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import joblib
from app.pii_masker import PIIMasker

# 1. Define the Input/Output
class EmailRequest(BaseModel):
    text: str

class EmailResponse(BaseModel):
    original_text: str
    masked_text: str
    category: str
    confidence_score: float

# 2. Initialize App
app = FastAPI(title="Enterprise PII & Classification API")
security = HTTPBearer() # This handles the "Bearer Token" security standard

# 3. Global Variables
model = None
masker = None

@app.on_event("startup")
def load_resources():
    global model, masker
    masker = PIIMasker()
    model = joblib.load("models/email_classifier.pkl")
    print("✅ System Ready!")

# ================= SECURITY LAYER =================
def verify_api_key(credentials: HTTPAuthorizationCredentials = Security(security)):
    """
    The Bouncer. checks if the token matches our secret password.
    """
    token = credentials.credentials
    # We get the real password from the Environment Variables (Secure Storage)
    correct_key = os.getenv("API_SECRET", "default_insecure_key")
    
    if token != correct_key:
        raise HTTPException(status_code=403, detail="⛔ Access Denied: Invalid API Key")
    return token
# ==================================================

@app.post("/classify", response_model=EmailResponse)
def classify_email(request: EmailRequest, token: str = Depends(verify_api_key)):
    """
    Now this endpoint requires a valid API Key to work!
    """
    clean_text = masker.mask_all(request.text)
    prediction = model.predict([clean_text])[0]
    probs = model.predict_proba([clean_text])[0]
    confidence = max(probs)
    
    return {
        "original_text": request.text,
        "masked_text": clean_text,
        "category": prediction,
        "confidence_score": round(confidence, 4)
    }

@app.get("/")
def health_check():
    return {"status": "running", "message": "Email Classifier is online. Auth required for /classify."}