from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import joblib
import os
from typing import List, Dict, Optional

router = APIRouter()

# Model Path
MODEL_PATH = "ml/rejection_model.joblib"

# ---------------------------------------------------------------------------
# SCHEME-SPECIFIC DOCUMENT REQUIREMENTS
# Maps each scheme to the compliance fields it actually cares about,
# plus a base_acceptance reflecting real-world scheme difficulty/competition.
# Fields correspond to the 8 compliance questions asked to the user.
# ---------------------------------------------------------------------------
SCHEME_PROFILES = {
    "pm_kisan": {
        "fields": ["aadhaar_name_match", "bank_account_seeded", "address_match", "self_attested_docs"],
        "base_acceptance": 72,
        "doc_count": 3,
    },
    "swami_vivekananda_scholarship": {
        "fields": ["aadhaar_name_match", "income_certificate_valid", "category_certificate_valid", "photo_correct", "self_attested_docs"],
        "base_acceptance": 55,
        "doc_count": 4,
    },
    "mudra_loan": {
        "fields": ["aadhaar_name_match", "address_match", "bank_account_seeded", "self_attested_docs"],
        "base_acceptance": 60,
        "doc_count": 4,
    },
    "kanyashree": {
        "fields": ["aadhaar_name_match", "address_match", "bank_account_seeded", "self_attested_docs"],
        "base_acceptance": 78,
        "doc_count": 4,
    },
    "ayushman_bharat": {
        "fields": ["aadhaar_name_match", "address_match"],
        "base_acceptance": 88,
        "doc_count": 3,
    },
    "pm_awas_yojana": {
        "fields": ["aadhaar_name_match", "income_certificate_valid", "address_match", "self_attested_docs"],
        "base_acceptance": 62,
        "doc_count": 3,
    },
    "pm_ujjwala": {
        "fields": ["aadhaar_name_match", "address_match", "category_certificate_valid", "self_attested_docs"],
        "base_acceptance": 82,
        "doc_count": 3,
    },
    "mgnrega": {
        "fields": ["aadhaar_name_match", "address_match"],
        "base_acceptance": 90,
        "doc_count": 2,
    },
    "pm_shram_yogi": {
        "fields": ["aadhaar_name_match", "bank_account_seeded", "mobile_linked"],
        "base_acceptance": 80,
        "doc_count": 2,
    },
    "nsap_pension": {
        "fields": ["aadhaar_name_match", "income_certificate_valid", "address_match", "self_attested_docs"],
        "base_acceptance": 70,
        "doc_count": 3,
    },
    "pm_matru_vandana": {
        "fields": ["aadhaar_name_match", "bank_account_seeded", "self_attested_docs"],
        "base_acceptance": 84,
        "doc_count": 2,
    },
    "stand_up_india": {
        "fields": ["aadhaar_name_match", "category_certificate_valid", "bank_account_seeded", "self_attested_docs"],
        "base_acceptance": 50,
        "doc_count": 3,
    },
    "pm_vishwakarma": {
        "fields": ["aadhaar_name_match", "bank_account_seeded", "category_certificate_valid", "self_attested_docs"],
        "base_acceptance": 68,
        "doc_count": 3,
    },
    "sukanya_samriddhi": {
        "fields": ["aadhaar_name_match", "self_attested_docs"],
        "base_acceptance": 91,
        "doc_count": 2,
    },
    "pm_poshan": {
        "fields": ["aadhaar_name_match", "address_match"],
        "base_acceptance": 93,
        "doc_count": 2,
    },
    "startup_india_learning": {
        "fields": [],  # Just needs email, near-certain
        "base_acceptance": 97,
        "doc_count": 1,
    },
    "atal_pension": {
        "fields": ["aadhaar_name_match", "bank_account_seeded", "mobile_linked"],
        "base_acceptance": 86,
        "doc_count": 2,
    },
    "pm_svanidhi": {
        "fields": ["aadhaar_name_match", "address_match", "mobile_linked", "self_attested_docs"],
        "base_acceptance": 74,
        "doc_count": 3,
    },
    "lakhpati_didi": {
        "fields": ["aadhaar_name_match", "income_certificate_valid", "self_attested_docs"],
        "base_acceptance": 69,
        "doc_count": 3,
    },
    "pm_surya_ghar": {
        "fields": ["aadhaar_name_match", "address_match", "self_attested_docs"],
        "base_acceptance": 71,
        "doc_count": 3,
    },
    "pm_jan_dhan": {
        "fields": ["aadhaar_name_match", "address_match", "mobile_linked"],
        "base_acceptance": 95,
        "doc_count": 2,
    },
    "pm_jeevan_jyoti": {
        "fields": ["aadhaar_name_match", "bank_account_seeded", "mobile_linked"],
        "base_acceptance": 87,
        "doc_count": 2,
    },
    "pm_suraksha_bima": {
        "fields": ["aadhaar_name_match", "bank_account_seeded", "mobile_linked"],
        "base_acceptance": 89,
        "doc_count": 2,
    },
    "pm_shri": {
        "fields": ["aadhaar_name_match", "address_match"],
        "base_acceptance": 80,
        "doc_count": 1,
    },
    "naps_apprenticeship": {
        "fields": ["aadhaar_name_match", "self_attested_docs"],
        "base_acceptance": 76,
        "doc_count": 2,
    },
    "antyodaya_anna": {
        "fields": ["aadhaar_name_match", "income_certificate_valid", "address_match", "self_attested_docs"],
        "base_acceptance": 66,
        "doc_count": 2,
    },
    "pm_pvtg_mission": {
        "fields": ["aadhaar_name_match", "category_certificate_valid", "self_attested_docs"],
        "base_acceptance": 73,
        "doc_count": 2,
    },
    "agnipath_scheme": {
        "fields": ["aadhaar_name_match", "address_match", "photo_correct", "self_attested_docs"],
        "base_acceptance": 35,
        "doc_count": 3,
    },
    "mahila_samman_savings": {
        "fields": ["aadhaar_name_match", "bank_account_seeded", "self_attested_docs"],
        "base_acceptance": 88,
        "doc_count": 3,
    },
    "pm_ebus_sewa": {
        "fields": ["aadhaar_name_match", "address_match", "self_attested_docs"],
        "base_acceptance": 58,
        "doc_count": 2,
    },
    "pm_fme_scheme": {
        "fields": ["aadhaar_name_match", "income_certificate_valid", "bank_account_seeded", "self_attested_docs"],
        "base_acceptance": 55,
        "doc_count": 3,
    },
    "pm_daksh": {
        "fields": ["aadhaar_name_match", "income_certificate_valid", "category_certificate_valid", "self_attested_docs"],
        "base_acceptance": 72,
        "doc_count": 3,
    },
    "national_overseas_scholarship": {
        "fields": ["aadhaar_name_match", "category_certificate_valid", "photo_correct", "self_attested_docs"],
        "base_acceptance": 45,
        "doc_count": 4,
    },
    "pm_fasal_bima": {
        "fields": ["aadhaar_name_match", "address_match", "bank_account_seeded"],
        "base_acceptance": 85,
        "doc_count": 3,
    },
    "pm_kusum": {
        "fields": ["aadhaar_name_match", "address_match", "bank_account_seeded"],
        "base_acceptance": 78,
        "doc_count": 3,
    },
    "e_shram": {
        "fields": ["aadhaar_name_match", "mobile_linked", "bank_account_seeded"],
        "base_acceptance": 96,
        "doc_count": 2,
    },
    "onorc": {
        "fields": ["aadhaar_name_match", "address_match"],
        "base_acceptance": 94,
        "doc_count": 1,
    },
    "beti_bachao_beti_padhao": {
        "fields": ["aadhaar_name_match", "address_match"],
        "base_acceptance": 91,
        "doc_count": 1,
    },
    "janani_suraksha": {
        "fields": ["aadhaar_name_match", "bank_account_seeded", "category_certificate_valid"],
        "base_acceptance": 88,
        "doc_count": 2,
    },
    "mission_indradhanush": {
        "fields": ["aadhaar_name_match", "address_match"],
        "base_acceptance": 93,
        "doc_count": 1,
    },
    "pm_devine": {
        "fields": ["aadhaar_name_match", "address_match", "self_attested_docs"],
        "base_acceptance": 62,
        "doc_count": 2,
    },
    "sagy": {
        "fields": ["aadhaar_name_match", "address_match"],
        "base_acceptance": 85,
        "doc_count": 1,
    },
    "swachh_bharat_token": {
        "fields": ["aadhaar_name_match", "address_match", "bank_account_seeded"],
        "base_acceptance": 90,
        "doc_count": 2,
    },
    "pm_wani": {
        "fields": ["aadhaar_name_match"],
        "base_acceptance": 95,
        "doc_count": 1,
    },
    "nats_apprenticeship": {
        "fields": ["aadhaar_name_match", "photo_correct", "self_attested_docs"],
        "base_acceptance": 75,
        "doc_count": 2,
    },
    "nmms_scholarship": {
        "fields": ["aadhaar_name_match", "income_certificate_valid", "category_certificate_valid", "self_attested_docs"],
        "base_acceptance": 68,
        "doc_count": 3,
    },
    "pre_matric_minority": {
        "fields": ["aadhaar_name_match", "income_certificate_valid", "category_certificate_valid", "self_attested_docs"],
        "base_acceptance": 76,
        "doc_count": 3,
    },
    "post_matric_minority": {
        "fields": ["aadhaar_name_match", "income_certificate_valid", "category_certificate_valid", "self_attested_docs"],
        "base_acceptance": 74,
        "doc_count": 3,
    },
    "merit_cum_means_minority": {
        "fields": ["aadhaar_name_match", "income_certificate_valid", "category_certificate_valid", "self_attested_docs"],
        "base_acceptance": 70,
        "doc_count": 3,
    },
    "usttad_scheme": {
        "fields": ["aadhaar_name_match", "category_certificate_valid", "self_attested_docs"],
        "base_acceptance": 66,
        "doc_count": 2,
    },
    "svamitva_scheme": {
        "fields": ["aadhaar_name_match", "address_match"],
        "base_acceptance": 89,
        "doc_count": 1,
    },
    "pm_kisan_maandhan": {
        "fields": ["aadhaar_name_match", "bank_account_seeded", "self_attested_docs"],
        "base_acceptance": 84,
        "doc_count": 2,
    },
}

