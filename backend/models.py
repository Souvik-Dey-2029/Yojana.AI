from pydantic import BaseModel
from typing import List, Optional

class UserProfile(BaseModel):
    name: Optional[str] = "User"
    age: int
    income_lpa: float
    gender: str
    state: str
    occupation: str
    education: str
    category: str
    land_owned: bool
    disability: bool
    language: str = "en"

class SchemeResult(BaseModel):
    id: str
    name: str
    icon: Optional[str] = "📋"
    description: str
    benefits: str
    required_documents: List[str]
    deadline: str
    apply_url: str
    popularity: int = 0

class EligibilityResponse(BaseModel):
    eligible_schemes: List[SchemeResult]
