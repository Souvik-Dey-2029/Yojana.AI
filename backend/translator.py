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
        "Description": "विवरण",
        # Scheme Names
        "PM Kisan Samman Nidhi": "पीएम किसान सम्मान निधि",
        "Swami Vivekananda Merit-cum-Means Scholarship": "स्वामी विवेकानंद मेरिट-सह-साधन छात्रवृत्ति",
        "Pradhan Mantri Mudra Yojana (PMMY)": "प्रधानमंत्री मुद्रा योजना (पीएमएमवाई)",
        "Kanyashree Prakalpa": "कन्याश्री प्रकल्प",
        "Ayushman Bharat (PM-JAY)": "आयुष्मान भारत (पीएम-जय)",
        "PM Awas Yojana (PMAY)": "पीएम आवास योजना (पीएमएवाई)",
        "PM Ujjwala Yojana": "पीएम उज्ज्वला योजना",
        "MGNREGA Employment": "मनरेगा रोजगार",
        "PM Shram Yogi Maandhan (PM-SYM)": "पीएम श्रम योगी मानधन",
        "National Social Assistance Programme": "राष्ट्रीय सामाजिक सहायता कार्यक्रम",
        "PM Matru Vandana Yojana": "पीएम मातृ वंदना योजना",
        "Stand Up India Scheme": "स्टैंड अप इंडिया योजना",
        "PM Vishwakarma Scheme": "पीएम विश्वकर्मा योजना",
        "Sukanya Samriddhi Yojana": "सुकन्या समृद्धि योजना",
        "PM POSHAN (Mid Day Meal)": "पीएम पोषण (मिड डे मील)",
        "Startup India Learning Program": "स्टार्टअप इंडिया लर्निंग प्रोग्राम",
        "Atal Pension Yojana (APY)": "अटल पेंशन योजना (एपीवाई)",
        "PM SVANidhi (Street Vendor Loan)": "पीएम स्वनिधि (स्ट्रीट वेंडर लोन)",
        "Lakhpati Didi Scheme": "लखपति दीदी योजना",
        "PM Surya Ghar: Muft Bijli Yojana": "पीएम सूर्य घर: मुफ्त बिजली योजना",
        "Pradhan Mantri Jan Dhan Yojana (PMJDY)": "प्रधानमंत्री जन धन योजना (पीएमजेडीवाई)",
        "PM Jeevan Jyoti Bima Yojana (PMJJBY)": "पीएम जीवन ज्योति बीमा योजना (पीएमजेजेबीवाई)",
        "PM Suraksha Bima Yojana (PMSBY)": "पीएम सुरक्षा बीमा योजना (पीएमएसबीवाई)",
        "PM SHRI Schools": "पीएम श्री स्कूल",
        "National Apprenticeship Promotion Scheme (NAPS)": "राष्ट्रीय अप्रेंटिसशिप प्रोत्साहन योजना (एनएपीएस)",
        "Antyodaya Anna Yojana (AAY)": "अंत्योदय अन्न योजना (एएवाई)",
        "PM PVTG Development Mission": "पीएम पीवीटीजी विकास मिशन",
        "Agnipath Scheme (Agniveer)": "अग्निपथ योजना (अग्निवीर)",
        "Mahila Samman Savings Certificate": "महिला सम्मान बचत प्रमाण पत्र",
        "PM eBus Sewa": "पीएम ई-बस सेवा",
        "PM Formalisation of Micro Food Processing Enterprises (PMFME)": "पीएम सूक्ष्म खाद्य प्रसंस्करण उद्यम औपचारिकता (पीएमएफएमई)"
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
        "Description": "বিবরণ",
        # Scheme Names
        "PM Kisan Samman Nidhi": "পিএম কিষাণ সম্মান নিধি",
        "Swami Vivekananda Merit-cum-Means Scholarship": "স্বামী বিবেকানন্দ মেরিট-কাম-মিনস স্কলারশিপ",
        "Pradhan Mantri Mudra Yojana (PMMY)": "প্রধানমন্ত্রী মুদ্রা যোজনা (পিএমএমওয়াই)",
        "Kanyashree Prakalpa": "কন্যাশ্রী প্রকল্প",
        "Ayushman Bharat (PM-JAY)": "আয়ুষ্মান ভারত (পিএম-জেএওয়াই)",
        "PM Awas Yojana (PMAY)": "পিএম আবাস যোজনা (পিএমএওয়াই)",
        "PM Ujjwala Yojana": "পিএম উজ্জ্বলা যোজনা",
        "MGNREGA Employment": "মনরেগা কর্মসংস্থান",
        "PM Shram Yogi Maandhan (PM-SYM)": "পিএম শ্রম যোগী মানধন",
        "National Social Assistance Programme": "জাতীয় সামাজিক সহায়তা কর্মসূচি",
        "PM Matru Vandana Yojana": "পিএম মাতৃ বন্দনা যোজনা",
        "Stand Up India Scheme": "স্ট্যান্ড আপ ইন্ডিয়া স্কিম",
        "PM Vishwakarma Scheme": "পিএম বিশ্বকর্মা যোজনা",
        "Sukanya Samriddhi Yojana": "সুকন্যা সমৃদ্ধি যোজনা",
        "PM POSHAN (Mid Day Meal)": "পিএম পোষাণ (মিড ডে মিল)",
        "Startup India Learning Program": "স্টার্টআপ ইন্ডিয়া লার্নিং প্রোগ্রাম",
        "Atal Pension Yojana (APY)": "অটল পেনশন যোজনা (এপিওয়াই)",
        "PM SVANidhi (Street Vendor Loan)": "পিএম স্বনিধি (স্ট্রিট ভেন্ডর লোন)",
        "Lakhpati Didi Scheme": "লখপতি দিদি যোজনা",
        "PM Surya Ghar: Muft Bijli Yojana": "পিএম সূর্য ঘর: মুফ্ত বিজলি যোজনা",
        "Pradhan Mantri Jan Dhan Yojana (PMJDY)": "প্রধানমন্ত্রী জন ধন যোজনা (পিএমজেডিওয়াই)",
        "PM Jeevan Jyoti Bima Yojana (PMJJBY)": "পিএম জীবন জ্যোতি বিমা যোজনা (পিএমজেজেবিওয়াই)",
        "PM Suraksha Bima Yojana (PMSBY)": "পিএম সুরক্ষা বিমা যোজনা (পিএমএসবিওয়াই)",
        "PM SHRI Schools": "পিএম শ্রী স্কুল",
        "National Apprenticeship Promotion Scheme (NAPS)": "জাতীয় শিক্ষানবিশ প্রচার প্রকল্প (এনএপিএস)",
        "Antyodaya Anna Yojana (AAY)": "অন্ত্যোদয় অন্ন যোজনা (এএওয়াই)",
        "PM PVTG Development Mission": "পিএম পিভিটিজি উন্নয়ন মিশন",
        "Agnipath Scheme (Agniveer)": "অগ্নিপথ প্রকল্প (অগ্নিবীর)",
        "Mahila Samman Savings Certificate": "মহিলা সম্মান সঞ্চয় শংসাপত্র",
        "PM eBus Sewa": "পিএম ই-বাস সেবা",
        "PM Formalisation of Micro Food Processing Enterprises (PMFME)": "পিএম মাইক্রো ফুড প্রসেসিং এন্টারপ্রাইজ ফর্মালইজেশন (পিএমএফএমই)"
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
