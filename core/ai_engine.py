import json
import google.generativeai as genai
from aris_bot.core.config import settings
from openai import OpenAI

# Gemini configuration
genai.configure(api_key=settings.OPENAI_API_KEY) # We'll reuse the env var or you can rename it
model = genai.GenerativeModel('gemini-1.5-flash')

# We still need OpenAI for Whisper (STT) because Gemini's direct audio processing 
# in Python SDK is slightly different. But for NLP/Sentiment, we use Gemini.
client = OpenAI(api_key=settings.OPENAI_API_KEY) 

async def transcribe_voice(file_path: str) -> str:
    """Transcribes voice message using OpenAI Whisper (or you can use Gemini if you upload to cloud)."""
    # Note: If you want to avoid OpenAI completely, we'd need a different STT.
    # For now, keeping Whisper as it's very accurate.
    with open(file_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file
        )
    return transcript.text

async def extract_finance_data(text: str):
    """Extracts financial data using Gemini."""
    prompt = f"""
    Quyidagi matndan moliyaviy ma'lumotlarni ajratib ol: "{text}"
    Natijani faqat JSON formatida qaytar:
    {{
        "amount": float,
        "category": string,
        "type": "income" yoki "expense",
        "description": string
    }}
    Agar ma'lumot topilmasa, null qiymat ber. Faqat JSON qaytar, boshqa matn kerak emas.
    """
    
    response = model.generate_content(prompt)
    # Clean the response text to ensure it's valid JSON
    json_text = response.text.replace('```json', '').replace('```', '').strip()
    return json.loads(json_text)

async def analyze_sentiment(text: str):
    """Analyzes sentiment using Gemini."""
    prompt = f"""
    Foydalanuvchi quyidagilarni yozdi: "{text}"
    1. Sentimentni aniqla (positive, negative, neutral).
    2. Agar negative bo'lsa, ARIS (qattiqqo'l lekin samimiy murabbiy) sifatida dalda ber.
    3. Agar positive bo'lsa, uni yanada ruhlantir.
    Natijani faqat JSON formatida qaytar:
    {{
        "sentiment": "string",
        "response": "string"
    }}
    Faqat JSON qaytar, boshqa matn kerak emas.
    """
    
    response = model.generate_content(prompt)
    json_text = response.text.replace('```json', '').replace('```', '').strip()
    return json.loads(json_text)
