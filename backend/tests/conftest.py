import os
import sqlite3
import tempfile
from collections.abc import Generator
from pathlib import Path

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.main import app as main_app

TEST_TOKEN = "token"  # noqa: S105


@pytest.fixture
def override_token():
    """Override the API token for testing purposes."""
    try:
        from app.config.config import settings  # noqa: PLC0415

        original_token: str = settings.API_TOKEN or "error"
        settings.API_TOKEN = TEST_TOKEN

        yield settings.API_TOKEN or TEST_TOKEN

    finally:
        # restore original
        settings.API_TOKEN = original_token  # type: ignore  # noqa: PGH003


@pytest.fixture
def test_db() -> Generator[str, None, None]:
    """Create a temporary database for testing."""
    fd: int
    test_db_path: str
    fd, test_db_path = tempfile.mkstemp(suffix=".db")
    os.close(fd)

    try:
        # override the database path for testing
        from app.config.config import settings  # noqa: PLC0415

        original_db_file: str = settings.DB_URL
        settings.DB_URL = test_db_path

        conn: sqlite3.Connection = sqlite3.connect(test_db_path)
        cursor: sqlite3.Cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE bottles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                barcode TEXT UNIQUE NOT NULL,
                deposit_value REAL NOT NULL,
                type TEXT NOT NULL,
                brand TEXT NOT NULL,
                added_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                redeemed BOOLEAN DEFAULT 0
            )
        """)

        conn.commit()
        conn.close()

        yield test_db_path

    finally:
        # restore original database path
        settings.DB_URL = original_db_file  # type: ignore  # noqa: PGH003
        # clean up test database
        Path(test_db_path).unlink(missing_ok=True)


@pytest.fixture
def app(test_db: str, override_token: str) -> FastAPI:  # noqa: ARG001
    """Create a FastAPI app instance for testing with explicitly set token."""
    return main_app


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    """Create a test client."""
    return TestClient(app)


@pytest.fixture
def auth_headers() -> dict[str, str]:
    """Return authentication headers for API requests."""
    # read the values from the .env file
    return {"Authorization": f"Bearer {TEST_TOKEN}"}
