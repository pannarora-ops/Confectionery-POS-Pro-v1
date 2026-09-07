"""
Database connection configuration.

Creates the SQLAlchemy engine used throughout the application.
"""

from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

# Project Root
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Database Folder
DATA_DIR = PROJECT_ROOT / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# SQLite Database File
DATABASE_FILE = DATA_DIR / "confectionery_pos.db"

# SQLAlchemy Database URL
DATABASE_URL = f"sqlite:///{DATABASE_FILE}"

# SQLAlchemy Engine
engine: Engine = create_engine(
    DATABASE_URL,
    echo=False,
    future=True,
    connect_args={
        "check_same_thread": False,
        "timeout": 30,
    },
)