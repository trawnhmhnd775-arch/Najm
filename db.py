import aiosqlite
from typing import Optional, List, Dict, Any

class DB:
    def __init__(self, path: str):
        self.path = path
        self.conn: Optional[aiosqlite.Connection] = None

    async def init(self):
        self.conn = await aiosqlite.connect(self.path)
        self.conn.row_factory = aiosqlite.Row
        await self.conn.execute("PRAGMA foreign_keys = ON;")
        await self.conn.commit()

    async def close(self):
        if self.conn:
            await self.conn.close()

    # --- users ---
    async def ensure_user(self, user) -> Dict[str, Any]:
        await self.conn.execute(
            "INSERT OR IGNORE INTO users (id, username) VALUES (?, ?)",
            (user.id, getattr(user, "username", None))
        )
        await self.conn.commit()
        return await self.get_user(user.id)

    async def get_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        cur = await self.conn.execute("SELECT * FROM users WHERE id=?", (user_id,))
        r = await cur.fetchone(); await cur.close()
        return dict(r) if r else None

    # --- menus ---
    async def create_menu(self, title: str, parent_id: Optional[int] = None, type: str = "menu", image_file_id: Optional[str]=None, description: Optional[str]=None, request_info_type: Optional[str]=None):
        cur = await self.conn.execute(
            "INSERT INTO menus (parent_id, title, type, image_file_id, description, request_info_type) VALUES (?,?,?,?,?,?)",
            (parent_id, title, type, image_file_id, description, request_info_type)
        )
        await self.conn.commit()
        return cur.lastrowid

    async def get_children(self, parent_id: Optional[int] = None) -> List[Dict[str, Any]]:
        cur = await self.conn.execute("SELECT * FROM menus WHERE parent_id IS ? ORDER BY position, id", (parent_id,))
        rows = await cur.fetchall(); await cur.close()
        return [dict(r) for r in rows]
