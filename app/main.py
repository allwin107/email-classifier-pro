from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
from app.pii_masker import PIIMasker

# 1. Define the Input Format (The Contract)
class EmailRequest(BaseModel):
    text: str

# 2. Define the Output Format
class EmailResponse(BaseModel):
    original_text: str
    masked_text: str
    category: str
    confidence_score: float

# 3. Initialize the App
app = FastAPI(title="Enterprise PII & Classification API")

# 4. Global Variables to hold our brains
model = None
masker = None

@app.on_event("startup")
def load_resources():
    """
    Load the heavy AI models once when the server starts.
    This prevents reloading them for every single request (which is slow).
    """
    global model, masker
    print("⏳ Loading AI Models...")
    
    # Load the PII Shield
    masker = PIIMasker()
    
    # Load the Trained Brain
    model = joblib.load("models/email_classifier.pkl")
    print("✅ System Ready!")

@app.post("/classify", response_model=EmailResponse)
def classify_email(request: EmailRequest):
    """
    The main endpoint. 
    Flow: Raw Text -> PII Mask -> Classification -> JSON Response
    """
    # Step 1: Protection (Mask PII)
    clean_text = masker.mask_all(request.text)
    
    # Step 2: Prediction (Ask the Brain)
    # The model expects a list of texts, so we wrap it in [ ]
    prediction = model.predict([clean_text])[0]
    
    # Step 3: Confidence (How sure are we?)
    # model.predict_proba gives probabilities for all classes. We take the max one.
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
    return {"status": "running", "message": "Email Classifier is online."}