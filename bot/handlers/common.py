from aiogram import Router, types
from aiogram.filters import CommandStart, Command

router = Router()

@router.message(CommandStart())
async def cmd_start(message: types.Message):
    welcome_text = (
        "Salom! Men ARIS — sizning shaxsiy yordamchingiz, moliyaviy maslahatchingiz va murabbiyingizman.\n\n"
        "Men bilan:\n"
        "💰 Xarajatlaringizni ovozli xabar orqali yozib borishingiz\n"
        "📈 Moliyaviy hisobotlar olishingiz\n"
        "📓 Audio kundalik yuritishingiz\n"
        "🔥 Va doimiy motivatsiyada bo'lishingiz mumkin.\n\n"
        "Dangasalikni yig'ishtiring, ishni boshlaymiz!"
    )
    await message.answer(welcome_text)

@router.message(Command("help"))
async def cmd_help(message: types.Message):
    help_text = (
        "Buyruqlar:\n"
        "/start - Botni ishga tushirish\n"
        "/report - Moliyaviy hisobot\n"
        "/goals - Maqsadlarni ko'rish\n"
        "Ovozli xabar yuboring - Moliya yoki Kundalik uchun."
    )
    await message.answer(help_text)
