from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from concurrent.futures import ThreadPoolExecutor
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
            with ThreadPoolExecutor(max_workers=10) as executor:
                # Convert SchemeResult objects to dicts for translation
                scheme_dicts = [scheme.dict() for scheme in eligible_schemes]
                # Map translation tasks
                translated_schemes = list(executor.map(lambda s: translate_scheme(s, profile.language), scheme_dicts))
            
            return {"eligible_schemes": translated_schemes}
        
        return {"eligible_schemes": eligible_schemes}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
