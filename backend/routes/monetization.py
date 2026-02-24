from fastapi import APIRouter

router = APIRouter()

@router.get("/monetization/plans")
async def get_plans():
    return {
        "plans": [
            {
                "id": "free",
                "name": "Vikas (Free)",
                "price": 0,
                "features": ["Access to 50+ Central Schemes", "Basic Matching", "Native Support"]
            },
            {
                "id": "pro",
                "name": "Pro",
                "price": 49,
                "features": ["Personalized PDF Guides", "Priority AI Consultation", "SMS Alerts", "Priority Support"]
            },
            {
                "id": "ngo",
                "name": "NGO",
                "price": 499,
                "features": ["Bulk Checks", "Village Dashboard", "10GB Storage", "API Access"]
            }
        ]
    }
