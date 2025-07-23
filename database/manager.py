"""Database manager for handling all database operations."""

import sqlite3
import os
from typing import List, Optional, Dict, Any
from datetime import datetime

from config.database import DatabaseConfig
from database.models import DataEntry, CREATE_TABLES


class DatabaseManager:
    """Manages all database operations."""
    
    def __init__(self):
        self.config = DatabaseConfig()
        self._last_modified = None
    
    def initialize_database(self) -> None:
        """Initialize the database with required tables."""
        try:
            with self.config.get_connection() as conn:
                conn.executescript(CREATE_TABLES)
                conn.commit()
            print(f"Database initialized at: {self.config.database_path}")
        except Exception as e:
            print(f"Error initializing database: {e}")
            raise
    
    def get_last_modified(self) -> Optional[datetime]:
        """Get the last modification time of the database file."""
        try:
            if os.path.exists(self.config.database_path):
                timestamp = os.path.getmtime(self.config.database_path)
                return datetime.fromtimestamp(timestamp)
        except Exception as e:
            print(f"Error getting last modified time: {e}")
        return None
    
    def has_database_changed(self) -> bool:
        """Check if the database has been modified since last check."""
        current_modified = self.get_last_modified()
        if self._last_modified is None:
            self._last_modified = current_modified
            return True
        
        if current_modified != self._last_modified:
            self._last_modified = current_modified
            return True
        
        return False
    
    def create_entry(self, entry: DataEntry) -> int:
        """Create a new data entry."""
        try:
            with self.config.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO data_entries (name, email, phone, company, position, notes, created_by)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (entry.name, entry.email, entry.phone, entry.company, 
                      entry.position, entry.notes, entry.created_by))
                conn.commit()
                return cursor.lastrowid
        except Exception as e:
            print(f"Error creating entry: {e}")
            raise
    
    def get_all_entries(self) -> List[DataEntry]:
        """Get all data entries."""
        try:
            with self.config.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT id, name, email, phone, company, position, notes,
                           created_at, updated_at, created_by
                    FROM data_entries
                    ORDER BY updated_at DESC
                """)
                rows = cursor.fetchall()
                
                entries = []
                for row in rows:
                    entry = DataEntry(
                        id=row['id'],
                        name=row['name'],
                        email=row['email'],
                        phone=row['phone'],
                        company=row['company'],
                        position=row['position'],
                        notes=row['notes'],
                        created_at=datetime.fromisoformat(row['created_at']) if row['created_at'] else None,
                        updated_at=datetime.fromisoformat(row['updated_at']) if row['updated_at'] else None,
                        created_by=row['created_by']
                    )
                    entries.append(entry)
                
                return entries
        except Exception as e:
            print(f"Error getting entries: {e}")
            return []
    
    def update_entry(self, entry: DataEntry) -> bool:
        """Update an existing data entry."""
        try:
            with self.config.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE data_entries
                    SET name=?, email=?, phone=?, company=?, position=?, notes=?
                    WHERE id=?
                """, (entry.name, entry.email, entry.phone, entry.company,
                      entry.position, entry.notes, entry.id))
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Error updating entry: {e}")
            return False
    
    def delete_entry(self, entry_id: int) -> bool:
        """Delete a data entry."""
        try:
            with self.config.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM data_entries WHERE id=?", (entry_id,))
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Error deleting entry: {e}")
            return False
    
    def get_entry_count(self) -> int:
        """Get the total number of entries."""
        try:
            with self.config.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM data_entries")
                return cursor.fetchone()[0]
        except Exception as e:
            print(f"Error getting entry count: {e}")
            return 0
