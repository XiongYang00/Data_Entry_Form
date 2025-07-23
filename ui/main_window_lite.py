"""Main application window without real-time sync to avoid timer issues."""

from PyQt6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, 
                             QStackedWidget, QLabel, QFrame, QSizePolicy, QPushButton)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPalette, QColor

from ui.sidebar import ModernSidebar
from ui.entry_form import DataEntryForm
from ui.data_viewer import DataViewer
from ui.dashboard import Dashboard
from database.manager import DatabaseManager
from config.settings import *


class MainWindowLite(QMainWindow):
    """Main application window without automatic sync."""
    
    def __init__(self):
        super().__init__()
        self.db_manager = DatabaseManager()
        
        self.init_ui()
        self.setup_connections()
        self.apply_theme()
        
        # Start with entry form
        self.show_entry_form()
    
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle(WINDOW_TITLE + " - Lite Mode")
        self.setMinimumSize(1200, 800)
        self.resize(1400, 900)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create sidebar
        self.sidebar = ModernSidebar()
        main_layout.addWidget(self.sidebar)
        
        # Create content area
        self.content_area = QStackedWidget()
        main_layout.addWidget(self.content_area)
        
        # Create pages
        self.dashboard = Dashboard(self.db_manager)
        self.entry_form = DataEntryForm(self.db_manager)
        self.data_viewer = DataViewer(self.db_manager)
        
        # Add pages to content area
        self.content_area.addWidget(self.dashboard)
        self.content_area.addWidget(self.entry_form)
        self.content_area.addWidget(self.data_viewer)
        
        # Status bar with manual refresh button
        self.statusBar().showMessage("Ready - Lite Mode (Manual refresh only)")
        
        # Add refresh button to status bar
        self.refresh_btn = QPushButton("🔄 Refresh Data")
        self.refresh_btn.clicked.connect(self.manual_refresh)
        self.refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 4px 8px;
                margin: 2px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        self.statusBar().addPermanentWidget(self.refresh_btn)
    
    def setup_connections(self):
        """Set up signal connections."""
        # Sidebar navigation
        self.sidebar.dashboard_requested.connect(self.show_dashboard)
        self.sidebar.entry_form_requested.connect(self.show_entry_form)
        self.sidebar.data_viewer_requested.connect(self.show_data_viewer)
        
        # Entry form signals
        self.entry_form.entry_saved.connect(self.on_entry_saved)
        
        # Data viewer signals
        self.data_viewer.entry_updated.connect(self.on_entry_updated)
        self.data_viewer.entry_deleted.connect(self.on_entry_deleted)
    
    def apply_theme(self):
        """Apply the application theme."""
        if DARK_THEME:
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #1e1e1e;
                    color: #ffffff;
                }
                QStatusBar {
                    background-color: #2d2d2d;
                    color: #ffffff;
                    border-top: 1px solid #404040;
                }
            """)
    
    def show_dashboard(self):
        """Show the dashboard."""
        self.content_area.setCurrentWidget(self.dashboard)
        self.sidebar.set_active_button("dashboard")
        self.statusBar().showMessage("Dashboard Mode - Lite")
        # Refresh dashboard data
        self.dashboard.refresh_data()
    
    def show_entry_form(self):
        """Show the data entry form."""
        self.content_area.setCurrentWidget(self.entry_form)
        self.sidebar.set_active_button("entry")
        self.statusBar().showMessage("Data Entry Mode - Lite")
    
    def show_data_viewer(self):
        """Show the data viewer."""
        self.content_area.setCurrentWidget(self.data_viewer)
        self.sidebar.set_active_button("viewer")
        self.data_viewer.refresh_data()
        self.statusBar().showMessage("Data Viewer Mode - Lite")
    
    def manual_refresh(self):
        """Manually refresh data."""
        if self.content_area.currentWidget() == self.data_viewer:
            self.data_viewer.refresh_data()
            self.statusBar().showMessage("Data refreshed manually", 3000)
        else:
            self.statusBar().showMessage("Switch to Data Viewer to refresh", 3000)
    
    def on_entry_saved(self):
        """Handle entry saved event."""
        self.statusBar().showMessage("Entry saved successfully", 3000)
        # Refresh dashboard and data viewer
        if hasattr(self, 'dashboard'):
            self.dashboard.refresh_data()
        if hasattr(self, 'data_viewer'):
            self.data_viewer.refresh_data()
    
    def on_entry_updated(self):
        """Handle entry updated event."""
        self.statusBar().showMessage("Entry updated successfully", 3000)
        # Refresh dashboard when data is updated
        if hasattr(self, 'dashboard'):
            self.dashboard.refresh_data()
    
    def on_entry_deleted(self):
        """Handle entry deleted event."""
        self.statusBar().showMessage("Entry deleted successfully", 3000)
        # Refresh dashboard when data is deleted
        if hasattr(self, 'dashboard'):
            self.dashboard.refresh_data()
    
    def closeEvent(self, event):
        """Handle application close event."""
        # No sync handler to stop in lite mode
        event.accept()
