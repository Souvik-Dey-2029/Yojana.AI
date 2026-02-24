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
        "PM Formalisation of Micro Food Processing Enterprises (PMFME)": "पीएम सूक्ष्म खाद्य प्रसंस्करण उद्यम औপचारिकता (पीएमएफएमई)",
        "PM-DAKSH (Skill Development)": "पीएम-दक्ष (कौशल विकास)",
        "National Overseas Scholarship": "राष्ट्रीय प्रवासी छात्रवृत्ति",
        "PM Fasal Bima Yojana (PMFBY)": "पीएम फसल बीमा योजना",
        "PM-KUSUM (Solar Pump Scheme)": "पीएम-कुसुम (सौर पंप योजना)",
        "e-Shram Card": "ई-श्रम कार्ड",
        "One Nation One Ration Card": "एक राष्ट्र एक राशन कार्ड",
        "Beti Bachao Beti Padhao": "बेटी बचाओ बेटी पढ़ाओ",
        "Janani Suraksha Yojana (JSY)": "जननी सुरक्षा योजना",
        "Mission Indradhanush (Immunization)": "मिशन इंद्रधनुष (टीकाकरण)",
        "PM-DevINE (North East Development)": "पीएम-डिवाइन (उत्तर पूर्व विकास)",
        "Saansad Adarsh Gram Yojana (SAGY)": "सासंद आदर्श ग्राम योजना",
        "Swachh Bharat Abhiyan Assistance": "स्वच्छ भारत अभियान सहायता",
        "PM-WANI (Public Wi-Fi)": "पीएम-वाणी (सार्वजनिक वाई-फाई)",
        "National Apprenticeship Training Scheme (NATS)": "राष्ट्रीय शिक्षुता प्रशिक्षण योजना (एनएटीएस)",
        "NMMS Scholarship": "एनएमएमएस छात्रवृत्ति",
        "Pre-Matric Minority Scholarship": "प्री-मैट्रिक अल्पसंख्यक छात्रवृत्ति",
        "Post-Matric Minority Scholarship": "पोस्ट-मैट्रिक अल्पसंख्यक छात्रवृत्ति",
        "Merit-cum-Means Minority Scholarship": "मेरिट-सह-साधन अल्पसंख्यक छात्रवृत्ति",
        "USTTAD (Minority Artisans)": "उस्ताद (अल्पसंख्यक शिल्पकार)",
        "SVAMITVA Scheme": "स्वामित्व योजना",
        "PM-Kisan Maandhan Yojana": "पीएम-किसान मानधन योजना",
        # Footer Terms
        "Platform": "प्लेटफ़ॉर्म",
        "Other Links": "अन्य लिंक",
        "Legal": "कानूनी",
        "Developer Contact": "डेवलपर संपर्क",
        "Disclaimer": "डिस्क्लेमर",
        "FAQs": "अक्सर पूछे जाने वाले प्रश्न",
        "AI Methodology": "एआई कार्यप्रणाली",
        "User Guide": "उपयोगकर्ता मार्गदर्शिका",
        "Terms & Conditions": "नियम और शर्तें",
        "Privacy Policy": "गोपनीयता नीति",
        "Data Protection": "डेटा सुरक्षा",
        "Accessibility": "सुलभता"
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
        "PM Formalisation of Micro Food Processing Enterprises (PMFME)": "পিএম মাইক্রো ফুড প্রসেসিং এন্টারপ্রাইজ ফর্মালইজেশন (পিএমএফএমই)",
        "PM-DAKSH (Skill Development)": "পিএম-দক্ষ (দক্ষতা উন্নয়ন)",
        "National Overseas Scholarship": "জাতীয় বিদেশী বৃত্তি",
        "PM Fasal Bima Yojana (PMFBY)": "পিএম ফসল বিমা যোজনা",
        "PM-KUSUM (Solar Pump Scheme)": "পিএম-কুসুম (সৌর পাম্প প্রকল্প)",
        "e-Shram Card": "ই-শ্রম কার্ড",
        "One Nation One Ration Card": "এক জাতি এক রেশন কার্ড",
        "Beti Bachao Beti Padhao": "বেটি বাঁচাও বেটি পড়াও",
        "Janani Suraksha Yojana (JSY)": "জননী সুরক্ষা যোজনা",
        "Mission Indradhanush (Immunization)": "মিশন ইন্দ্রধনুশ (টিকাকরণ)",
        "PM-DevINE (North East Development)": "পিএম-ডিভাইন (উত্তর পূর্ব উন্নয়ন)",
        "Saansad Adarsh Gram Yojana (SAGY)": "সাংসদ আদর্শ গ্রাম যোজনা",
        "Swachh Bharat Abhiyan Assistance": "স্বচ্ছ ভারত অভিযান সহায়তা",
        "PM-WANI (Public Wi-Fi)": "পিএম-বাণী (পাবলিক ওয়াই-ফাই)",
        "National Apprenticeship Training Scheme (NATS)": "জাতীয় শিক্ষানবিশ প্রশিক্ষণ প্রকল্প ( এনএটিএস)",
        "NMMS Scholarship": "এনএমএমএস বৃত্তি",
        "Pre-Matric Minority Scholarship": "প্রি-ম্যাট্রিক সংখ্যালঘু বৃত্তি",
        "Post-Matric Minority Scholarship": "পোস্ট-ম্যাট্রিক সংখ্যালঘু বৃত্তি",
        "Merit-cum-Means Minority Scholarship": "মেরিট-কাম-মিনস সংখ্যালঘু বৃত্তি",
        "USTTAD (Minority Artisans)": "ওস্তাদ (সংখ্যালঘু কারিগর)",
        "SVAMITVA Scheme": "স্বামিত্ব প্রকল্প",
        "PM-Kisan Maandhan Yojana": "পিএম-কিষাণ মানধন যোজনা",
        # Footer Terms
        "Platform": "প্ল্যাটফর্ম",
        "Other Links": "অন্যান্য লিঙ্ক",
        "Legal": "আইনি",
        "Developer Contact": "ডেভেলপার যোগাযোগ",
        "Disclaimer": "দাবিত্যাগ",
        "FAQs": "সাধারণ জিজ্ঞাসা",
        "AI Methodology": "এআই পদ্ধতি",
        "User Guide": "ব্যবহারকারী নির্দেশিকা",
        "Terms & Conditions": "শর্তাবলী",
        "Privacy Policy": "গোপনীয়তা নীতি",
        "Data Protection": "ডেটা সুরক্ষা",
        "Accessibility": "সহজলভ্যতা"
    },
    "ta": {
        "Aadhaar Card": "ஆதார் அட்டை",
        "Aadhaar": "ஆதார்",
        "Income Certificate": "வருமானச் சான்றிதழ்",
        "Ration Card": "ரேஷன் அட்டை",
        "Bank Passbook": "வங்கி கணக்குப் புத்தகம்",
        "Required Documents": "தேவையான ஆவணங்கள்",
        "Apply Now": "இப்பொழுதே விண்ணப்பிக்கவும்",
        "AI Guide": "AI வழிகாட்டி",
        "Deadline": "காலக்கெடு",
        "Benefits": "நன்மைகள்",
        "Description": "விளக்கம்",
        # Scheme Names
        "PM Kisan Samman Nidhi": "பிஎம் கிசான் சம்மான் நிதி",
        "Swami Vivekananda Merit-cum-Means Scholarship": "சுவாமி விவேகானந்தர் மெரிட்-கம்-மீன்ஸ் ஸ்காலர்ஷிப்",
        "Pradhan Mantri Mudra Yojana (PMMY)": "பிரதான் மந்திரி முத்ரா யோஜனா (PMMY)",
        "Kanyashree Prakalpa": "கன்யாஸ்ரீ பிரகல்பா",
        "Ayushman Bharat (PM-JAY)": "ஆயுஷ்மான் பாரத் (PM-JAY)",
        "PM Awas Yojana (PMAY)": "பிஎம் ஆவாஸ் யோஜனா (PMAY)",
        "PM Ujjwala Yojana": "பிஎம் உஜ்வாலா யோஜனா",
        "MGNREGA Employment": "மகாத்மா காந்தி தேசிய ஊரக வேலை வாய்ப்புத் திட்டம்",
        "PM Shram Yogi Maandhan (PM-SYM)": "பிஎம் ஸ்ரம் யோகி மான்தன்",
        "National Social Assistance Programme": "தேசிய சமூக உதவித் திட்டம்",
        "PM Matru Vandana Yojana": "பிஎம் மாத்ரு வந்தனா யோஜனா",
        "Stand Up India Scheme": "ஸ்டாண்ட் அப் இந்தியா திட்டம்",
        "PM Vishwakarma Scheme": "பிஎம் விஸ்வகர்மா திட்டம்",
        "Sukanya Samriddhi Yojana": "சுகன்யா சம்ரிதி யோஜனா",
        "PM POSHAN (Mid Day Meal)": "பிஎம் போஷன் (மதிய உணவுத் திட்டம்)",
        "Startup India Learning Program": "ஸ்டார்ட்அப் இந்தியா கற்றல் திட்டம்",
        "Atal Pension Yojana (APY)": "அடல் பென்ஷன் யோஜனா (APY)",
        "PM SVANidhi (Street Vendor Loan)": "பிஎம் ஸ்வாநிதி (தெரு வியாபாரிகள் கடன்)",
        "Lakhpati Didi Scheme": "லக்பதி திதி திட்டம்",
        "PM Surya Ghar: Muft Bijli Yojana": "பிஎம் சூர்ய கர்: இலவச மின்சாரத் திட்டம்",
        "Pradhan Mantri Jan Dhan Yojana (PMJDY)": "பிரதான் மந்திரி ஜன தன் யோஜனா (PMJDY)",
        "PM Jeevan Jyoti Bima Yojana (PMJJBY)": "பிஎம் ஜீவன் ஜோதி பீமா யோஜனா",
        "PM Suraksha Bima Yojana (PMSBY)": "பிஎம் சுரக்ஷா பீமா யோஜனா",
        "PM SHRI Schools": "பிஎம் ஸ்ரீ பள்ளிகள்",
        "National Apprenticeship Promotion Scheme (NAPS)": "தேசிய அப்ரண்டிஷிப் ஊக்குவிப்புத் திட்டம்",
        "Antyodaya Anna Yojana (AAY)": "அந்தியோதயா அன்ன யோஜனா",
        "PM PVTG Development Mission": "பிஎம் பிவிடிஜி வளர்ச்சித் திட்டம்",
        "Agnipath Scheme (Agniveer)": "அக்னிபத் திட்டம் (அக்னிவீர்)",
        "Mahila Samman Savings Certificate": "மகிளா சம்மான் சேமிப்புச் சான்றிதழ்",
        "PM eBus Sewa": "பிஎம் இ-பஸ் சேவை",
        "PM Formalisation of Micro Food Processing Enterprises (PMFME)": "பிஎம் குறு உணவு பதப்படுத்தும் நிறுவனங்கள் முறைப்படுத்தும் திட்டம்",
        "PM-DAKSH (Skill Development)": "பிஎம்-தக்ஷ் (திறன் மேம்பாடு)",
        "National Overseas Scholarship": "தேசிய வெளிநாட்டு உதவித்தொகை",
        "PM Fasal Bima Yojana (PMFBY)": "பிஎம் பயிர் காப்பீட்டுத் திட்டம்",
        "PM-KUSUM (Solar Pump Scheme)": "பிஎம்-குசும் (சூரிய சக்தி பம்ப் திட்டம்)",
        "e-Shram Card": "இ-ஷ்ரம் அட்டை",
        "One Nation One Ration Card": "ஒரே நாடு ஒரே ரேஷன் கார்டு",
        "Beti Bachao Beti Padhao": "பெட்டி பச்சாவோ பெட்டி படாவோ",
        "Janani Suraksha Yojana (JSY)": "ஜனனி சுரக்ஷா யோஜனா",
        "Mission Indradhanush (Immunization)": "மிஷன் இந்திரதனுஷ் (தடுப்பூசி)",
        "PM-DevINE (North East Development)": "பிஎம்-டிவைன் (வடகிழக்கு வளர்ச்சி)",
        "Saansad Adarsh Gram Yojana (SAGY)": "சன்சாத் ஆதர்ஷ் கிராம யோஜனா",
        "Swachh Bharat Abhiyan Assistance": "தூய்மை இந்தியா திட்ட உதவி",
        "PM-WANI (Public Wi-Fi)": "பிஎம்-வாணி (பொது வைஃபை)",
        "National Apprenticeship Training Scheme (NATS)": "தேசிய அப்ரண்டிஷிப் பயிற்சித் திட்டம்",
        "NMMS Scholarship": "NMMS உதவித்தொகை",
        "Pre-Matric Minority Scholarship": "மெட்ரிக் முன் சிறுபான்மையினர் உதவித்தொகை",
        "Post-Matric Minority Scholarship": "மெட்ரிக் பின் சிறுபான்மையினர் உதவித்தொகை",
        "Merit-cum-Means Minority Scholarship": "தகுதி மற்றும் வருமான அடிப்படையிலான சிறுபான்மையினர் உதவித்தொகை",
        "USTTAD (Minority Artisans)": "உஸ்தாத் (சிறுபான்மையினக் கைவினைஞர்கள்)",
        "SVAMITVA Scheme": "சுவாமித்வா திட்டம்",
        "PM-Kisan Maandhan Yojana": "பிஎம்-கிசான் மான்தன் யோஜனா",
        # Footer Terms
        "Platform": "தளம்",
        "Other Links": "பிற இணைப்புகள்",
        "Legal": "சட்டபூர்வமான",
        "Developer Contact": "டெவலப்பர் தொடர்பு",
        "Disclaimer": "மறுப்பு",
        "FAQs": "அடிக்கடி கேட்கப்படும் கேள்விகள்",
        "AI Methodology": "AI முறை",
        "User Guide": "பயனர் வழிகாட்டி",
        "Terms & Conditions": "விதிமுறைகள் மற்றும் நிபந்தனைகள்",
        "Privacy Policy": "தனியுரிமைக் கொள்கை",
        "Data Protection": "தரவு பாதுகாப்பு",
        "Accessibility": "அணுகல்தன்மை"
    },
    "mr": {
        "Aadhaar Card": "आधार कार्ड",
        "Aadhaar": "आधार",
        "Income Certificate": "उत्पन्न प्रमाणपत्र",
        "Ration Card": "रेशन कार्ड",
        "Bank Passbook": "बँक पासबुक",
        "Required Documents": "आवश्यक कागदपत्रे",
        "Apply Now": "आता अर्ज करा",
        "AI Guide": "AI मार्गदर्शक",
        "Deadline": "डेडलाईन",
        "Benefits": "फायदे",
        "Description": "वर्णन",
        # Scheme Names
        "PM Kisan Samman Nidhi": "पीएम किसान सन्मान निधी",
        "Swami Vivekananda Merit-cum-Means Scholarship": "स्वामी विवेकानंद गुणवत्ता-निहाय शिष्यवृत्ती",
        "Pradhan Mantri Mudra Yojana (PMMY)": "प्रधानमंत्री मुद्रा योजना (PMMY)",
        "Kanyashree Prakalpa": "कन्याश्री प्रकल्प",
        "Ayushman Bharat (PM-JAY)": "आयुष्मान भारत (PM-JAY)",
        "PM Awas Yojana (PMAY)": "पीएम आवास योजना (PMAY)",
        "PM Ujjwala Yojana": "पीएम उज्ज्वला योजना",
        "MGNREGA Employment": "मनरेगा रोजगार",
        "PM Shram Yogi Maandhan (PM-SYM)": "पीएम श्रम योगी मानधन",
        "National Social Assistance Programme": "राष्ट्रीय सामाजिक सहायता कार्यक्रम",
        "PM Matru Vandana Yojana": "पीएम मातृ वंदना योजना",
        "Stand Up India Scheme": "स्टँड अप इंडिया योजना",
        "PM Vishwakarma Scheme": "पीएम विश्वकर्मा योजना",
        "Sukanya Samriddhi Yojana": "सुकन्या समृद्धी योजना",
        "PM POSHAN (Mid Day Meal)": "पीएम पोषण (मिड डे मील)",
        "Startup India Learning Program": "स्टार्टअप इंडिया लर्निंग प्रोग्राम",
        "Atal Pension Yojana (APY)": "अटल पेन्शन योजना (APY)",
        "PM SVANidhi (Street Vendor Loan)": "पीएम स्वनिधी (पथविक्रेता कर्ज)",
        "Lakhpati Didi Scheme": "लखपती दीदी योजना",
        "PM Surya Ghar: Muft Bijli Yojana": "पीएम सूर्य घर: मोफत वीज योजना",
        "Pradhan Mantri Jan Dhan Yojana (PMJDY)": "प्रधानमंत्री जन धन योजना (PMJDY)",
        "PM Jeevan Jyoti Bima Yojana (PMJJBY)": "पीएम जीवन ज्योती विमा योजना",
        "PM Suraksha Bima Yojana (PMSBY)": "पीएम सुरक्षा विमा योजना",
        "PM SHRI Schools": "पीएम श्री शाळा",
        "National Apprenticeship Promotion Scheme (NAPS)": "राष्ट्रीय शिकाऊ उमेदवारी प्रोत्साहन योजना",
        "Antyodaya Anna Yojana (AAY)": "अंत्योदय अन्न योजना",
        "PM PVTG Development Mission": "पीएम पीव्हीटीजी विकास मिशन",
        "Agnipath Scheme (Agniveer)": "अग्निपथ योजना (अग्निवीर)",
        "Mahila Samman Savings Certificate": "महिला सन्मान बचत प्रमाणपत्र",
        "PM eBus Sewa": "पीएम ई-बस सेवा",
        "PM Formalisation of Micro Food Processing Enterprises (PMFME)": "पीएम सूक्ष्म अन्न प्रक्रिया उद्योग औपचारिकीकरण योजना",
        "PM-DAKSH (Skill Development)": "पीएम-दक्ष (कौशल्य विकास)",
        "National Overseas Scholarship": "राष्ट्रीय परदेशी शिष्यवृत्ती",
        "PM Fasal Bima Yojana (PMFBY)": "पीएम फसल विमा योजना",
        "PM-KUSUM (Solar Pump Scheme)": "पीएम-कुसुम (सौर पंप योजना)",
        "e-Shram Card": "ई-श्रम कार्ड",
        "One Nation One Ration Card": "एक राष्ट्र एक रेशन कार्ड",
        "Beti Bachao Beti Padhao": "बेटी बचाओ बेटी पढाओ",
        "Janani Suraksha Yojana (JSY)": "जननी सुरक्षा योजना",
        "Mission Indradhanush (Immunization)": "मिशन इंद्रधनुष (लसीकरण)",
        "PM-DevINE (North East Development)": "पीएम-डिवाईन (ईशान्य विकास)",
        "Saansad Adarsh Gram Yojana (SAGY)": "सांसद आदर्श ग्राम योजना",
        "Swachh Bharat Abhiyan Assistance": "स्वच्छ भारत अभियान सहायता",
        "PM-WANI (Public Wi-Fi)": "पीएम-वाणी (सार्वजनिक वाय-फाय)",
        "National Apprenticeship Training Scheme (NATS)": "राष्ट्रीय शिकाऊ प्रशिक्षण योजना",
        "NMMS Scholarship": "NMMS शिष्यवृत्ती",
        "Pre-Matric Minority Scholarship": "मॅट्रिकपूर्व अल्पसंख्याक शिष्यवृत्ती",
        "Post-Matric Minority Scholarship": "मॅट्रिकोत्तर अल्पसंख्याक शिष्यवृत्ती",
        "Merit-cum-Means Minority Scholarship": "गुणवत्ता-निहाय अल्पसंख्याक शिष्यवृत्ती",
        "USTTAD (Minority Artisans)": "उस्ताद (अल्पसंख्याक कारागीर)",
        "SVAMITVA Scheme": "स्वामित्व योजना",
        "PM-Kisan Maandhan Yojana": "पीएम-किसान मानधन योजना",
        # Footer Terms
        "Platform": "प्लॅटफॉर्म",
        "Other Links": "इतर दुवे",
        "Legal": "कायदेशीर",
        "Developer Contact": "डेव्हलपर संपर्क",
        "Disclaimer": "डिस्क्लेमर",
        "FAQs": "वारंवार विचारले जाणारे प्रश्न",
        "AI Methodology": "एआय कार्यपद्धती",
        "User Guide": "वापरकर्ता मार्गदर्शक",
        "Terms & Conditions": "अटी आणि शर्ती",
        "Privacy Policy": "गोपनीयता धोरण",
        "Data Protection": "डेटा सुरक्षा",
        "Accessibility": "सुलभता"
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
