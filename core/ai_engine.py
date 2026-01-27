import json
from openai import OpenAI
from core.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

async def transcribe_voice(file_path: str) -> str:
    """Transcribes voice message using OpenAI Whisper."""
    with open(file_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file
        )
    return transcript.text

async def extract_finance_data(text: str):
    """Extracts financial data (amount, category, type) using GPT-4."""
    prompt = f"""
    Quyidagi matndan moliyaviy ma'lumotlarni ajratib ol: "{text}"
    Natijani faqat JSON formatida qaytar:
    {{
        "amount": float,
        "category": string,
        "type": "income" yoki "expense",
        "description": string
    }}
    Agar ma'lumot topilmasa, null qiymat ber.
    """
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "Siz moliyaviy tahlilchisiz."},
                  {"role": "user", "content": prompt}],
        response_format={ "type": "json_object" }
    )
    return json.loads(response.choices[0].message.content)

async def analyze_sentiment(text: str):
    """Analyzes sentiment and provides a motivational response."""
    prompt = f"""
    Foydalanuvchi quyidagilarni yozdi: "{text}"
    1. Sentimentni aniqla (positive, negative, neutral).
    2. Agar negative bo'lsa, ARIS (qattiqqo'l lekin samimiy murabbiy) sifatida dalda ber.
    3. Agar positive bo'lsa, uni yanada ruhlantir.
    Natijani JSON formatida qaytar:
    {{
        "sentiment": "string",
        "response": "string"
    }}
    """
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "Siz ARIS - qattiqqo'l va samimiy murabbiysiz."},
                  {"role": "user", "content": prompt}],
        response_format={ "type": "json_object" }
    )
    return json.loads(response.choices[0].message.content)
