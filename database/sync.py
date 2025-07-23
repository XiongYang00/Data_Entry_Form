"""Real-time synchronization handler for database changes."""

import os
from typing import Callable, Optional
from PyQt6.QtCore import QObject, QTimer, pyqtSignal, QFileSystemWatcher
from database.manager import DatabaseManager


class DatabaseSyncHandler(QObject):
    """Handles real-time database synchronization."""
    
    # Signals
    database_changed = pyqtSignal()
    
    def __init__(self, database_manager: DatabaseManager):
        super().__init__()
        self.db_manager = database_manager
        self.file_watcher = None
        self.poll_timer = None
        self._monitoring = False
        
        # Only create timer when needed
        self._setup_monitoring()
    
    def _setup_monitoring(self):
        """Set up monitoring components."""
        if self._monitoring:
            return
            
        try:
            # Set up file system watcher
            self.file_watcher = QFileSystemWatcher()
            if os.path.exists(self.db_manager.config.database_path):
                self.file_watcher.addPath(self.db_manager.config.database_path)
            
            # Connect signals
            self.file_watcher.fileChanged.connect(self._on_file_changed)
            
            # Set up polling timer as backup (much longer interval)
            self.poll_timer = QTimer()
            self.poll_timer.timeout.connect(self._check_for_changes)
            self.poll_timer.setSingleShot(False)
            self.poll_timer.start(30000)  # Check every 30 seconds only
            
            self._monitoring = True
            
        except Exception as e:
            print(f"Warning: Could not set up file monitoring: {e}")
            # Fall back to manual refresh only
    
    def _on_file_changed(self, path: str) -> None:
        """Handle file system change event."""
        if path == self.db_manager.config.database_path:
            self.database_changed.emit()
            
            # Re-add the path to watcher (sometimes it gets removed)
            if self.file_watcher and not self.file_watcher.files():
                try:
                    self.file_watcher.addPath(path)
                except Exception as e:
                    print(f"Warning: Could not re-add file to watcher: {e}")
    
    def _check_for_changes(self) -> None:
        """Periodically check for database changes (fallback method)."""
        try:
            if self.db_manager.has_database_changed():
                self.database_changed.emit()
        except Exception as e:
            print(f"Warning: Error checking for database changes: {e}")
    
    def start_monitoring(self) -> None:
        """Start monitoring for database changes."""
        if not self._monitoring:
            self._setup_monitoring()
    
    def stop_monitoring(self) -> None:
        """Stop monitoring for database changes."""
        if self.poll_timer and self.poll_timer.isActive():
            self.poll_timer.stop()
        
        if self.file_watcher:
            # Remove all paths and delete watcher
            for path in self.file_watcher.files():
                self.file_watcher.removePath(path)
            
        self._monitoring = False
    
    def refresh_file_path(self) -> None:
        """Refresh the file path being watched."""
        if not self.file_watcher:
            return
            
        try:
            # Remove all current paths
            for path in self.file_watcher.files():
                self.file_watcher.removePath(path)
            
            # Add current database path
            if os.path.exists(self.db_manager.config.database_path):
                self.file_watcher.addPath(self.db_manager.config.database_path)
        except Exception as e:
            print(f"Warning: Error refreshing file path: {e}")
    
    def __del__(self):
        """Cleanup when object is destroyed."""
        self.stop_monitoring()
