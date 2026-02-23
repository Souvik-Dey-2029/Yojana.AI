from backend.database import SessionLocal, engine, Base
from backend.db_models import Scheme
import json

Base.metadata.create_all(bind=engine)

SCHEMES_LIST = [
    {
        "id": "pm_kisan",
        "name": "PM Kisan Samman Nidhi",
        "icon": "🚜",
        "description": "Financial assistance to small and marginal farmers across the country.",
        "benefits": "₹6,000 per year in three equal installments.",
        "max_income": 300000,
        "eligible_states": ["All"],
        "eligible_occupations": ["Farmer"],
        "eligible_categories": ["All"],
        "land_owned_required": True,
        "required_documents": ["Aadhaar Card", "Bank Passbook", "Land Records"],
        "deadline": "Rolling",
        "apply_url": "https://pmkisan.gov.in/",
        "category": "Agriculture",
        "popularity": 95,
        "guidance_steps": [
            "Visit the official PM-Kisan portal.",
            "Click on 'New Farmer Registration' and enter your Aadhaar number.",
            "Fill in the required land details and upload your passbook.",
            "Submit and note down your reference number for tracking."
        ]
    },
    {
        "id": "swami_vivekananda_scholarship",
        "name": "Swami Vivekananda Merit-cum-Means Scholarship",
        "icon": "🎓",
        "description": "Scholarship for meritorious students from economically weaker sections in West Bengal.",
        "benefits": "Up to ₹60,000 per year depending on course.",
        "max_income": 250000,
        "eligible_states": ["West Bengal"],
        "eligible_occupations": ["Student"],
        "eligible_categories": ["All"],
        "min_age": 15,
        "required_documents": ["Previous Marksheet", "Income Certificate", "Income Affidavit", "Aadhaar Card"],
        "deadline": "31st Dec",
        "apply_url": "https://svmcm.wbhed.gov.in/",
        "category": "Education",
        "popularity": 88,
        "guidance_steps": [
            "Register on the SVMCM portal with your academic details.",
            "Login and fill the detailed application form.",
            "Upload scanned income certificates and marksheets.",
            "Submit and wait for institutional verification."
        ]
    },
    {
        "id": "mudra_loan",
        "name": "Pradhan Mantri Mudra Yojana (PMMY)",
        "icon": "💼",
        "description": "Loans up to ₹10 Lakhs for non-corporate, non-farm small/micro enterprises.",
        "benefits": "Collateral-free loans for starting or expanding businesses.",
        "max_income": 1000000,
        "eligible_states": ["All"],
        "eligible_occupations": ["Business Owner", "Self-Employed", "Entrepreneur"],
        "eligible_categories": ["All"],
        "required_documents": ["Identity Proof", "Address Proof", "Business Project Report", "Bank Statement"],
        "deadline": "Monthly",
        "apply_url": "https://www.mudra.org.in/",
        "category": "Finance",
        "popularity": 92,
        "guidance_steps": [
            "Identify the category (Shishu, Kishore, Tarun) based on loan amount.",
            "Download the Mudra loan application form from the website.",
            "Approach your nearest bank branch with the project report.",
            "Submit documents and complete the KYC process at the bank."
        ]
    },
    {
        "id": "kanyashree",
        "name": "Kanyashree Prakalpa",
        "icon": "👧",
        "description": "Incentivizing schooling and delaying marriage of girl children in West Bengal.",
        "benefits": "Annual scholarship and a one-time grant of ₹25,000.",
        "max_income": 120000,
        "eligible_states": ["West Bengal"],
        "eligible_occupations": ["Student"],
        "eligible_categories": ["All"],
        "gender": "Female",
        "min_age": 13,
        "max_age": 19,
        "required_documents": ["Birth Certificate", "Unmarried Declaration", "Aadhaar Card", "Bank Passbook"],
        "deadline": "Dec 31",
        "apply_url": "https://www.wbkanyashree.gov.in/",
        "category": "Social Welfare",
        "popularity": 85
    },
    {
        "id": "ayushman_bharat",
        "name": "Ayushman Bharat (PM-JAY)",
        "icon": "🏥",
        "description": "World's largest health insurance scheme fully financed by the government.",
        "benefits": "Health cover of ₹5 Lakh per family per year for secondary and tertiary care hospitalization.",
        "max_income": 600000,
        "eligible_states": ["All"],
        "eligible_occupations": ["All"],
        "eligible_categories": ["All"],
        "required_documents": ["Aadhaar", "Ration Card", "Identity Proof"],
        "deadline": "Open",
        "apply_url": "https://pib.gov.in/PressReleasePage.aspx?PRID=1951508",
        "category": "Health",
        "popularity": 98
    },
    {
        "id": "pm_awas_yojana",
        "name": "PM Awas Yojana (PMAY)",
        "icon": "🏠",
        "description": "Housing for all by providing interest subsidies on home loans.",
        "benefits": "Subsidy up to ₹2.67 Lakhs on home loan interest.",
        "max_income": 1800000,
        "eligible_states": ["All"],
        "eligible_occupations": ["All"],
        "eligible_categories": ["All"],
        "required_documents": ["Aadhaar", "Income Proof", "Affidavit of No Pucca House"],
        "deadline": "Dec 2026",
        "apply_url": "https://pmaymis.gov.in/",
        "category": "Housing",
        "popularity": 96,
        "guidance_steps": [
            "Check the eligible category (EWS, LIG, MIG).",
            "Apply online or through a registered bank/HFC.",
            "Submit the declaration bahwa you do not own a pucca house.",
            "Once approved, credit link subsidy will be added to your loan account."
        ]
    },
    {
        "id": "pm_ujjwala",
        "name": "PM Ujjwala Yojana",
        "icon": "🔥",
        "description": "Providing clean cooking fuel to BPL households.",
        "benefits": "Free LPG connection and first refill for eligible women.",
        "max_income": 200000,
        "eligible_states": ["All"],
        "eligible_occupations": ["All"],
        "eligible_categories": ["SC", "ST", "OBC", "General (BPL)"],
        "gender": "Female",
        "required_documents": ["Ration Card", "BPL Certificate", "Aadhaar Card"],
        "deadline": "Ongoing",
        "apply_url": "https://www.pmuy.gov.in/",
        "category": "Social Welfare",
        "popularity": 94
    },
    {
        "id": "mgnrega",
        "name": "MGNREGA Employment",
        "icon": "⛏️",
        "description": "Legal guarantee for at least 100 days of wage employment in a financial year.",
        "benefits": "Guaranteed minimum wage and unemployment allowance if work not provided.",
        "max_income": 5000000,
        "eligible_states": ["All"],
        "eligible_occupations": ["Artisan", "Unemployed", "Farmer", "Manual Labor"],
        "eligible_categories": ["All"],
        "required_documents": ["Job Card", "Aadhaar Card"],
        "deadline": "Rolling",
        "apply_url": "https://nrega.nic.in/",
        "category": "Employment",
        "popularity": 97
    },
    {
        "id": "pm_shram_yogi",
        "name": "PM Shram Yogi Maandhan (PM-SYM)",
        "icon": "👴",
        "description": "Voluntary and contributory pension scheme for unorganized workers.",
        "benefits": "Minimum assured pension of ₹3,000 per month after age 60.",
        "max_income": 180000,
        "eligible_states": ["All"],
        "eligible_occupations": ["Artisan", "Self-Employed", "Manual Labor", "Daily Wager"],
        "eligible_categories": ["All"],
        "min_age": 18,
        "max_age": 40,
        "required_documents": ["Savings Bank Account", "Aadhaar Card"],
        "deadline": "Ongoing",
        "apply_url": "https://maandhan.in/",
        "category": "Social Welfare",
        "popularity": 82
    },
    {
        "id": "nsap_pension",
        "name": "National Social Assistance Programme",
        "icon": "👵",
        "description": "Support to elderly, widows and disabled persons from BPL households.",
        "benefits": "Monthly pension ranging from ₹200 to ₹500 (plus state contributions).",
        "max_income": 100000,
        "eligible_states": ["All"],
        "eligible_occupations": ["All"],
        "eligible_categories": ["General (BPL)"],
        "min_age": 60,
        "required_documents": ["BPL Card", "Age Proof", "Disability Certificate (if applicable)"],
        "deadline": "Ongoing",
        "apply_url": "https://nsap.nic.in/",
        "category": "Social Welfare",
        "popularity": 80
    },
    {
        "id": "pm_matru_vandana",
        "name": "PM Matru Vandana Yojana",
        "icon": "🤰",
        "description": "Maternity benefit program for pregnant and lactating mothers.",
        "benefits": "Cash incentive of ₹5,000 in three installments.",
        "max_income": 800000,
        "eligible_states": ["All"],
        "eligible_occupations": ["All"],
        "eligible_categories": ["All"],
        "gender": "Female",
        "required_documents": ["Mother-Child Protection Card", "Bank Account Details"],
        "deadline": "Ongoing",
        "apply_url": "https://wcd.nic.in/schemes/pradhan-mantri-matru-vandana-yojana",
        "category": "Health",
        "popularity": 86
    },
    {
        "id": "stand_up_india",
        "name": "Stand Up India Scheme",
        "icon": "📈",
        "description": "Bank loans between ₹10 lakh and ₹1 Crore to SC/ST and Women entrepreneurs.",
        "benefits": "Accessible financing for setting up greenfield enterprises.",
        "max_income": 5000000,
        "eligible_states": ["All"],
        "eligible_occupations": ["Entrepreneur"],
        "eligible_categories": ["SC", "ST", "All (if Female)"],
        "required_documents": ["Business Plan", "Caste Certificate", "Bank Statements"],
        "deadline": "Open",
        "apply_url": "https://www.standupmitra.in/",
        "category": "Finance",
        "popularity": 78
    },
    {
        "id": "pm_vishwakarma",
        "name": "PM Vishwakarma Scheme",
        "icon": "⚒️",
        "description": "Support for traditional artisans and craftspeople.",
        "benefits": "Skill training, tool kit incentive, and credit support.",
        "max_income": 600000,
        "eligible_states": ["All"],
        "eligible_occupations": ["Artisan", "Carpenter", "Blacksmith", "Potter"],
        "eligible_categories": ["All"],
        "required_documents": ["Aadhaar", "Bank Passbook", "Caste Certificate"],
        "deadline": "Open",
        "apply_url": "https://pmvishwakarma.gov.in/",
        "category": "Skill Development",
        "popularity": 89
    },
    {
        "id": "sukanya_samriddhi",
        "name": "Sukanya Samriddhi Yojana",
        "icon": "💰",
        "description": "Savings scheme for the girl child education/marriage.",
        "benefits": "High interest rate and tax benefits.",
        "max_income": 5000000,
        "eligible_states": ["All"],
        "eligible_occupations": ["All"],
        "eligible_categories": ["All"],
        "gender": "Female",
        "max_age": 10,
        "required_documents": ["Birth Certificate", "Aadhaar Card of Parent"],
        "deadline": "Ongoing",
        "apply_url": "https://www.indiapost.gov.in/",
        "category": "Finance",
        "popularity": 91
    },
    {
        "id": "pm_poshan",
        "name": "PM POSHAN (Mid Day Meal)",
        "icon": "🍲",
        "description": "Ensuring nutrition for primary students.",
        "benefits": "Free warm nutritious meals in government schools.",
        "max_income": 9999999,
        "eligible_states": ["All"],
        "eligible_occupations": ["Student"],
        "eligible_categories": ["All"],
        "min_age": 5,
        "max_age": 14,
        "required_documents": ["School ID", "Ration Card"],
        "deadline": "Rolling",
        "apply_url": "https://pmposhan.education.gov.in/",
        "category": "Social Welfare",
        "popularity": 93
    },
    {
        "id": "startup_india_learning",
        "name": "Startup India Learning Program",
        "icon": "💡",
        "description": "Free online entrepreneurship program.",
        "benefits": "Certification and mentorship.",
        "max_income": 99999999,
        "eligible_states": ["All"],
        "eligible_occupations": ["Entrepreneur", "Student", "Unemployed"],
        "eligible_categories": ["All"],
        "required_documents": ["Email ID"],
        "deadline": "Always Open",
        "apply_url": "https://www.startupindia.gov.in/content/sih/en/learning-and-development_v2.html",
        "category": "Education",
        "popularity": 75
    },
    {
        "id": "atal_pension",
        "name": "Atal Pension Yojana (APY)",
        "icon": "👴",
        "description": "Pension scheme for citizens in the unorganized sector.",
        "benefits": "Fixed pension after age 60.",
        "max_income": 800000,
        "eligible_states": ["All"],
        "eligible_occupations": ["All"],
        "eligible_categories": ["All"],
        "min_age": 18,
        "max_age": 40,
        "required_documents": ["Savings Bank Account", "Aadhaar Card"],
        "deadline": "Ongoing",
        "apply_url": "https://npscra.nsdl.co.in/scheme-details.php",
        "category": "Social Welfare",
        "popularity": 81
    }
]

def seed_db():
    db = SessionLocal()
    try:
        # Create tables first
        Base.metadata.create_all(bind=engine)

        # Clear and Re-seed to ensure schema updates are applied
        db.query(Scheme).delete()
        print("Cleared existing schemes for fresh seed...")

        for s_data in SCHEMES_LIST:
            scheme = Scheme(**s_data)
            db.add(scheme)
        
        db.commit()
        print(f"Successfully seeded {len(SCHEMES_LIST)} schemes into the database.")
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_db()

if __name__ == "__main__":
    seed_db()
