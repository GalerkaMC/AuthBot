from aiogram import Router, F
from aiogram.types import Message
from ..messages import MESSAGES

router = Router()

@router.message(F.text == "/help")
async def cmd_help(msg: Message):
    await msg.answer(MESSAGES["help"])