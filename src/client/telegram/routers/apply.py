'''Apply form using FSM.'''
import logging
import os
import re

import dotenv
import aiohttp
from aiogram import Router, F
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters.callback_data import CallbackData

from ..messages import MESSAGES
from ..blocked_db import is_blocked, block_user
from src.client.ClientFabric import ClientFabric

logger = logging.getLogger("bot")

dotenv.load_dotenv(".env.config")

router = Router()

# Admin chat ID from .env.config
ADMIN_CHAT_ID = int(os.getenv('ADMIN_CHAT_ID', '0'))

# Regex for Minecraft nick (3-16 chars, alnum and _ )
NICK_REGEX = re.compile(r'^[a-zA-Z0-9_]{3,16}$')


class ApplyForm(StatesGroup):
    name = State()
    nick = State()
    source = State()


class ApplyCallback(CallbackData, prefix='apply'):
    action: str  # accept, reject, block
    user_id: str
    nickname: str


@router.message(F.text == '/whitelist')
async def cmd_apply(msg: Message, state: FSMContext):
    """Whitelist request command"""
    if await is_blocked(msg.from_user.id):
        await msg.answer(MESSAGES['apply_blocked_user'])
        return

    minecraft_host = os.getenv('MINECRAFT_SERVER_BASE_URL')
    check_path = os.getenv('WHITELIST_CHECK_URL')
    user_id = msg.from_user.id

    # Check player in whitelist
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{minecraft_host}{check_path}?userId={user_id}") as response:

            if response.status != 200:
                logger.error(
                    f"unexpected response in check whitelist exists, details: {await response.text()}, {response.status}")
                return

            json_ = await response.json()
            exists = json_["exists"]

            if exists:
                await msg.answer(MESSAGES['apply_already_in_whitelist'])
                return

            await state.set_state(ApplyForm.name)
            await msg.answer(MESSAGES['apply_name'])


@router.message(F.text == "/cancel")
async def cancel(message: Message, state: FSMContext):
    """Отменить заполнение формы"""
    await state.clear()
    await message.answer(MESSAGES['apply_form_input_canceled'])


@router.message(ApplyForm.name)
async def process_name(msg: Message, state: FSMContext):
    await state.update_data(name=msg.text)
    await state.set_state(ApplyForm.nick)
    await msg.answer(MESSAGES['apply_nick'])


@router.message(ApplyForm.nick)
async def process_nick(msg: Message, state: FSMContext):
    if not NICK_REGEX.fullmatch(msg.text):
        await msg.answer(MESSAGES['apply_nickname_is_invalid'])
        return

    minecraft_host = os.getenv('MINECRAFT_SERVER_BASE_URL')
    path = os.getenv("WHITELIST_EXISTS_BY_NICKNAME_URL")
    nickname = msg.text

    async with aiohttp.ClientSession() as session:
        async with session.get(f"{minecraft_host}{path}?nickname={nickname}") as response:
            if response.status != 200:
                logger.error(f"error in whitelist accept, details: {await response.text()}, {response.status}")
                return

            json_ = await response.json()
            print(json_)
            if json_["exists"]:
                await msg.answer(MESSAGES['apply_nickname_already_exists'])
                return

    await state.update_data(nick=msg.text)
    await state.set_state(ApplyForm.source)
    await msg.answer(MESSAGES['apply_source'])


@router.message(ApplyForm.source)
async def process_source(msg: Message, state: FSMContext):
    await state.update_data(source=msg.text)
    data = await state.get_data()
    await state.clear()

    admin_text = (
        f"Новая заявка:\nИмя: {data['name']}\nНик: {data['nick']}\nИсточник: {data['source']}\nUserID: {msg.from_user.id}\nЮзернейм: {msg.from_user.username}"
    )
    kb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text=MESSAGES['apply_btn_accept'],
                             callback_data=ApplyCallback(
                                 action='accept',
                                 user_id=str(msg.from_user.id),
                                 nickname=data['nick']).pack()),
        InlineKeyboardButton(text=MESSAGES['apply_btn_reject'],
                             callback_data=ApplyCallback(
                                 action='reject',
                                 user_id=str(msg.from_user.id),
                                 nickname=data['nick']).pack()),
        InlineKeyboardButton(text=MESSAGES['apply_btn_block'],
                             callback_data=ApplyCallback(
                                 action='block',
                                 user_id=str(msg.from_user.id),
                                 nickname=data['nick']).pack())
    ]])
    bot = ClientFabric().get().bot
    await bot.send_message(chat_id=ADMIN_CHAT_ID, text=admin_text, reply_markup=kb)
    await msg.answer(MESSAGES['apply_send_to_admins'])


def _is_admin(cb: CallbackQuery) -> bool:
    return cb.message and cb.message.chat.id == ADMIN_CHAT_ID


@router.callback_query(ApplyCallback.filter())
async def handle_apply(cb: CallbackQuery, callback_data: ApplyCallback):
    if not _is_admin(cb):
        await cb.answer(MESSAGES['apply_forbidden'], show_alert=True)
        return
    user_id = int(callback_data.user_id)
    action = callback_data.action
    bot = ClientFabric().get().bot
    status_map = {
        'accept': MESSAGES['apply_request_status_apply'],
        'reject': MESSAGES['apply_request_status_reject'],
        'block': MESSAGES['apply_request_status_blocked']
    }
    await cb.message.edit_text(cb.message.text + f"\n{status_map.get(action, '')}")
    await cb.answer()
    if action == 'accept':
        await bot.send_message(user_id, MESSAGES['apply_success_user'])
        await on_accept(user_id, callback_data.nickname)
    elif action == 'reject':
        await bot.send_message(user_id, MESSAGES['apply_reject_user'])
    elif action == 'block':
        await block_user(user_id)
        await bot.send_message(user_id, MESSAGES['apply_blocked_user'])


async def on_accept(user_id: int, nickname: str):
    minecraft_host = os.getenv('MINECRAFT_SERVER_BASE_URL')
    path = os.getenv("WHITELIST_ADD_URL")
    data = {
        "userId": user_id,
        "nickname": nickname
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(f"{minecraft_host}{path}", json=data) as response:
            if response.status == 200:
                return
            else:
                logger.error(f"error in whitelist accept, details: {await response.text()}, {response.status}")
