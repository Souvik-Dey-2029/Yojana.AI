import json
import os
from deep_translator import GoogleTranslator

SUPPORTED_LANGUAGES = {
    "en": "english",
    "hi": "hindi",
    "bn": "bengali",
    "ta": "tamil",
    "mr": "marathi"
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
    
    # Start with a full copy to preserve id, icon, deadline, apply_url, etc.
    translated_scheme = scheme.copy()
    
    # Translate specific string fields
    translated_scheme["name"] = translate_text(scheme.get("name", ""), target_lang)
    translated_scheme["description"] = translate_text(scheme.get("description", ""), target_lang)
    translated_scheme["benefits"] = translate_text(scheme.get("benefits", ""), target_lang)
    
    if "required_documents" in scheme and isinstance(scheme["required_documents"], list):
        translated_scheme["required_documents"] = [translate_text(doc, target_lang) for doc in scheme["required_documents"]]
    
    return translated_scheme
