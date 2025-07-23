"""Data entry form with modern styling and validation."""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
                             QLineEdit, QTextEdit, QPushButton, QLabel, QFrame,
                             QScrollArea, QSizePolicy, QMessageBox, QGroupBox)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QPalette

import os
from database.manager import DatabaseManager
from database.models import DataEntry
from config.settings import *


class ModernLineEdit(QLineEdit):
    """Modern styled line edit."""
    
    def __init__(self, placeholder: str = ""):
        super().__init__()
        self.setPlaceholderText(placeholder)
        self.setMinimumHeight(40)
        self.setFont(QFont("Segoe UI", 10))
        self.apply_style()
    
    def apply_style(self):
        """Apply modern styling."""
        self.setStyleSheet(f"""
            QLineEdit {{
                border: 2px solid #404040;
                border-radius: 8px;
                padding: 8px 12px;
                background-color: {BACKGROUND_COLOR if DARK_THEME else 'white'};
                color: {TEXT_COLOR};
                font-size: 14px;
            }}
            QLineEdit:focus {{
                border-color: {PRIMARY_COLOR};
                background-color: {'#2d2d2d' if DARK_THEME else '#f8f9fa'};
            }}
        """)


class ModernTextEdit(QTextEdit):
    """Modern styled text edit."""
    
    def __init__(self, placeholder: str = ""):
        super().__init__()
        self.setPlaceholderText(placeholder)
        self.setMinimumHeight(100)
        self.setMaximumHeight(150)
        self.setFont(QFont("Segoe UI", 10))
        self.apply_style()
    
    def apply_style(self):
        """Apply modern styling."""
        self.setStyleSheet(f"""
            QTextEdit {{
                border: 2px solid #404040;
                border-radius: 8px;
                padding: 8px 12px;
                background-color: {BACKGROUND_COLOR if DARK_THEME else 'white'};
                color: {TEXT_COLOR};
                font-size: 14px;
            }}
            QTextEdit:focus {{
                border-color: {PRIMARY_COLOR};
                background-color: {'#2d2d2d' if DARK_THEME else '#f8f9fa'};
            }}
        """)


class ModernButton(QPushButton):
    """Modern styled button."""
    
    def __init__(self, text: str, primary: bool = False):
        super().__init__(text)
        self.is_primary = primary
        self.setMinimumHeight(45)
        self.setFont(QFont("Segoe UI", 11, QFont.Weight.Medium))
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.apply_style()
    
    def apply_style(self):
        """Apply button styling."""
        if self.is_primary:
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: {PRIMARY_COLOR};
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 12px 24px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background-color: #1976D2;
                }}
                QPushButton:pressed {{
                    background-color: #0D47A1;
                }}
            """)
        else:
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: transparent;
                    color: {TEXT_COLOR};
                    border: 2px solid #404040;
                    border-radius: 8px;
                    padding: 12px 24px;
                }}
                QPushButton:hover {{
                    background-color: rgba(255, 255, 255, 0.1);
                    border-color: {PRIMARY_COLOR};
                }}
            """)


