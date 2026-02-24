import json
import os
from concurrent.futures import ThreadPoolExecutor
from deep_translator import GoogleTranslator

SUPPORTED_LANGUAGES = {
    "en": "english",
    "hi": "hindi",
    "bn": "bengali",
    "ta": "tamil",
    "mr": "marathi"
}

# Industry-specific translations for consistency
COMMON_TERMS = {
    "hi": {
        "Aadhaar Card": "आधार कार्ड",
        "Aadhaar": "आधार",
        "Income Certificate": "आय प्रमाण पत्र",
        "Ration Card": "राशन कार्ड",
        "Bank Passbook": "बैंक पासबुक",
        "Required Documents": "आवश्यक दस्तावेज",
        "Apply Now": "अभी आवेदन करें",
        "AI Guide": "एआई गाइड",
        "Deadline": "समय सीमा",
        "Benefits": "लाभ",
        "Description": "विवरण"
    },
    "bn": {
        "Aadhaar Card": "আধার কার্ড",
        "Aadhaar": "আধার",
        "Income Certificate": "আয় শংসাপত্র",
        "Ration Card": "রেশন কার্ড",
        "Bank Passbook": "ব্যাঙ্ক পাসবুক",
        "Required Documents": "প্রয়োজনীয় নথি",
        "Apply Now": "এখনই আবেদন করুন",
        "AI Guide": "এআই গাইড",
        "Deadline": "শেষ তারিখ",
        "Benefits": "উপকারিতা",
        "Description": "বিবরণ"
    }
}

# Simple persistent cache
CACHE_FILE = "translation_cache.json"

def load_cache():
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

TRANSLATION_CACHE = load_cache()

def save_cache():
    try:
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(TRANSLATION_CACHE, f, ensure_ascii=False, indent=2)
    except:
        pass

def translate_text(text: str, target_lang: str) -> str:
    if target_lang == "en" or target_lang not in SUPPORTED_LANGUAGES:
        return text
    
    # 1. Check common terms dictionary
    if target_lang in COMMON_TERMS and text in COMMON_TERMS[target_lang]:
        return COMMON_TERMS[target_lang][text]

    # 2. Check simple persistent cache
    cache_key = f"{target_lang}:{text}"
    if cache_key in TRANSLATION_CACHE:
        return TRANSLATION_CACHE[cache_key]
        
    try:
        # Simple timeout or error handling for external service
        translated = GoogleTranslator(source='auto', target=target_lang).translate(text)
        if not translated:
            return text
        TRANSLATION_CACHE[cache_key] = translated
        save_cache()
        return translated
    except Exception as e:
        print(f"Translation error for {target_lang}: {e}")
        return text

def translate_scheme(scheme: dict, target_lang: str) -> dict:
    if target_lang == "en":
        return scheme
    
    translated_scheme = scheme.copy()
    
    # Fields to translate
    fields_to_translate = ["name", "description", "benefits"]
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        # 1. Translate string fields
        future_to_field = {executor.submit(translate_text, scheme.get(field, ""), target_lang): field for field in fields_to_translate}
        
        # 2. Translate documents list if it exists
        docs_future = None
        if "required_documents" in scheme and isinstance(scheme["required_documents"], list):
            docs = scheme["required_documents"]
            docs_future = [executor.submit(translate_text, doc, target_lang) for doc in docs]

        # Collect string fields
        for future in future_to_field:
            field = future_to_field[future]
            translated_scheme[field] = future.result()

        # Collect documents
        if docs_future:
            translated_scheme["required_documents"] = [f.result() for f in docs_future]
    
    return translated_scheme