# Default profile for unknown schemes
DEFAULT_PROFILE = {
    "fields": ["aadhaar_name_match", "address_match", "self_attested_docs"],
    "base_acceptance": 70,
    "doc_count": 3,
}


class ComplianceRequest(BaseModel):
    aadhaar_name_match: int
    income_certificate_valid: int
    bank_account_seeded: int
    address_match: int
    category_certificate_valid: int
    photo_correct: int
    mobile_linked: int
    self_attested_docs: int


class SchemeComplianceRequest(BaseModel):
    aadhaar_name_match: int
    income_certificate_valid: int
    bank_account_seeded: int
    address_match: int
    category_certificate_valid: int
    photo_correct: int
    mobile_linked: int
    self_attested_docs: int
    scheme_ids: List[str]


class PredictionResults(BaseModel):
    score: float
    risk_level: str
    suggestions: List[str]


class SchemeScore(BaseModel):
    scheme_id: str
    score: float
    risk_level: str
    suggestions: List[str]


class SchemeScoresResponse(BaseModel):
    scores: Dict[str, SchemeScore]


def _compute_scheme_score(compliance: dict, scheme_id: str) -> dict:
    """
    Computes a scheme-specific acceptance score based on:
    1. Which compliance fields this scheme actually cares about
    2. The base acceptance difficulty for this scheme
    3. User-provided compliance answers for the relevant fields
    """
    profile = SCHEME_PROFILES.get(scheme_id, DEFAULT_PROFILE)
    relevant_fields = profile["fields"]
    base = profile["base_acceptance"]

    # Suggestions for issues found
    suggestions = []
    field_suggestion_map = {
        "aadhaar_name_match": "Ensure your Aadhaar name matches all other documents exactly.",
        "income_certificate_valid": "Obtain a fresh Income Certificate issued within the last 12 months.",
        "bank_account_seeded": "Enable DBT (Aadhaar seeding) in your bank account before applying.",
        "address_match": "Ensure your address is consistent across Aadhaar and Ration Card.",
        "category_certificate_valid": "Renew/verify your Category Certificate (SC/ST/OBC) validity.",
        "photo_correct": "Prepare a new passport-size photo with white background as per guidelines.",
        "mobile_linked": "Link your active mobile number to your Aadhaar at the nearest CSC.",
        "self_attested_docs": "Self-attest all document photocopies with your signature before submission.",
    }

    if not relevant_fields:
        # Scheme with minimal docs (e.g., email only) — near guaranteed if online
        score = float(base)
        risk_level = "LOW"
        return {"score": round(score, 1), "risk_level": risk_level, "suggestions": []}

    # Count how many RELEVANT fields the user is compliant with
    compliant = 0
    for field in relevant_fields:
        val = compliance.get(field, 1)
        if val == 1:
            compliant += 1
        else:
            if field in field_suggestion_map:
                suggestions.append(field_suggestion_map[field])

    compliance_ratio = compliant / len(relevant_fields)

    # Score = base_acceptance * compliance_ratio, with a minimum floor
    # If all relevant docs are fine, score = base_acceptance
    # If some are missing, score drops proportionally
    score = base * compliance_ratio

    # Add a small floor so score never goes to 0 (admin can always help)
    score = max(score, 8.0)
    score = min(score, 98.0)

    if score >= 75:
        risk_level = "LOW"
    elif score >= 45:
        risk_level = "MEDIUM"
    else:
        risk_level = "HIGH"

    return {
        "score": round(score, 1),
        "risk_level": risk_level,
        "suggestions": suggestions[:4],
    }


