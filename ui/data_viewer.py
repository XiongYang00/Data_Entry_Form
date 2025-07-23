"""Modern spreadsheet-like data viewer with editing capabilities."""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
                             QTableWidgetItem, QHeaderView, QPushButton, QLabel,
                             QLineEdit, QMessageBox, QAbstractItemView, QFrame,
                             QToolBar, QComboBox, QSpacerItem, QSizePolicy)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QColor, QPalette, QAction, QIcon

from typing import List
from database.manager import DatabaseManager
from database.models import DataEntry
from config.settings import *


class ModernTableWidget(QTableWidget):
    """Modern styled table widget."""
    
    def __init__(self):
        super().__init__()
        self.setup_table()
        self.apply_style()
    
    def setup_table(self):
        """Set up table properties."""
        # Table behavior
        self.setAlternatingRowColors(True)
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setEditTriggers(QAbstractItemView.EditTrigger.DoubleClicked)
        self.setSortingEnabled(True)
        
        # Headers
        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.verticalHeader().hide()
        
        # Grid
        self.setShowGrid(True)
        self.setGridStyle(Qt.PenStyle.SolidLine)
    
    def apply_style(self):
        """Apply modern table styling."""
        self.setStyleSheet(f"""
            QTableWidget {{
                background-color: {BACKGROUND_COLOR if DARK_THEME else 'white'};
                alternate-background-color: {'#2d2d2d' if DARK_THEME else '#f8f9fa'};
                color: {TEXT_COLOR};
                border: 1px solid #404040;
                border-radius: 8px;
                gridline-color: #404040;
                font-size: 12px;
            }}
            QTableWidget::item {{
                padding: 8px;
                border: none;
            }}
            QTableWidget::item:selected {{
                background-color: {PRIMARY_COLOR};
                color: white;
            }}
            QTableWidget::item:hover {{
                background-color: rgba(33, 150, 243, 0.1);
            }}
            QHeaderView::section {{
                background-color: {'#404040' if DARK_THEME else '#e9ecef'};
                color: {TEXT_COLOR};
                padding: 12px 8px;
                border: 1px solid #606060;
                font-weight: bold;
                font-size: 12px;
            }}
            QHeaderView::section:hover {{
                background-color: {PRIMARY_COLOR};
                color: white;
            }}
        """)


class SearchBar(QLineEdit):
    """Modern search bar."""
    
    def __init__(self):
        super().__init__()
        self.setPlaceholderText("🔍 Search entries...")
        self.setMinimumHeight(40)
        self.setFont(QFont("Segoe UI", 11))
        self.apply_style()
    
    def apply_style(self):
        """Apply search bar styling."""
        self.setStyleSheet(f"""
            QLineEdit {{
                border: 2px solid #404040;
                border-radius: 20px;
                padding: 8px 16px;
                background-color: {BACKGROUND_COLOR if DARK_THEME else 'white'};
                color: {TEXT_COLOR};
                font-size: 14px;
            }}
            QLineEdit:focus {{
                border-color: {PRIMARY_COLOR};
                background-color: {'#2d2d2d' if DARK_THEME else '#f8f9fa'};
            }}
        """)


