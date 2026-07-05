from aiogram import Router, F
from aiogram.types import Message
from ..messages import MESSAGES

router = Router()

@router.message(F.text == "/start")
async def cmd_start(msg: Message):
    await msg.answer(MESSAGES["start"])