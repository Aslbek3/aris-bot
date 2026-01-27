import os
from aiogram import Router, types, F
from core.ai_engine import transcribe_voice, extract_finance_data
from core.config import settings
from database.requests import add_transaction

router = Router()

@router.message(F.voice)
async def handle_voice_finance(message: types.Message, bot):
    # 1. Download voice file
    file_id = message.voice.file_id
    file = await bot.get_file(file_id)
    file_path = os.path.join(settings.VOICE_DIR, f"{file_id}.ogg")
    await bot.download_file(file.file_path, file_path)
    
    # 2. Transcribe
    text = await transcribe_voice(file_path)
    
    # 3. Extract data
    data = await extract_finance_data(text)
    
    if data and data.get("amount"):
        # 4. Save to DB
        await add_transaction(
            user_id=message.from_user.id,
            amount=data["amount"],
            category=data["category"],
            trans_type=data["type"],
            description=data.get("description", text)
        )
        
        response = (
            f"✅ Saqlandi!\n"
            f"Summa: {data['amount']}\n"
            f"Kategoriya: {data['category']}\n"
            f"Tur: {data['type']}"
        )
    else:
        # If not finance, maybe it's a diary entry? 
        # (This logic can be expanded to route to diary.py)
        response = f"Tushundim: \"{text}\"\nLekin moliyaviy ma'lumot topa olmadim."
        
    await message.answer(response)