class DataViewer(QWidget):
    """Modern spreadsheet-like data viewer."""
    
    # Signals
    entry_updated = pyqtSignal()
    entry_deleted = pyqtSignal()
    
    def __init__(self, db_manager: DatabaseManager):
        super().__init__()
        self.db_manager = db_manager
        self.current_data: List[DataEntry] = []
        self.filtered_data: List[DataEntry] = []
        self._updating = False  # Flag to prevent recursion
        
        self.init_ui()
        self.apply_theme()
        self.refresh_data()
    
    def init_ui(self):
        """Initialize the viewer UI."""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(32, 32, 32, 32)
        main_layout.setSpacing(16)
        
        # Header
        header_layout = QHBoxLayout()
        
        title = QLabel("Data Viewer")
        title.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        # Record count
        self.count_label = QLabel("0 records")
        self.count_label.setFont(QFont("Segoe UI", 12))
        self.count_label.setStyleSheet(f"color: {'#b0b0b0' if DARK_THEME else '#666666'};")
        header_layout.addWidget(self.count_label)
        
        main_layout.addLayout(header_layout)
        
        # Toolbar
        toolbar_layout = QHBoxLayout()
        
        # Search bar
        self.search_bar = SearchBar()
        self.search_bar.textChanged.connect(self.filter_data)
        toolbar_layout.addWidget(self.search_bar)
        
        # Refresh button
        self.refresh_btn = QPushButton("🔄 Refresh")
        self.refresh_btn.setMinimumHeight(40)
        self.refresh_btn.setFont(QFont("Segoe UI", 10))
        self.refresh_btn.clicked.connect(self.refresh_data)
        self.refresh_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {PRIMARY_COLOR};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 16px;
            }}
            QPushButton:hover {{
                background-color: #1976D2;
            }}
        """)
        toolbar_layout.addWidget(self.refresh_btn)
        
        # Delete button
        self.delete_btn = QPushButton("🗑️ Delete")
        self.delete_btn.setMinimumHeight(40)
        self.delete_btn.setFont(QFont("Segoe UI", 10))
        self.delete_btn.clicked.connect(self.delete_selected)
        self.delete_btn.setEnabled(False)
        self.delete_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: #f44336;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 16px;
            }}
            QPushButton:hover {{
                background-color: #d32f2f;
            }}
            QPushButton:disabled {{
                background-color: #666666;
                color: #999999;
            }}
        """)
        toolbar_layout.addWidget(self.delete_btn)
        
        main_layout.addLayout(toolbar_layout)
        
        # Table
        self.table = ModernTableWidget()
        self.setup_table_headers()
        main_layout.addWidget(self.table)
        
        # Connect table signals
        self.table.cellChanged.connect(self.on_cell_changed)
        self.table.itemSelectionChanged.connect(self.on_selection_changed)
    
    def setup_table_headers(self):
        """Set up table headers."""
        headers = ["ID", "Name", "Email", "Phone", "Company", "Position", "Notes", "Created", "Updated", "Created By"]
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        
        # Set column widths
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)  # ID
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)  # Name
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.Stretch)  # Notes
        
        self.table.setColumnWidth(0, 60)   # ID
        self.table.setColumnWidth(1, 150)  # Name
        self.table.setColumnWidth(2, 200)  # Email
        self.table.setColumnWidth(3, 120)  # Phone
        self.table.setColumnWidth(4, 150)  # Company
        self.table.setColumnWidth(5, 120)  # Position
        self.table.setColumnWidth(7, 140)  # Created
        self.table.setColumnWidth(8, 140)  # Updated
        self.table.setColumnWidth(9, 100)  # Created By
    
    def apply_theme(self):
        """Apply viewer theme."""
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {BACKGROUND_COLOR};
                color: {TEXT_COLOR};
            }}
        """)
    
    def refresh_data(self):
        """Refresh data from database."""
        if self._updating:
            return  # Prevent refresh during update
            
        try:
            self.current_data = self.db_manager.get_all_entries()
            self.filtered_data = self.current_data.copy()
            self.populate_table()
            self.update_count_label()
        except Exception as e:
            print(f"Failed to refresh data: {str(e)}")
    
    def populate_table(self):
        """Populate table with current data."""
        # Block signals to prevent recursion during population
        self.table.blockSignals(True)
        
        self.table.setRowCount(len(self.filtered_data))
        
        for row, entry in enumerate(self.filtered_data):
            # Make ID column non-editable
            id_item = QTableWidgetItem(str(entry.id))
            id_item.setFlags(id_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            id_item.setBackground(QColor("#404040" if DARK_THEME else "#e9ecef"))
            self.table.setItem(row, 0, id_item)
            
            # Editable columns
            self.table.setItem(row, 1, QTableWidgetItem(entry.name))
            self.table.setItem(row, 2, QTableWidgetItem(entry.email))
            self.table.setItem(row, 3, QTableWidgetItem(entry.phone))
            self.table.setItem(row, 4, QTableWidgetItem(entry.company))
            self.table.setItem(row, 5, QTableWidgetItem(entry.position))
            self.table.setItem(row, 6, QTableWidgetItem(entry.notes))
            
            # Read-only timestamp columns
            created_item = QTableWidgetItem(entry.created_at.strftime("%Y-%m-%d %H:%M") if entry.created_at else "")
            created_item.setFlags(created_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            created_item.setBackground(QColor("#404040" if DARK_THEME else "#e9ecef"))
            self.table.setItem(row, 7, created_item)
            
            updated_item = QTableWidgetItem(entry.updated_at.strftime("%Y-%m-%d %H:%M") if entry.updated_at else "")
            updated_item.setFlags(updated_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            updated_item.setBackground(QColor("#404040" if DARK_THEME else "#e9ecef"))
            self.table.setItem(row, 8, updated_item)
            
            created_by_item = QTableWidgetItem(entry.created_by)
            created_by_item.setFlags(created_by_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            created_by_item.setBackground(QColor("#404040" if DARK_THEME else "#e9ecef"))
            self.table.setItem(row, 9, created_by_item)
        
        # Re-enable signals
        self.table.blockSignals(False)
    
    def filter_data(self, text: str):
        """Filter data based on search text."""
        if not text.strip():
            self.filtered_data = self.current_data.copy()
        else:
            text = text.lower()
            self.filtered_data = [
                entry for entry in self.current_data
                if (text in entry.name.lower() or
                    text in entry.email.lower() or
                    text in entry.phone.lower() or
                    text in entry.company.lower() or
                    text in entry.position.lower() or
                    text in entry.notes.lower())
            ]
        
        self.populate_table()
        self.update_count_label()
    
    def update_count_label(self):
        """Update the record count label."""
        total = len(self.current_data)
        filtered = len(self.filtered_data)
        
        if filtered == total:
            self.count_label.setText(f"{total} records")
        else:
            self.count_label.setText(f"{filtered} of {total} records")
    
    def on_cell_changed(self, row: int, column: int):
        """Handle cell changes."""
        # Prevent recursion
        if self._updating or column == 0:  # ID column shouldn't be editable
            return
        
        # Set flag to prevent recursion
        self._updating = True
        
        try:
            # Get the entry being edited
            entry = self.filtered_data[row]
            new_value = self.table.item(row, column).text()
            
            # Update the entry based on column
            if column == 1:
                entry.name = new_value
            elif column == 2:
                entry.email = new_value
            elif column == 3:
                entry.phone = new_value
            elif column == 4:
                entry.company = new_value
            elif column == 5:
                entry.position = new_value
            elif column == 6:
                entry.notes = new_value
            
            # Update in database
            if self.db_manager.update_entry(entry):
                self.entry_updated.emit()
                # Refresh immediately without timer to avoid handle issues
                self.refresh_data()
            else:
                # Show error using print instead of QMessageBox to avoid recursion
                print("Error: Failed to update entry!")
                self.refresh_data()  # Revert changes
                
        except Exception as e:
            # Print error instead of using QMessageBox
            print(f"Update failed: {str(e)}")
            self.refresh_data()
        finally:
            # Always reset the flag
            self._updating = False
    
    def on_selection_changed(self):
        """Handle selection changes."""
        has_selection = len(self.table.selectedItems()) > 0
        self.delete_btn.setEnabled(has_selection)
    
    def delete_selected(self):
        """Delete selected entries."""
        selected_rows = set()
        for item in self.table.selectedItems():
            selected_rows.add(item.row())
        
        if not selected_rows:
            return
        
        # Simple confirmation using print instead of QMessageBox to avoid recursion issues
        count = len(selected_rows)
        print(f"Deleting {count} record(s)...")
        
        try:
            # Delete entries
            deleted_count = 0
            for row in sorted(selected_rows, reverse=True):
                entry = self.filtered_data[row]
                if self.db_manager.delete_entry(entry.id):
                    deleted_count += 1
            
            if deleted_count > 0:
                self.entry_deleted.emit()
                self.refresh_data()
                print(f"Successfully deleted {deleted_count} record(s).")
            else:
                print("No records were deleted.")
                
        except Exception as e:
            print(f"Deletion failed: {str(e)}")
            self.refresh_data()
