import sqlite3
from contextlib import contextmanager
import logging

class Database:
    def __init__(self, db_name='ems_boards.db'):
        self.db_name = db_name
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self.create_tables()

    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row  # This allows accessing columns by name
        try:
            yield conn
        except sqlite3.Error as e:
            self.logger.error(f"Database error: {e}")
            raise
        finally:
            conn.close()

    def create_tables(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS boards (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    type TEXT NOT NULL,
                    manufacturer TEXT NOT NULL,
                    manufacture_date TEXT NOT NULL,
                    notes TEXT
                )
            ''')
            conn.commit()
            self.logger.info("Database tables created successfully")

    def insert_board(self, board_info):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO boards (id, name, type, manufacturer, manufacture_date, notes)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                board_info['id'],
                board_info['name'],
                board_info['type'],
                board_info['manufacturer'],
                board_info['manufacture_date'],
                board_info['notes']
            ))
            conn.commit()
            self.logger.info(f"Board inserted/updated: {board_info['id']}")
        return True

    def get_all_boards(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM boards")
            rows = cursor.fetchall()
            boards = [dict(row) for row in rows]
            self.logger.info(f"Retrieved {len(boards)} boards")
            return boards

    def id_exists(self, board_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM boards WHERE id = ?", (board_id,))
            count = cursor.fetchone()[0]
            return count > 0

    def update_board(self, board_id, updated_info):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE boards
                SET name = ?, type = ?, manufacturer = ?, manufacture_date = ?, notes = ?
                WHERE id = ?
            """, (
                updated_info['name'],
                updated_info['type'],
                updated_info['manufacturer'],
                updated_info['manufacture_date'],
                updated_info['notes'],
                board_id
            ))
            conn.commit()
            if cursor.rowcount > 0:
                self.logger.info(f"Board updated: {board_id}")
                return True
            else:
                self.logger.warning(f"No board found with id: {board_id}")
                return False

    def delete_board(self, board_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM boards WHERE id = ?", (board_id,))
            conn.commit()
            if cursor.rowcount > 0:
                self.logger.info(f"Board deleted: {board_id}")
                return True
            else:
                self.logger.warning(f"No board found with id: {board_id}")
                return False

    def get_board_by_id(self, board_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM boards WHERE id = ?", (board_id,))
            row = cursor.fetchone()
            if row:
                self.logger.info(f"Retrieved board: {board_id}")
                return dict(row)
            else:
                self.logger.warning(f"No board found with id: {board_id}")
                return None