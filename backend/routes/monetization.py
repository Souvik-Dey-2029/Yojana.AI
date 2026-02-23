from fastapi import APIRouter

router = APIRouter()

@router.get("/monetization/plans")
async def get_plans():
    return {
        "plans": [
            {
                "id": "free",
                "name": "Free",
                "price": 0,
                "features": ["Eligibility Check", "30+ Schemes", "Multi-language"]
            },
            {
                "id": "pro",
                "name": "Pro",
                "price": 49,
                "features": ["Personalized PDF Guides", "Unlimited OCR", "SMS Alerts", "Priority Support"]
            },
            {
                "id": "ngo",
                "name": "NGO",
                "price": 499,
                "features": ["Bulk Checks", "Village Dashboard", "10GB Storage", "API Access"]
            }
        ]
    }
