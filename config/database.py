"""Database configuration and connection setup."""

import sqlite3
import os
from typing import Optional
from config.settings import DATABASE_PATH, SHARED_FOLDER_PATH


class DatabaseConfig:
    """Database configuration class."""
    
    def __init__(self):
        self.database_path = self._get_database_path()
    
    def _get_database_path(self) -> str:
        """Get the full path to the database file."""
        if os.path.exists(SHARED_FOLDER_PATH):
            return os.path.join(SHARED_FOLDER_PATH, DATABASE_PATH)
        else:
            # Fallback to local database if shared folder is not available
            return DATABASE_PATH
    
    def get_connection(self) -> sqlite3.Connection:
        """Get a database connection."""
        conn = sqlite3.connect(self.database_path)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        return conn
    
    @property
    def is_shared(self) -> bool:
        """Check if database is on shared folder."""
        return SHARED_FOLDER_PATH in self.database_path
