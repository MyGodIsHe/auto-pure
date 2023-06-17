import sqlite3
from datetime import datetime


class DataBase:
    def __init__(self) -> None:
        self.con = sqlite3.connect('likes.db')
        cur = self.con.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS likes(
                user_id TEXT PRIMARY KEY NOT NULL,
                created_at DATETIME NOT NULL,
                data TEXT
            )
            """)
        self.con.commit()

    def was_liked(self, user_id: str) -> bool:
        cur = self.con.cursor()
        res = cur.execute('SELECT COUNT(*) FROM likes WHERE user_id = ?', [user_id])
        cnt = res.fetchone()
        return cnt[0] > 0

    def set_like(self, user_id: str, data: str) -> None:
        cur = self.con.cursor()
        cur.execute(
            """
            INSERT INTO likes (user_id, created_at, data)
            VALUES (?, ?, ?)
            """,
            [user_id, datetime.utcnow(), data],
        )
        self.con.commit()

    def update_like(self, user_id: str, data: str) -> None:
        cur = self.con.cursor()
        cur.execute('UPDATE likes SET data = ? WHERE user_id = ?', [data, user_id])
        self.con.commit()

    def get_like_count(self) -> int:
        cur = self.con.cursor()
        res = cur.execute('SELECT COUNT(*) FROM likes')
        cnt = res.fetchone()
        return cnt[0]

    def search(self, query: str) -> list[str]:
        cur = self.con.cursor()
        res = cur.execute(
            """
            SELECT created_at, data FROM likes
            WHERE json_extract(data, \'$.announcement_text\') like ?
            ORDER BY created_at DESC
            """,
            ['%' + query + '%'],
        )
        return res.fetchall()
