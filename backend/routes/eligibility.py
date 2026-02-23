from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from backend.models import UserProfile, EligibilityResponse
from backend.eligibility_engine import EligibilityEngine
from backend.translator import translate_scheme
from backend.database import get_db

router = APIRouter()
engine = EligibilityEngine()

@router.post("/eligibility", response_model=EligibilityResponse)
async def post_eligibility(profile: UserProfile, db: Session = Depends(get_db)):
    try:
        eligible_schemes = engine.predict_eligibility(profile, db)
        
        # Translate if needed
        if profile.language != "en":
            translated_schemes = []
            for scheme in eligible_schemes:
                # Convert SchemeResult back to dict for translator
                scheme_dict = scheme.dict()
                translated_dict = translate_scheme(scheme_dict, profile.language)
                translated_schemes.append(translated_dict)
            return {"eligible_schemes": translated_schemes}
        
        return {"eligible_schemes": eligible_schemes}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
