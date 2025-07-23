"""Modern collapsible sidebar with navigation buttons."""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QLabel, 
                             QFrame, QSizePolicy, QSpacerItem)
from PyQt6.QtCore import Qt, pyqtSignal, QPropertyAnimation, QEasingCurve, QSize
from PyQt6.QtGui import QFont, QIcon, QPalette, QColor

from config.settings import *


class ModernButton(QPushButton):
    """Modern styled button for sidebar."""
    
    def __init__(self, text: str, icon_text: str = ""):
        super().__init__()
        self.full_text = text
        self.icon_text = icon_text
        self.is_active = False
        
        self.setText(text)
        self.setMinimumHeight(50)
        self.setFont(QFont("Segoe UI", 10))
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        self.apply_style()
    
    def apply_style(self):
        """Apply modern button styling."""
        active_style = f"""
            QPushButton {{
                background-color: {PRIMARY_COLOR};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px;
                text-align: left;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #1976D2;
            }}
        """
        
        inactive_style = f"""
            QPushButton {{
                background-color: transparent;
                color: {TEXT_COLOR};
                border: none;
                border-radius: 8px;
                padding: 12px;
                text-align: left;
            }}
            QPushButton:hover {{
                background-color: rgba(255, 255, 255, 0.1);
            }}
        """
        
        self.setStyleSheet(active_style if self.is_active else inactive_style)
    
    def set_active(self, active: bool):
        """Set button active state."""
        self.is_active = active
        self.apply_style()
    
    def set_collapsed(self, collapsed: bool):
        """Set button text for collapsed state."""
        if collapsed:
            self.setText(self.icon_text)
        else:
            self.setText(self.full_text)


class ModernSidebar(QFrame):
    """Modern collapsible sidebar widget."""
    
    # Signals
    entry_form_requested = pyqtSignal()
    data_viewer_requested = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.is_collapsed = False
        self.init_ui()
        self.apply_theme()
    
    def init_ui(self):
        """Initialize the sidebar UI."""
        self.setFixedWidth(SIDEBAR_WIDTH)
        self.setFrameStyle(QFrame.Shape.NoFrame)
        
        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(8)
        
        # Header
        self.header_label = QLabel("Navigation")
        self.header_label.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        self.header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.header_label)
        
        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet("color: #404040;")
        layout.addWidget(separator)
        
        # Navigation buttons
        self.entry_btn = ModernButton("📝 Data Entry", "📝")
        self.viewer_btn = ModernButton("📊 View Data", "📊")
        self.toggle_btn = ModernButton("◀ Collapse", "▶")
        
        layout.addWidget(self.entry_btn)
        layout.addWidget(self.viewer_btn)
        
        # Spacer
        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        
        # Toggle button at bottom
        layout.addWidget(self.toggle_btn)
        
        # Connect signals
        self.entry_btn.clicked.connect(self.on_entry_clicked)
        self.viewer_btn.clicked.connect(self.on_viewer_clicked)
        self.toggle_btn.clicked.connect(self.toggle_sidebar)
        
        # Set initial active button
        self.set_active_button("entry")
    
    def apply_theme(self):
        """Apply sidebar theme."""
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {BACKGROUND_COLOR if DARK_THEME else '#f5f5f5'};
                border-right: 1px solid #404040;
            }}
            QLabel {{
                color: {TEXT_COLOR};
            }}
        """)
    
    def on_entry_clicked(self):
        """Handle entry form button click."""
        self.set_active_button("entry")
        self.entry_form_requested.emit()
    
    def on_viewer_clicked(self):
        """Handle data viewer button click."""
        self.set_active_button("viewer")
        self.data_viewer_requested.emit()
    
    def set_active_button(self, button_name: str):
        """Set the active navigation button."""
        self.entry_btn.set_active(button_name == "entry")
        self.viewer_btn.set_active(button_name == "viewer")
    
    def toggle_sidebar(self):
        """Toggle sidebar collapsed state."""
        self.is_collapsed = not self.is_collapsed
        
        # Create animation
        self.animation = QPropertyAnimation(self, b"minimumWidth")
        self.animation.setDuration(ANIMATION_DURATION)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutCubic)
        
        if self.is_collapsed:
            self.animation.setEndValue(SIDEBAR_COLLAPSED_WIDTH)
            self.toggle_btn.setText("▶")
            self.header_label.hide()
        else:
            self.animation.setEndValue(SIDEBAR_WIDTH)
            self.toggle_btn.setText("◀")
            self.header_label.show()
        
        # Update button text
        self.entry_btn.set_collapsed(self.is_collapsed)
        self.viewer_btn.set_collapsed(self.is_collapsed)
        
        self.animation.start()
