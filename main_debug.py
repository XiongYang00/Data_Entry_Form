#!/usr/bin/env python3
"""
Data Entry Pro - Debug Version
A debug version with extensive logging to help identify issues.
"""

import sys
import os
import traceback
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def handle_exception(exc_type, exc_value, exc_traceback):
    """Handle uncaught exceptions."""
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    
    print("=" * 60)
    print("UNCAUGHT EXCEPTION:")
    print("=" * 60)
    traceback.print_exception(exc_type, exc_value, exc_traceback)
    print("=" * 60)

# Set up exception handling
sys.excepthook = handle_exception

def main():
    """Main application entry point with debug info."""
    print("Starting Data Entry Pro - Debug Version")
    print(f"Python version: {sys.version}")
    print(f"Working directory: {os.getcwd()}")
    
    try:
        app = QApplication(sys.argv)
        print("✓ QApplication created")
        
        # Set application properties
        app.setApplicationName("Data Entry Pro - Debug")
        app.setApplicationVersion("1.0.0")
        app.setOrganizationName("DataEntryApp")
        print("✓ Application properties set")
        
        # Import and initialize database
        from database.manager import DatabaseManager
        db_manager = DatabaseManager()
        db_manager.initialize_database()
        print("✓ Database initialized")
        
        # Import and create main window
        from ui.main_window_lite import MainWindowLite
        window = MainWindowLite()
        print("✓ Main window created")
        
        window.show()
        print("✓ Window shown")
        
        print("Starting application event loop...")
        return app.exec()
        
    except Exception as e:
        print(f"❌ Error during startup: {e}")
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
