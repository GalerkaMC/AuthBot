from aiogram import Router, F
from aiogram.filters.callback_data import CallbackData
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from src.client.ClientFabric import ClientFabric
from src.backend.two_factor_authentication.entities import Status
from src.backend.two_factor_authentication.entities import TwoFAEntitiesManager

router = Router()

class BotCallback(CallbackData, prefix="bot"):
    action: str
    payload: str

@router.callback_query(BotCallback.filter(F.action == "auth"))
async def handle_auth(cb: CallbackQuery, callback_data: BotCallback):
    payload = callback_data.payload

    # Telegram гарантирует, что userId нельзя подделать
    # Поэтому можно проверить ID на клиенте.
    # В другом случае замените это
    if int(payload) != cb.from_user.id:
        await ClientFabric().get().send_result(cb.from_user.id , Status.illegal)
        return

    entity = TwoFAEntitiesManager().get(payload)
    if not entity:
        await ClientFabric().get().send_result(cb.from_user.id , Status.expired)
        return

    await entity.confirm()


def auth_button(payload: str) -> InlineKeyboardMarkup:
    btn = InlineKeyboardButton(
        text="Confirm",
        callback_data=BotCallback(action="auth", payload=payload).pack()
    )
    return InlineKeyboardMarkup(inline_keyboard=[[btn]])