class DataEntryForm(QWidget):
    """Modern data entry form widget."""
    
    # Signals
    entry_saved = pyqtSignal()
    
    def __init__(self, db_manager: DatabaseManager):
        super().__init__()
        self.db_manager = db_manager
        self.init_ui()
        self.apply_theme()
    
    def init_ui(self):
        """Initialize the form UI."""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(32, 32, 32, 32)
        main_layout.setSpacing(24)
        
        # Header
        header = QLabel("Data Entry Form")
        header.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(header)
        
        # Subtitle
        subtitle = QLabel("Enter new data record")
        subtitle.setFont(QFont("Segoe UI", 12))
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet(f"color: {'#b0b0b0' if DARK_THEME else '#666666'};")
        main_layout.addWidget(subtitle)
        
        # Scroll area for form
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        main_layout.addWidget(scroll)
        
        # Form widget
        form_widget = QWidget()
        scroll.setWidget(form_widget)
        
        # Form layout
        form_layout = QVBoxLayout(form_widget)
        form_layout.setSpacing(20)
        
        # Personal Information Group
        personal_group = QGroupBox("Personal Information")
        personal_group.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        personal_layout = QFormLayout(personal_group)
        personal_layout.setSpacing(16)
        
        self.name_edit = ModernLineEdit("Enter full name")
        self.email_edit = ModernLineEdit("Enter email address")
        self.phone_edit = ModernLineEdit("Enter phone number")
        
        personal_layout.addRow("Name *:", self.name_edit)
        personal_layout.addRow("Email:", self.email_edit)
        personal_layout.addRow("Phone:", self.phone_edit)
        
        form_layout.addWidget(personal_group)
        
        # Professional Information Group
        professional_group = QGroupBox("Professional Information")
        professional_group.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        professional_layout = QFormLayout(professional_group)
        professional_layout.setSpacing(16)
        
        self.company_edit = ModernLineEdit("Enter company name")
        self.position_edit = ModernLineEdit("Enter position/title")
        
        professional_layout.addRow("Company:", self.company_edit)
        professional_layout.addRow("Position:", self.position_edit)
        
        form_layout.addWidget(professional_group)
        
        # Additional Information Group
        additional_group = QGroupBox("Additional Information")
        additional_group.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        additional_layout = QFormLayout(additional_group)
        additional_layout.setSpacing(16)
        
        self.notes_edit = ModernTextEdit("Enter additional notes or comments")
        additional_layout.addRow("Notes:", self.notes_edit)
        
        form_layout.addWidget(additional_group)
        
        # Button layout
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.clear_btn = ModernButton("Clear Form")
        self.save_btn = ModernButton("Save Entry", primary=True)
        
        button_layout.addWidget(self.clear_btn)
        button_layout.addWidget(self.save_btn)
        
        main_layout.addLayout(button_layout)
        
        # Connect signals
        self.save_btn.clicked.connect(self.save_entry)
        self.clear_btn.clicked.connect(self.clear_form)
        
        # Apply group box styling
        self.apply_group_styling(personal_group)
        self.apply_group_styling(professional_group)
        self.apply_group_styling(additional_group)
    
    def apply_group_styling(self, group_box: QGroupBox):
        """Apply styling to group boxes."""
        group_box.setStyleSheet(f"""
            QGroupBox {{
                font-weight: bold;
                border: 2px solid #404040;
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 12px;
                color: {TEXT_COLOR};
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 8px;
                background-color: {BACKGROUND_COLOR};
                color: {PRIMARY_COLOR};
            }}
        """)
    
    def apply_theme(self):
        """Apply form theme."""
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {BACKGROUND_COLOR};
                color: {TEXT_COLOR};
            }}
            QScrollArea {{
                border: none;
                background-color: {BACKGROUND_COLOR};
            }}
        """)
    
    def save_entry(self):
        """Save the current entry."""
        # Validate required fields
        if not self.name_edit.text().strip():
            QMessageBox.warning(self, "Validation Error", "Name is required!")
            self.name_edit.setFocus()
            return
        
        try:
            # Create entry object
            entry = DataEntry(
                name=self.name_edit.text().strip(),
                email=self.email_edit.text().strip(),
                phone=self.phone_edit.text().strip(),
                company=self.company_edit.text().strip(),
                position=self.position_edit.text().strip(),
                notes=self.notes_edit.toPlainText().strip(),
                created_by=os.getlogin()  # Get current user
            )
            
            # Save to database
            entry_id = self.db_manager.create_entry(entry)
            
            if entry_id:
                QMessageBox.information(self, "Success", "Entry saved successfully!")
                self.clear_form()
                self.entry_saved.emit()
            else:
                QMessageBox.critical(self, "Error", "Failed to save entry!")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
    
    def clear_form(self):
        """Clear all form fields."""
        self.name_edit.clear()
        self.email_edit.clear()
        self.phone_edit.clear()
        self.company_edit.clear()
        self.position_edit.clear()
        self.notes_edit.clear()
        self.name_edit.setFocus()
