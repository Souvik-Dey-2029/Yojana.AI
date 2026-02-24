from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import joblib
import os
from typing import List, Dict

router = APIRouter()

# Model Path
MODEL_PATH = "ml/rejection_model.joblib"

class ComplianceRequest(BaseModel):
    aadhaar_name_match: int
    income_certificate_valid: int
    bank_account_seeded: int
    address_match: int
    category_certificate_valid: int
    photo_correct: int
    mobile_linked: int
    self_attested_docs: int

class PredictionResults(BaseModel):
    score: float
    risk_level: str
    suggestions: List[str]

@router.post("/predict-application-success", response_model=PredictionResults)
async def predict_success(req: ComplianceRequest):
    if not os.path.exists(MODEL_PATH):
        raise HTTPException(status_code=500, detail="Rejection model not trained.")
    
    try:
        model = joblib.load(MODEL_PATH)
        
        # Prepare Features
        features = [[
            req.aadhaar_name_match,
            req.income_certificate_valid,
            req.bank_account_seeded,
            req.address_match,
            req.category_certificate_valid,
            req.photo_correct,
            req.mobile_linked,
            req.self_attested_docs
        ]]
        
        # Get Probability for [Class 1]
        probs = model.predict_proba(features)
        score = float(probs[0][1] * 100) # Success probability
        
        # Determine Risk Level
        if score >= 80:
            risk_level = "LOW"
        elif score >= 50:
            risk_level = "MEDIUM"
        else:
            risk_level = "HIGH"
            
        # Generate AI Suggestions
        suggestions = []
        if not req.aadhaar_name_match:
            suggestions.append("Update Aadhaar name to match other documents.")
        if not req.income_certificate_valid:
            suggestions.append("Obtain a fresh Income Certificate (issued within 12 months).")
        if not req.bank_account_seeded:
            suggestions.append("Enable DBT (Aadhaar Seeding) in your primary bank account.")
        if not req.address_match:
            suggestions.append("Ensure address consistency across Aadhaar and Ration Card.")
        if not req.category_certificate_valid:
            suggestions.append("Verify your Category Certificate validity and issuer.")
        if not req.photo_correct:
            suggestions.append("Re-upload a clear passport-size photo against a plain background.")
        if not req.mobile_linked:
            suggestions.append("Link your current mobile number with your Aadhaar card.")
        if not req.self_attested_docs:
            suggestions.append("Self-attest all document copies before submission.")
            
        return {
            "score": round(score, 1),
            "risk_level": risk_level,
            "suggestions": suggestions[:4] # Keep it concise
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")
