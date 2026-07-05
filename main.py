import asyncio

import uvicorn

from src.backend.two_factor_authentication.server.app import app
from src.client.ClientFabric import ClientFabric
from setup_logging import setup_logging

async def _run():
    setup_logging()
    bot = ClientFabric().get()
    bot_task = asyncio.create_task(bot.run())
    config = uvicorn.Config(app, host="0.0.0.0", port=8000)
    server = uvicorn.Server(config)
    await server.serve()
    bot_task.cancel()

if __name__ == "__main__":
    asyncio.run(_run())
