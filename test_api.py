import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_prediction():
    print("🧪 Testing Rejection Prediction API...")
    payload = {
        "aadhaar_name_match": 0,
        "income_certificate_valid": 0,
        "bank_account_seeded": 1,
        "address_match": 1,
        "category_certificate_valid": 1,
        "photo_correct": 1,
        "mobile_linked": 1,
        "self_attested_docs": 1
    }
    
    try:
        response = requests.post(f"{BASE_URL}/predict-application-success", json=payload)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Prediction Success: {result}")
            return result
        else:
            print(f"❌ Prediction Failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Connection Error: {e}")
    return None

def test_pdf_generation(score, risk, suggestions):
    print(f"🧪 Testing PDF Generation with Success Analysis ({score}%, {risk})...")
    # Using a known scheme ID (pm_kisan)
    url = f"{BASE_URL}/download-guide/pm_kisan?name=Souvik&score={score}&risk_level={risk}&suggestions={requests.utils.quote(suggestions)}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"✅ PDF Generation Success (Bytes: {len(response.content)})")
            with open("test_guide_with_analysis.pdf", "wb") as f:
                f.write(response.content)
            print("📁 PDF saved to test_guide_with_analysis.pdf")
        else:
            print(f"❌ PDF Generation Failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Connection Error: {e}")

if __name__ == "__main__":
    # Wait for server to be ready (assuming it's running)
    res = test_prediction()
    if res:
        test_pdf_generation(res['score'], res['risk_level'], ",".join(res['suggestions']))
