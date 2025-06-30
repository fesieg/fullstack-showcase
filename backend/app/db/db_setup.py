import sqlite3
from collections.abc import Generator

from app.config.config import settings
from app.utils.logs import logger


def get_db_conn() -> Generator[sqlite3.Connection, None, None]:
    conn = sqlite3.connect(settings.DB_URL)
    try:
        yield conn
    finally:
        conn.close()


def init_db() -> None:
    # init connection
    conn = sqlite3.connect(settings.DB_URL)
    cursor = conn.cursor()

    # create tables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT NOT NULL UNIQUE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bottles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id int NOT NULL,
            barcode TEXT NOT NULL UNIQUE,
            deposit_value REAL NOT NULL,
            type TEXT NOT NULL CHECK(type IN ('plastic', 'glass', 'metal')),
            brand TEXT NOT NULL,
            added_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            redeemed BOOLEAN NOT NULL DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)

    if settings.SEED_DB:
        logger.debug("Seeding the database with initial data (if empty)...")

        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT OR IGNORE INTO users (user_name) VALUES ('user1')")
            cursor.execute("INSERT OR IGNORE INTO users (user_name) VALUES ('user2')")

        # check if bottles table is empty
        cursor.execute("SELECT COUNT(*) FROM bottles")
        if cursor.fetchone()[0] == 0:
            cursor.execute("""
              INSERT OR IGNORE INTO bottles (user_id, barcode, deposit_value, type, brand)
              VALUES (1, '1234567890123', 0.25, 'plastic', 'BrandA')
          """)
            cursor.execute("""
              INSERT OR IGNORE INTO bottles (user_id, barcode, deposit_value, type, brand)
              VALUES (2, '9876543210987', 0.50, 'glass', 'BrandB')
          """)

    conn.commit()
    conn.close()
