from aiogram import Router, F
from aiogram.filters.callback_data import CallbackData
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

router = Router()

class BotCallback(CallbackData, prefix="bot"):
    action: str
    jwt: str

@router.callback_query(BotCallback.filter(F.action == "auth"))
async def handle_auth(cb: CallbackQuery, callback_data: BotCallback):
    # Placeholder: acknowledge receipt of JWT
    await cb.answer()
    await cb.message.edit_text(f"Received JWT: {callback_data.jwt}")

def auth_button(jwt: str) -> InlineKeyboardMarkup:
    btn = InlineKeyboardButton(
        text="Confirm",
        callback_data=BotCallback(action="auth", jwt=jwt).pack()
    )
    return InlineKeyboardMarkup(inline_keyboard=[[btn]])