@router.post("/predict-application-success", response_model=PredictionResults)
async def predict_success(req: ComplianceRequest):
    """Legacy endpoint — returns a single global score (kept for compatibility)."""
    if not os.path.exists(MODEL_PATH):
        raise HTTPException(status_code=500, detail="Rejection model not trained.")

    try:
        model = joblib.load(MODEL_PATH)
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
        probs = model.predict_proba(features)
        score = float(probs[0][1] * 100)

        if score >= 80:
            risk_level = "LOW"
        elif score >= 50:
            risk_level = "MEDIUM"
        else:
            risk_level = "HIGH"

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
            "suggestions": suggestions[:4]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


@router.post("/predict-scheme-scores", response_model=SchemeScoresResponse)
async def predict_scheme_scores(req: SchemeComplianceRequest):
    """
    New endpoint: Returns per-scheme acceptance scores.
    Each scheme gets a unique score based on which documents IT specifically requires
    and whether the user is compliant with those documents.
    """
    compliance = {
        "aadhaar_name_match": req.aadhaar_name_match,
        "income_certificate_valid": req.income_certificate_valid,
        "bank_account_seeded": req.bank_account_seeded,
        "address_match": req.address_match,
        "category_certificate_valid": req.category_certificate_valid,
        "photo_correct": req.photo_correct,
        "mobile_linked": req.mobile_linked,
        "self_attested_docs": req.self_attested_docs,
    }

    scores = {}
    for scheme_id in req.scheme_ids:
        result = _compute_scheme_score(compliance, scheme_id)
        scores[scheme_id] = SchemeScore(
            scheme_id=scheme_id,
            score=result["score"],
            risk_level=result["risk_level"],
            suggestions=result["suggestions"],
        )

    return {"scores": scores}
