"""
Database configuration for read-only operations
"""
import sqlite3
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Get database path from environment or use default
# Calculate path relative to project root (go up from backend/app/config to project root)
_project_root = Path(__file__).parent.parent.parent.parent
DB_PATH = os.getenv('DB_PATH', str(_project_root / 'database' / 'credit_risk.db'))

def get_db_connection():
    """
    Get database connection for read-only operations.
    
    Note: Database and tables must be initialized using database/scripts/seed.py
    This function only provides connection functionality.
    """
    # Ensure database directory exists (creates dir if missing, but won't create DB file)
    db_dir = os.path.dirname(DB_PATH)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir, exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Return rows as dictionaries
    return conn

# Note: Database initialization (table creation) is handled by database/scripts/seed.py
# This file only provides connection functionality for read-only operations
# To initialize the database, run: python database/scripts/seed.py
