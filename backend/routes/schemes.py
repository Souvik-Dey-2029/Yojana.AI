from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.crud import get_schemes

router = APIRouter()

@router.get("/schemes")
async def get_all_schemes(db: Session = Depends(get_db)):
    return get_schemes(db)
