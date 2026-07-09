import asyncio

import uvicorn

from src.backend.two_factor_authentication.server.app import app
from src.client.telegram.blocked_db import create_tables
from src.client.telegram.TelegramBot import TelegramBot
from setup_logging import setup_logging

async def _run():
    setup_logging()
    bot = TelegramBot()
    bot_task = asyncio.create_task(bot.run())
    database_task = asyncio.create_task(create_tables())
    config = uvicorn.Config(app, host="0.0.0.0", port=8000)
    server = uvicorn.Server(config)
    await server.serve()
    bot_task.cancel()

if __name__ == "__main__":
    asyncio.run(_run())
