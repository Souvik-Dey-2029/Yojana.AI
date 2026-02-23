from fastapi import APIRouter, UploadFile, File, HTTPException
from PIL import Image
import pytesseract
import io
import re
import os

router = APIRouter()

# --- Professional OCR Configuration ---
# Automatically attempt to locate Tesseract on Windows if not in PATH
POSSIBLE_TESS_PATHS = [
    r'C:\Program Files\Tesseract-OCR\tesseract.exe',
    r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
    os.path.expanduser(r'~\AppData\Local\Programs\Tesseract-OCR\tesseract.exe')
]

for path in POSSIBLE_TESS_PATHS:
    if os.path.exists(path):
        pytesseract.pytesseract.tesseract_cmd = path
        break

@router.post("/ocr-extract")
async def ocr_extract(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image files are supported.")

    # Check if tesseract is configured/present
    tess_installed = False
    try:
        if pytesseract.pytesseract.tesseract_cmd and os.path.exists(pytesseract.pytesseract.tesseract_cmd):
            tess_installed = True
        else:
            import shutil
            if shutil.which("tesseract"):
                tess_installed = True
    except:
        pass

    if not tess_installed:
        return {
            "extracted": {"name": "Souvik Dey", "age": 28, "gender": "Male"},
            "status": "fallback",
            "warning": "Tesseract OCR engine not found. Providing demo data."
        }

    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        # Perform OCR
        text = pytesseract.image_to_string(image)
        
        extracted_data = {
            "name": None,
            "age": None,
            "gender": None
        }

        # 1. Age/DOB Detection
        dob_match = re.search(r"(\d{2}/\d{2}/\d{4})|(\d{4})", text)
        if dob_match:
            year_str = dob_match.group(0)[-4:]
            try:
                year = int(year_str)
                extracted_data["age"] = 2024 - year
            except: pass

        # 2. Gender Detection
        if re.search(r"\b(Male|MALE|M)\b", text):
            extracted_data["gender"] = "Male"
        elif re.search(r"\b(Female|FEMALE|F)\b", text):
            extracted_data["gender"] = "Female"

        # 3. Name (Heuristic)
        lines = [l.strip() for l in text.split("\n") if l.strip()]
        for line in lines:
            if re.match(r"^[A-Za-z ]{5,30}$", line) and not any(kw in line.upper() for kw in ["INDIA", "GOVERNMENT", "AADHAAR", "DOB"]):
                extracted_data["name"] = line
                break

        return {
            "extracted": extracted_data,
            "status": "success",
            "message": "Data extracted successfully via AI OCR engine."
        }

    except Exception as e:
        print(f"OCR Processing Error: {e}")
        return {
            "extracted": {"name": "Souvik Dey", "age": 28, "gender": "Male"},
            "status": "fallback",
            "warning": f"Processing error: {str(e)}. Providing demo data."
        }
