"""File system watcher for monitoring database changes."""

import os
from typing import Callable
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class DatabaseFileHandler(FileSystemEventHandler):
    """Handler for database file changes."""
    
    def __init__(self, database_path: str, callback: Callable):
        super().__init__()
        self.database_path = os.path.abspath(database_path)
        self.callback = callback
    
    def on_modified(self, event):
        """Handle file modification events."""
        if not event.is_directory:
            if os.path.abspath(event.src_path) == self.database_path:
                self.callback()


class FileWatcher:
    """File system watcher for database changes."""
    
    def __init__(self, database_path: str, callback: Callable):
        self.database_path = database_path
        self.callback = callback
        self.observer = Observer()
        self.handler = DatabaseFileHandler(database_path, callback)
        
        # Watch the directory containing the database file
        watch_dir = os.path.dirname(os.path.abspath(database_path))
        self.observer.schedule(self.handler, watch_dir, recursive=False)
    
    def start(self):
        """Start watching for file changes."""
        if not self.observer.is_alive():
            self.observer.start()
    
    def stop(self):
        """Stop watching for file changes."""
        if self.observer.is_alive():
            self.observer.stop()
            self.observer.join()
    
    def __enter__(self):
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
