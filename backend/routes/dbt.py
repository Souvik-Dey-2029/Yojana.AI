"""
DBT (Direct Benefit Transfer) Checker Route
Checks which of a user's eligible schemes pay via DBT,
and whether their bank is compatible with receiving DBT payments.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from backend.database import get_db
from backend.db_models import Scheme

router = APIRouter()

# All scheduled banks in India are DBT-compatible.
# This list covers the major ones users are likely to enter.
SCHEDULED_BANKS = {
    "state bank of india", "sbi",
    "bank of baroda", "bob",
    "punjab national bank", "pnb",
    "canara bank",
    "union bank of india",
    "bank of india", "boi",
    "central bank of india",
    "indian bank",
    "indian overseas bank",
    "uco bank",
    "bank of maharashtra",
    "punjab & sind bank",
    "hdfc bank", "hdfc",
    "icici bank", "icici",
    "axis bank",
    "kotak mahindra bank", "kotak",
    "yes bank",
    "indusind bank",
    "idfc first bank", "idfc",
    "federal bank",
    "south indian bank",
    "karur vysya bank",
    "city union bank",
    "bandhan bank",
    "au small finance bank", "au bank",
    "equitas small finance bank",
    "ujjivan small finance bank",
    "jana small finance bank",
    "fincare small finance bank",
    "post office savings bank", "india post payments bank", "ippb",
    "paytm payments bank",
    "airtel payments bank",
    "gramin bank", "regional rural bank", "rrb",
    "cooperative bank",
    "nainital bank",
    "dhanlaxmi bank",
    "karnataka bank",
    "catholic syrian bank",
    "tamilnad mercantile bank",
    "dcb bank",
    "rbl bank",
    "idbi bank", "idbi",
    "corporation bank",
    "andhra bank",
    "allahabad bank",
    "syndicate bank",
    "vijaya bank",
    "dena bank",
}

# Seeding checklist steps (generic, applies to all banks)
SEEDING_CHECKLIST = [
    {
        "step": 1,
        "title": "Link Aadhaar to Bank Account",
        "detail": "Visit your bank branch or use your bank's mobile app/internet banking to link your Aadhaar number to your savings account.",
        "icon": "🔗"
    },
    {
        "step": 2,
        "title": "Verify Mobile Number",
        "detail": "Ensure the mobile number registered with your bank matches the one linked to your Aadhaar (used for OTP verification).",
        "icon": "📱"
    },
    {
        "step": 3,
        "title": "Activate DBT on Account",
        "detail": "Inform your bank that you want to receive DBT benefits. For joint accounts, Aadhaar should be seeded for the primary account holder.",
        "icon": "✅"
    },
    {
        "step": 4,
        "title": "Check NPCI Mapper Status",
        "detail": "Visit any bank branch and ask them to verify your Aadhaar is mapped on the NPCI (National Payments Corporation of India) mapper — this is the gateway for all DBT transfers.",
        "icon": "🏦"
    },
    {
        "step": 5,
        "title": "Keep Account Active",
        "detail": "Ensure your bank account is not dormant. Transact at least once every 12 months to keep it active for DBT credit.",
        "icon": "💳"
    }
]


class DBTCheckRequest(BaseModel):
    bank_name: str
    account_type: str  # "Savings" or "Current"
    eligible_scheme_ids: List[str] = []


class DBTSchemeResult(BaseModel):
    id: str
    name: str
    icon: str
    benefits: str
    category: str


class DBTCheckResponse(BaseModel):
    bank_name: str
    account_type: str
    is_bank_compatible: bool
    compatibility_note: str
    dbt_schemes: List[DBTSchemeResult]
    total_dbt_schemes: int
    seeding_checklist: list


@router.post("/dbt-check", response_model=DBTCheckResponse)
async def check_dbt_compatibility(request: DBTCheckRequest, db: Session = Depends(get_db)):
    """
    Given a bank name, account type, and the user's eligible scheme IDs,
    returns which schemes are DBT-linked and whether the bank supports DBT.
    """
    bank_lower = request.bank_name.strip().lower()

    # Check bank compatibility
    is_compatible = any(known in bank_lower for known in SCHEDULED_BANKS)

    if is_compatible:
        compatibility_note = (
            f"✅ {request.bank_name.title()} is a Scheduled Bank and is fully compatible "
            f"with the Government of India's DBT framework. You can receive direct benefit "
            f"transfers to your {request.account_type} account once Aadhaar is seeded."
        )
    else:
        # Try partial match for common abbreviations
        words = bank_lower.split()
        is_compatible = any(
            any(known_word in word or word in known_word for word in words)
            for known_word in SCHEDULED_BANKS
        )
        if is_compatible:
            compatibility_note = (
                f"✅ {request.bank_name.title()} appears to be a Scheduled/Recognised Bank "
                f"compatible with DBT. Please confirm with your branch that your Aadhaar is seeded."
            )
        else:
            compatibility_note = (
                f"⚠️ '{request.bank_name}' could not be verified as a Scheduled Bank. "
                f"Only RBI-recognised Scheduled Banks can receive DBT payments. "
                f"Please check spellings, or open a Jan Dhan account at any nationalised bank."
            )

    # Fetch DBT-enabled schemes the user is eligible for
    dbt_schemes = []
    if request.eligible_scheme_ids:
        schemes = db.query(Scheme).filter(
            Scheme.id.in_(request.eligible_scheme_ids),
            Scheme.is_dbt == True
        ).all()
    else:
        # If no IDs provided, show all DBT schemes as a discovery mode
        schemes = db.query(Scheme).filter(Scheme.is_dbt == True).all()

    for s in schemes:
        dbt_schemes.append(DBTSchemeResult(
            id=s.id,
            name=s.name,
            icon=s.icon or "📋",
            benefits=s.benefits,
            category=s.category
        ))

    return DBTCheckResponse(
        bank_name=request.bank_name.title(),
        account_type=request.account_type,
        is_bank_compatible=is_compatible,
        compatibility_note=compatibility_note,
        dbt_schemes=dbt_schemes,
        total_dbt_schemes=len(dbt_schemes),
        seeding_checklist=SEEDING_CHECKLIST
    )
