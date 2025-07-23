#!/usr/bin/env python3
"""
Modern Data Entry Application
A professional desktop application for data entry with real-time database synchronization.
"""

import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.main_window import MainWindow
from database.manager import DatabaseManager


def main():
    """Main application entry point."""
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("Data Entry Pro")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("DataEntryApp")
    
    # Enable high DPI scaling (PyQt6 does this automatically)
    
    # Initialize database
    db_manager = DatabaseManager()
    db_manager.initialize_database()
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
