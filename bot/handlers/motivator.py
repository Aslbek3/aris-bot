from aiogram import Router, types, F
from core.ai_engine import analyze_sentiment
from database.requests import add_diary_entry

router = Router()

@router.message(F.text)
async def handle_text_message(message: types.Message):
    # Analyze sentiment for every text message (or diary entry)
    analysis = await analyze_sentiment(message.text)
    
    # Save as diary entry if it's long enough
    if len(message.text) > 10:
        await add_diary_entry(
            user_id=message.from_user.id,
            content=message.text,
            sentiment=analysis["sentiment"],
            voice_file_id=None
        )
    
    # Respond with ARIS persona
    await message.answer(analysis["response"])
