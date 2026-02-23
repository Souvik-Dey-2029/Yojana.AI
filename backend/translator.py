import json
import os

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
        translated = GoogleTranslator(source='auto', target=target_lang).translate(text)
        TRANSLATION_CACHE[cache_key] = translated
        save_cache()
        return translated
    except Exception as e:
        print(f"Translation error: {e}")
        return text

def translate_scheme(scheme: dict, target_lang: str) -> dict:
    if target_lang == "en":
        return scheme
    
    translated_scheme = scheme.copy()
    translated_scheme["name"] = translate_text(scheme["name"], target_lang)
    translated_scheme["description"] = translate_text(scheme["description"], target_lang)
    translated_scheme["benefits"] = translate_text(scheme["benefits"], target_lang)
    translated_scheme["required_documents"] = [translate_text(doc, target_lang) for doc in scheme["required_documents"]]
    
    return translated_scheme
