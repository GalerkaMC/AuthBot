'''SQLite helper for blocked players.'''
import os
import aiosqlite
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), '../../blocked_players.db')

async def create_tables() -> None:
    conn = await aiosqlite.connect(DB_PATH)
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS blocked (
            tg_user_id INTEGER PRIMARY KEY,
            blocked_at TEXT NOT NULL
        )
    ''')
    await conn.commit()

async def is_blocked(user_id: int) -> bool:
    async with aiosqlite.connect(DB_PATH) as conn:
        cur = await conn.execute('SELECT 1 FROM blocked WHERE tg_user_id = ?', (user_id,))
        row = await cur.fetchone()
        return row is not None

async def block_user(user_id: int) -> None:
    async with aiosqlite.connect(DB_PATH) as conn:
        await conn.execute('INSERT OR REPLACE INTO blocked (tg_user_id, blocked_at) VALUES (?, ?)', (user_id, datetime.utcnow().isoformat()))
        await conn.commit()
