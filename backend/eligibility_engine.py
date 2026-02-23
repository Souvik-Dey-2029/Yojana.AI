import os
import joblib
import pandas as pd
from backend.db_models import Scheme
from backend.models import UserProfile, SchemeResult
from sqlalchemy.orm import Session

class EligibilityEngine:
    """
    Core logic engine that determines user eligibility for various schemes.
    Utilizes a hybrid approach:
    1. ML-based classification (Decision Trees) for pattern recognition.
    2. Rule-based strict validation against database parameters.
    """
    def __init__(self):
        self.model_path = os.path.join(os.getcwd(), "ml", "model.pkl")
        self.model_data = None
        if os.path.exists(self.model_path):
            try:
                self.model_data = joblib.load(self.model_path)
            except Exception as e:
                print(f"Error loading model: {e}")

    def predict_eligibility(self, profile: UserProfile, db: Session) -> list:
        eligible_ids = []
        
        # 1. ML Prediction (Primary)
        # ... (same ML logic as before, just for IDs)
        if self.model_data:
            try:
                input_df = pd.DataFrame([{
                    "age": profile.age,
                    "income_lpa": profile.income_lpa,
                    "gender": profile.gender,
                    "state": profile.state,
                    "occupation": profile.occupation,
                    "education": profile.education,
                    "category": profile.category,
                    "land_owned": profile.land_owned,
                    "disability": profile.disability
                }])

                input_encoded = input_df.copy()
                for col, le in self.model_data['encoders'].items():
                    try:
                        input_encoded[col] = le.transform(input_df[col])
                    except:
                        input_encoded[col] = 0 

                preds = self.model_data['model'].predict(input_encoded)
                # Note: This list must match the one in train_model.py
                # In production, we'd fetch these IDs from a Config/DB table
                scheme_ids = [
                    'pm_kisan', 'swami_vivekananda_scholarship', 'mudra_loan', 
                    'kanyashree', 'ews_scholarship', 'skill_india', 
                    'startup_india_seed', 'pm_awas_yojana'
                ]
                
                for idx, val in enumerate(preds[0]):
                    if val == 1:
                        eligible_ids.append(scheme_ids[idx])
            except Exception as e:
                print(f"ML prediction failed: {e}")

        # 2. Rule-based Validation (using DB)
        final_eligible_schemes = []
        schemes_from_db = db.query(Scheme).all()
        
        for scheme_obj in schemes_from_db:
            scheme = scheme_obj.__dict__
            is_eligible = True
            
            # Rule: Income check
            if profile.income_lpa * 100000 > scheme.get("max_income", 99999999):
                is_eligible = False
            
            # Rule: State check
            if scheme["eligible_states"] and "All" not in scheme["eligible_states"] and profile.state not in scheme["eligible_states"]:
                is_eligible = False
                
            # Rule: Occupation check
            if scheme["eligible_occupations"] and "All" not in scheme["eligible_occupations"] and profile.occupation not in scheme["eligible_occupations"]:
                is_eligible = False

            # Rule: Gender check
            if scheme.get("gender") and scheme["gender"] != profile.gender:
                is_eligible = False
                
            # Rule: Age check
            if scheme.get("min_age") and profile.age < scheme["min_age"]:
                is_eligible = False
            if scheme.get("max_age") and profile.age > scheme["max_age"]:
                is_eligible = False
                
            # Rule: Land owned
            if scheme.get("land_owned_required", False) and not profile.land_owned:
                is_eligible = False

            if is_eligible:
                # Convert DB model to SchemeResult pydantic model
                final_eligible_schemes.append(SchemeResult(
                    id=scheme["id"],
                    name=scheme["name"],
                    icon=scheme.get("icon", "📋"),
                    description=scheme["description"],
                    benefits=scheme["benefits"],
                    required_documents=scheme["required_documents"],
                    deadline=scheme["deadline"],
                    apply_url=scheme["apply_url"],
                    popularity=scheme.get("popularity", 0)
                ))
        
        return final_eligible_schemes
