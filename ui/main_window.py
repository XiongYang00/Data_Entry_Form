"""Main application window with modern toggle sidebar."""

from PyQt6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, 
                             QStackedWidget, QLabel, QFrame, QSizePolicy)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer
from PyQt6.QtGui import QFont, QPalette, QColor

from ui.sidebar import ModernSidebar
from ui.entry_form import DataEntryForm
from ui.data_viewer import DataViewer
from ui.dashboard import Dashboard
from database.manager import DatabaseManager
from database.sync import DatabaseSyncHandler
from config.settings import *


class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self):
        super().__init__()
        self.db_manager = DatabaseManager()
        
        # Only create sync handler when needed and with minimal timers
        self.sync_handler = None
        
        self.init_ui()
        self.setup_connections()
        self.apply_theme()
        
        # Start with dashboard
        self.show_dashboard()
        
        # Initialize sync handler after everything is set up
        self._setup_sync_handler()
    
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle(WINDOW_TITLE)
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
        
        # Status bar
        self.statusBar().showMessage("Ready")
    
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
        
        # Dashboard signals
        self.dashboard.refresh_requested.connect(self.on_dashboard_refresh)
    
    def _setup_sync_handler(self):
        """Set up sync handler with minimal resource usage."""
        try:
            self.sync_handler = DatabaseSyncHandler(self.db_manager)
            # Database sync
            self.sync_handler.database_changed.connect(self.on_database_changed)
        except Exception as e:
            print(f"Warning: Real-time sync disabled due to: {e}")
            self.sync_handler = None
    
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
        self.dashboard.refresh_data()
        self.statusBar().showMessage("Dashboard Mode")
    
    def show_entry_form(self):
        """Show the data entry form."""
        self.content_area.setCurrentWidget(self.entry_form)
        self.sidebar.set_active_button("entry")
        self.statusBar().showMessage("Data Entry Mode")
    
    def show_data_viewer(self):
        """Show the data viewer."""
        self.content_area.setCurrentWidget(self.data_viewer)
        self.sidebar.set_active_button("viewer")
        self.data_viewer.refresh_data()
        self.statusBar().showMessage("Data Viewer Mode")
    
    def on_database_changed(self):
        """Handle database change notification."""
        # Refresh current view
        current_widget = self.content_area.currentWidget()
        if current_widget == self.data_viewer:
            self.data_viewer.refresh_data()
        elif current_widget == self.dashboard:
            self.dashboard.refresh_data()
        
        # Update status
        self.statusBar().showMessage("Database updated - Data refreshed", 3000)
    
    def on_entry_saved(self):
        """Handle entry saved event."""
        self.statusBar().showMessage("Entry saved successfully", 3000)
        # Refresh dashboard and data viewer
        self.dashboard.refresh_data()
        if hasattr(self, 'data_viewer'):
            self.data_viewer.refresh_data()
    
    def on_entry_updated(self):
        """Handle entry updated event."""
        self.statusBar().showMessage("Entry updated successfully", 3000)
        # Refresh dashboard
        self.dashboard.refresh_data()
    
    def on_entry_deleted(self):
        """Handle entry deleted event."""
        self.statusBar().showMessage("Entry deleted successfully", 3000)
        # Refresh dashboard
        self.dashboard.refresh_data()
    
    def on_dashboard_refresh(self):
        """Handle dashboard refresh request."""
        self.statusBar().showMessage("Dashboard refreshed", 2000)
    
    def closeEvent(self, event):
        """Handle application close event."""
        if self.sync_handler:
            self.sync_handler.stop_monitoring()
        event.accept()
