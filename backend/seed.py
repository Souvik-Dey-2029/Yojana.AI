from backend.database import SessionLocal, engine, Base
from backend.db_models import Scheme
import json

Base.metadata.create_all(bind=engine)

SCHEMES_LIST = [
    # --- PHASE 1/2 SCHEMES ---
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
        "category": "Social Welfare"
    },
    # --- NEW PHASE 3 SCHEMES (EXPANSION) ---
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
        "category": "Health"
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
        "category": "Health"
    },
    {
        "id": "stand_up_india",
        "name": "Stand Up India Scheme",
        "icon": "📈",
        "description": "Bank loans between ₹10 lakh and ₹1 Crore to at least one SC or ST borrower and at least one woman borrower per bank branch.",
        "benefits": "Accessible financing for setting up greenfield enterprises.",
        "max_income": 5000000,
        "eligible_states": ["All"],
        "eligible_occupations": ["Entrepreneur"],
        "eligible_categories": ["SC", "ST"],
        "required_documents": ["Business Plan", "Caste Certificate", "Bank Statements"],
        "deadline": "Open",
        "apply_url": "https://www.standupmitra.in/",
        "category": "Finance"
    },
    {
        "id": "pm_vishwakarma",
        "name": "PM Vishwakarma Scheme",
        "icon": "⚒️",
        "description": "Support for traditional artisans and craftspeople in various sectors.",
        "benefits": "Skill training, tool kit incentive, and collateral-free credit support.",
        "max_income": 600000,
        "eligible_states": ["All"],
        "eligible_occupations": ["Artisan", "Carpenter", "Blacksmith", "Potter"],
        "eligible_categories": ["All"],
        "required_documents": ["Aadhaar", "Bank Passbook", "Caste Certificate"],
        "deadline": "Open",
        "apply_url": "https://pmvishwakarma.gov.in/",
        "category": "Skill Development"
    },
    {
        "id": "sukanya_samriddhi",
        "name": "Sukanya Samriddhi Yojana",
        "icon": "💰",
        "description": "Savings scheme for the girl child under the 'Beti Bachao Beti Padhao' campaign.",
        "benefits": "High interest rate and tax benefits on savings for girl's education/marriage.",
        "max_income": 5000000,
        "eligible_states": ["All"],
        "eligible_occupations": ["All"],
        "eligible_categories": ["All"],
        "gender": "Female",
        "max_age": 10,
        "required_documents": ["Birth Certificate", "Aadhaar Card of Parent"],
        "deadline": "Ongoing",
        "apply_url": "https://www.indiapost.gov.in/",
        "category": "Finance"
    },
    {
        "id": "pm_poshan",
        "name": "PM POSHAN (Mid Day Meal)",
        "icon": "🍲",
        "description": "Ensuring nutrition and increasing school attendance for primary students.",
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
        "category": "Social Welfare"
    },
    {
        "id": "startup_india_learning",
        "name": "Startup India Learning Program",
        "icon": "💡",
        "description": "Free online entrepreneurship program by Startup India.",
        "benefits": "Entrepreneurship certification and industry mentorship.",
        "max_income": 99999999,
        "eligible_states": ["All"],
        "eligible_occupations": ["Entrepreneur", "Student", "Unemployed"],
        "eligible_categories": ["All"],
        "required_documents": ["Email ID"],
        "deadline": "Always Open",
        "apply_url": "https://www.startupindia.gov.in/content/sih/en/learning-and-development_v2.html",
        "category": "Education"
    },
    {
        "id": "atal_pension",
        "name": "Atal Pension Yojana (APY)",
        "icon": "👴",
        "description": "Pension scheme for citizens in the unorganized sector.",
        "benefits": "Fixed pension of ₹1,000 to ₹5,000 after age 60.",
        "max_income": 800000,
        "eligible_states": ["All"],
        "eligible_occupations": ["All"],
        "eligible_categories": ["All"],
        "min_age": 18,
        "max_age": 40,
        "required_documents": ["Savings Bank Account", "Aadhaar Card"],
        "deadline": "Ongoing",
        "apply_url": "https://npscra.nsdl.co.in/scheme-details.php",
        "category": "Social Welfare"
    }
]

def seed_db():
    db = SessionLocal()
    try:
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
