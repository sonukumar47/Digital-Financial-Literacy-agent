"""
Multilingual support module.
Detects input language and translates between user language and English
so the RAG pipeline always works in English while users interact in their own language.
"""

from deep_translator import GoogleTranslator
from langdetect import detect, LangDetectException

# Supported languages map: display name → ISO-639-1 code
SUPPORTED_LANGUAGES = {
    "English":    "en",
    "Hindi":      "hi",
    "Tamil":      "ta",
    "Telugu":     "te",
    "Kannada":    "kn",
    "Malayalam":  "ml",
    "Bengali":    "bn",
    "Marathi":    "mr",
    "Gujarati":   "gu",
    "Punjabi":    "pa",
    "Urdu":       "ur",
    "Odia":       "or",
}

LANG_CODE_TO_NAME = {v: k for k, v in SUPPORTED_LANGUAGES.items()}

LANGUAGE_GREETINGS = {
    "hi": "नमस्ते! मैं आपका डिजिटल वित्तीय साक्षरता सहायक हूँ।",
    "ta": "வணக்கம்! நான் உங்கள் டிஜிட்டல் நிதி கல்வி உதவியாளர்.",
    "te": "నమస్కారం! నేను మీ డిజిటల్ ఆర్థిక అక్షరాస్యత సహాయకుడిని.",
    "kn": "ನಮಸ್ಕಾರ! ನಾನು ನಿಮ್ಮ ಡಿಜಿಟಲ್ ಹಣಕಾಸು ಸಾಕ್ಷರತೆ ಸಹಾಯಕ.",
    "ml": "നമസ്കാരം! ഞാൻ നിങ്ങളുടെ ഡിജിറ്റൽ സാമ്പത്തിക സാക്ഷരതാ സഹായി.",
    "bn": "নমস্কার! আমি আপনার ডিজিটাল আর্থিক সাক্ষরতা সহায়ক।",
    "mr": "नमस्कार! मी तुमचा डिजिटल आर्थिक साक्षरता सहाय्यक आहे.",
    "gu": "નમસ્તે! હું તમારો ડિજિટલ નાણાકીય સાક્ષરતા સહાયક છું.",
    "pa": "ਸਤ ਸ੍ਰੀ ਅਕਾਲ! ਮੈਂ ਤੁਹਾਡਾ ਡਿਜੀਟਲ ਵਿੱਤੀ ਸਾਖਰਤਾ ਸਹਾਇਕ ਹਾਂ।",
    "ur": "السلام علیکم! میں آپ کا ڈیجیٹل مالیاتی خواندگی کا معاون ہوں۔",
    "or": "ନମସ୍କାର! ମୁଁ ଆପଣଙ୍କ ଡିଜିଟାଲ ଆର୍ଥିକ ସାକ୍ଷରତା ସହାୟକ।",
    "en": "Hello! I am your Digital Financial Literacy Assistant.",
}


def detect_language(text: str) -> str:
    """Detect language of given text; fall back to English on failure."""
    try:
        code = detect(text)
        return code if code in SUPPORTED_LANGUAGES.values() else "en"
    except LangDetectException:
        return "en"


def translate_to_english(text: str, source_lang: str) -> str:
    """Translate text to English. Returns original text if already English."""
    if source_lang == "en":
        return text
    try:
        return GoogleTranslator(source=source_lang, target="en").translate(text)
    except Exception:
        return text  # graceful fallback


def translate_from_english(text: str, target_lang: str) -> str:
    """Translate English text to target language. Returns original if English."""
    if target_lang == "en":
        return text
    try:
        # GoogleTranslator has a 5000-char limit per call; chunk if needed
        if len(text) <= 4500:
            return GoogleTranslator(source="en", target=target_lang).translate(text)
        # Chunk on sentence boundaries
        sentences = text.split(". ")
        chunks, current = [], ""
        for s in sentences:
            if len(current) + len(s) < 4500:
                current += s + ". "
            else:
                chunks.append(current.strip())
                current = s + ". "
        if current:
            chunks.append(current.strip())
        translated_chunks = [
            GoogleTranslator(source="en", target=target_lang).translate(c)
            for c in chunks
        ]
        return " ".join(translated_chunks)
    except Exception:
        return text


def get_greeting(lang_code: str) -> str:
    return LANGUAGE_GREETINGS.get(lang_code, LANGUAGE_GREETINGS["en"])
