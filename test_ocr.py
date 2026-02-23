import pytesseract
from PIL import Image
import os

print("--- OCR Diagnostic ---")
try:
    print(f"Pytesseract version: {pytesseract.get_tesseract_version()}")
except Exception as e:
    print(f"Error getting version: {e}")

try:
    # Try to find tesseract
    print(f"Tesseract cmd in pytesseract: {pytesseract.pytesseract.tesseract_cmd}")
except Exception as e:
    print(f"Error getting cmd: {e}")

print("----------------------")
