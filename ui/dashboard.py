"""Dashboard widget with KPIs and visualizations."""

import sys
import os

# Set Qt API environment before importing any Qt modules
os.environ['QT_API'] = 'pyqt6'

import matplotlib
matplotlib.use('qtagg')  # Use Qt6Agg backend for PyQt6

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from datetime import datetime, timedelta
from typing import List, Dict, Any

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QLabel, QFrame, QScrollArea, QPushButton, QComboBox,
                             QGroupBox, QSizePolicy)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QFont, QPalette, QColor

from database.manager import DatabaseManager
from database.models import DataEntry
from config.settings import *


class KPICard(QFrame):
    """Modern KPI card widget."""
    
    def __init__(self, title: str, value: str, subtitle: str = "", color: str = PRIMARY_COLOR):
        super().__init__()
        self.setup_ui(title, value, subtitle, color)
    
    def setup_ui(self, title: str, value: str, subtitle: str, color: str):
        """Set up the KPI card UI."""
        self.setFrameStyle(QFrame.Shape.StyledPanel)
        self.setMinimumHeight(120)
        self.setMaximumHeight(150)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(4)
        
        # Title
        title_label = QLabel(title)
        title_label.setFont(QFont("Segoe UI", 10))
        title_label.setStyleSheet(f"color: {'#b0b0b0' if DARK_THEME else '#666666'};")
        layout.addWidget(title_label)
        
        # Value
        self.value_label = QLabel(value)
        self.value_label.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        self.value_label.setStyleSheet(f"color: {color};")
        layout.addWidget(self.value_label)
        
        # Subtitle
        if subtitle:
            subtitle_label = QLabel(subtitle)
            subtitle_label.setFont(QFont("Segoe UI", 9))
            subtitle_label.setStyleSheet(f"color: {'#888888' if DARK_THEME else '#999999'};")
            layout.addWidget(subtitle_label)
        
        layout.addStretch()
        
        # Styling
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {'#2d2d2d' if DARK_THEME else '#ffffff'};
                border: 1px solid {'#404040' if DARK_THEME else '#e0e0e0'};
                border-radius: 12px;
                border-left: 4px solid {color};
            }}
            QFrame:hover {{
                border-color: {color};
                background-color: {'#353535' if DARK_THEME else '#f8f9fa'};
            }}
        """)
    
    def update_value(self, value: str, subtitle: str = ""):
        """Update the KPI value."""
        self.value_label.setText(value)


class ChartWidget(QFrame):
    """Widget for displaying matplotlib charts."""
    
    def __init__(self, title: str = ""):
        super().__init__()
        self.title = title
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the chart widget UI."""
        self.setFrameStyle(QFrame.Shape.StyledPanel)
        self.setMinimumHeight(300)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        
        # Title
        if self.title:
            title_label = QLabel(self.title)
            title_label.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
            title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(title_label)
        
        # Create matplotlib figure
        self.figure = Figure(figsize=(8, 6), facecolor='none')
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        
        # Styling
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {'#2d2d2d' if DARK_THEME else '#ffffff'};
                border: 1px solid {'#404040' if DARK_THEME else '#e0e0e0'};
                border-radius: 12px;
            }}
        """)
    
    def clear_chart(self):
        """Clear the current chart."""
        self.figure.clear()
        self.canvas.draw()


class Dashboard(QWidget):
    """Main dashboard widget with KPIs and visualizations."""
    
    # Signals
    refresh_requested = pyqtSignal()
    
    def __init__(self, db_manager: DatabaseManager):
        super().__init__()
        self.db_manager = db_manager
        self.data: List[DataEntry] = []
        
        # Set up matplotlib theme
        self.setup_matplotlib_theme()
        
        self.init_ui()
        self.refresh_data()
        
        # Auto-refresh timer
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.refresh_data)
        self.refresh_timer.start(60000)  # Refresh every minute
    
    def setup_matplotlib_theme(self):
        """Configure matplotlib for dark/light theme."""
        if DARK_THEME:
            plt.style.use('dark_background')
            sns.set_palette("bright")
        else:
            plt.style.use('default')
            sns.set_palette("deep")
    
    def init_ui(self):
        """Initialize the dashboard UI."""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(20)
        
        # Header
        header_layout = QHBoxLayout()
        
        title = QLabel("📊 Dashboard")
        title.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        # Refresh button
        self.refresh_btn = QPushButton("🔄 Refresh")
        self.refresh_btn.setMinimumHeight(40)
        self.refresh_btn.clicked.connect(self.refresh_data)
        self.refresh_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {PRIMARY_COLOR};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 16px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #1976D2;
            }}
        """)
        header_layout.addWidget(self.refresh_btn)
        
        # Time period selector
        self.period_combo = QComboBox()
        self.period_combo.addItems(["Last 7 Days", "Last 30 Days", "Last 90 Days", "All Time"])
        self.period_combo.setCurrentText("Last 30 Days")
        self.period_combo.currentTextChanged.connect(self.refresh_data)
        self.period_combo.setStyleSheet(f"""
            QComboBox {{
                background-color: {'#2d2d2d' if DARK_THEME else '#ffffff'};
                border: 1px solid {'#404040' if DARK_THEME else '#e0e0e0'};
                border-radius: 6px;
                padding: 8px;
                min-width: 120px;
            }}
        """)
        header_layout.addWidget(self.period_combo)
        
        main_layout.addLayout(header_layout)
        
        # Scroll area for dashboard content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        main_layout.addWidget(scroll)
        
        # Dashboard content widget
        content_widget = QWidget()
        scroll.setWidget(content_widget)
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(20)
        
        # KPI Cards Section
        self.create_kpi_section(content_layout)
        
        # Charts Section
        self.create_charts_section(content_layout)
        
        # Apply theme
        self.apply_theme()
    
    def create_kpi_section(self, parent_layout: QVBoxLayout):
        """Create KPI cards section."""
        kpi_group = QGroupBox("Key Performance Indicators")
        kpi_group.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        parent_layout.addWidget(kpi_group)
        
        kpi_layout = QGridLayout(kpi_group)
        kpi_layout.setSpacing(16)
        
        # Create KPI cards
        self.total_entries_card = KPICard("Total Entries", "0", "All time", PRIMARY_COLOR)
        self.recent_entries_card = KPICard("Recent Entries", "0", "Last 7 days", "#4CAF50")
        self.avg_daily_card = KPICard("Daily Average", "0", "Entries per day", "#FF9800")
        self.top_company_card = KPICard("Top Company", "N/A", "Most entries", "#9C27B0")
        
        kpi_layout.addWidget(self.total_entries_card, 0, 0)
        kpi_layout.addWidget(self.recent_entries_card, 0, 1)
        kpi_layout.addWidget(self.avg_daily_card, 0, 2)
        kpi_layout.addWidget(self.top_company_card, 0, 3)
        
        # Apply group styling
        self.apply_group_styling(kpi_group)
    
    def create_charts_section(self, parent_layout: QVBoxLayout):
        """Create charts section."""
        charts_group = QGroupBox("Data Visualizations")
        charts_group.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        parent_layout.addWidget(charts_group)
        
        charts_layout = QGridLayout(charts_group)
        charts_layout.setSpacing(16)
        
        # Create chart widgets
        self.entries_timeline_chart = ChartWidget("Entries Over Time")
        self.company_distribution_chart = ChartWidget("Companies Distribution")
        self.position_analysis_chart = ChartWidget("Position Analysis")
        self.activity_heatmap_chart = ChartWidget("Activity Heatmap")
        
        charts_layout.addWidget(self.entries_timeline_chart, 0, 0, 1, 2)
        charts_layout.addWidget(self.company_distribution_chart, 1, 0)
        charts_layout.addWidget(self.position_analysis_chart, 1, 1)
        charts_layout.addWidget(self.activity_heatmap_chart, 2, 0, 1, 2)
        
        # Apply group styling
        self.apply_group_styling(charts_group)
    
    def apply_group_styling(self, group_box: QGroupBox):
        """Apply styling to group boxes."""
        group_box.setStyleSheet(f"""
            QGroupBox {{
                font-weight: bold;
                border: 2px solid #404040;
                border-radius: 12px;
                margin-top: 16px;
                padding-top: 16px;
                color: {TEXT_COLOR};
                background-color: {'#1a1a1a' if DARK_THEME else '#f8f9fa'};
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 12px;
                background-color: {BACKGROUND_COLOR};
                color: {PRIMARY_COLOR};
            }}
        """)
    
    def apply_theme(self):
        """Apply dashboard theme."""
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
    
    def refresh_data(self):
        """Refresh dashboard data and charts."""
        try:
            # Get fresh data
            self.data = self.db_manager.get_all_entries()
            
            # Filter data based on selected period
            filtered_data = self.filter_data_by_period()
            
            # Update KPIs
            self.update_kpis(filtered_data)
            
            # Update charts
            self.update_charts(filtered_data)
            
            self.refresh_requested.emit()
            
        except Exception as e:
            print(f"Error refreshing dashboard: {e}")
    
    def filter_data_by_period(self) -> List[DataEntry]:
        """Filter data based on selected time period."""
        period = self.period_combo.currentText()
        now = datetime.now()
        
        if period == "All Time":
            return self.data
        
        # Calculate cutoff date
        if period == "Last 7 Days":
            cutoff = now - timedelta(days=7)
        elif period == "Last 30 Days":
            cutoff = now - timedelta(days=30)
        elif period == "Last 90 Days":
            cutoff = now - timedelta(days=90)
        else:
            return self.data
        
        # Filter entries
        filtered = [
            entry for entry in self.data
            if entry.created_at and entry.created_at >= cutoff
        ]
        
        return filtered
    
    def update_kpis(self, data: List[DataEntry]):
        """Update KPI cards with current data."""
        total_entries = len(self.data)
        recent_entries = len([
            entry for entry in self.data
            if entry.created_at and entry.created_at >= datetime.now() - timedelta(days=7)
        ])
        
        # Calculate daily average
        if self.data:
            oldest_entry = min(entry.created_at for entry in self.data if entry.created_at)
            days_diff = max(1, (datetime.now() - oldest_entry).days)
            daily_avg = total_entries / days_diff
        else:
            daily_avg = 0
        
        # Find top company
        companies = [entry.company for entry in self.data if entry.company.strip()]
        if companies:
            company_counts = pd.Series(companies).value_counts()
            top_company = company_counts.index[0] if len(company_counts) > 0 else "N/A"
        else:
            top_company = "N/A"
        
        # Update cards
        self.total_entries_card.update_value(str(total_entries))
        self.recent_entries_card.update_value(str(recent_entries))
        self.avg_daily_card.update_value(f"{daily_avg:.1f}")
        self.top_company_card.update_value(top_company[:15] + "..." if len(top_company) > 15 else top_company)
    
    def update_charts(self, data: List[DataEntry]):
        """Update all charts with current data."""
        if not data:
            self.clear_all_charts()
            return
        
        try:
            # Convert to DataFrame for easier analysis
            df = self.entries_to_dataframe(data)
            
            # Update each chart
            self.update_timeline_chart(df)
            self.update_company_distribution_chart(df)
            self.update_position_analysis_chart(df)
            self.update_activity_heatmap(df)
            
        except Exception as e:
            print(f"Error updating charts: {e}")
    
    def entries_to_dataframe(self, data: List[DataEntry]) -> pd.DataFrame:
        """Convert entries to pandas DataFrame."""
        records = []
        for entry in data:
            if entry.created_at:
                records.append({
                    'id': entry.id,
                    'name': entry.name,
                    'email': entry.email,
                    'company': entry.company,
                    'position': entry.position,
                    'created_at': entry.created_at,
                    'created_by': entry.created_by,
                    'date': entry.created_at.date(),
                    'hour': entry.created_at.hour,
                    'day_of_week': entry.created_at.strftime('%A'),
                    'month': entry.created_at.strftime('%B %Y')
                })
        
        return pd.DataFrame(records)
    
    def update_timeline_chart(self, df: pd.DataFrame):
        """Update entries timeline chart."""
        self.entries_timeline_chart.clear_chart()
        
        if df.empty:
            return
        
        ax = self.entries_timeline_chart.figure.add_subplot(111)
        
        # Group by date and count entries
        daily_counts = df.groupby('date').size().reset_index(name='count')
        daily_counts['date'] = pd.to_datetime(daily_counts['date'])
        
        # Create line plot
        ax.plot(daily_counts['date'], daily_counts['count'], 
                marker='o', linewidth=2, markersize=4, color=PRIMARY_COLOR)
        ax.fill_between(daily_counts['date'], daily_counts['count'], 
                       alpha=0.3, color=PRIMARY_COLOR)
        
        ax.set_title('Daily Entry Count', fontsize=14, fontweight='bold')
        ax.set_xlabel('Date')
        ax.set_ylabel('Number of Entries')
        ax.grid(True, alpha=0.3)
        
        # Format dates on x-axis
        self.entries_timeline_chart.figure.autofmt_xdate()
        
        self.entries_timeline_chart.canvas.draw()
    
    def update_company_distribution_chart(self, df: pd.DataFrame):
        """Update company distribution pie chart."""
        self.company_distribution_chart.clear_chart()
        
        if df.empty:
            return
        
        ax = self.company_distribution_chart.figure.add_subplot(111)
        
        # Get top 8 companies
        companies = df[df['company'].str.strip() != '']['company'].value_counts().head(8)
        
        if not companies.empty:
            # Create pie chart
            colors = sns.color_palette("husl", len(companies))
            wedges, texts, autotexts = ax.pie(companies.values, labels=companies.index, 
                                             autopct='%1.1f%%', colors=colors,
                                             startangle=90)
            
            # Improve text readability
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
        
        ax.set_title('Top Companies', fontsize=14, fontweight='bold')
        
        self.company_distribution_chart.canvas.draw()
    
    def update_position_analysis_chart(self, df: pd.DataFrame):
        """Update position analysis bar chart."""
        self.position_analysis_chart.clear_chart()
        
        if df.empty:
            return
        
        ax = self.position_analysis_chart.figure.add_subplot(111)
        
        # Get top positions
        positions = df[df['position'].str.strip() != '']['position'].value_counts().head(10)
        
        if not positions.empty:
            # Create horizontal bar chart
            bars = ax.barh(positions.index, positions.values, color=PRIMARY_COLOR, alpha=0.7)
            
            # Add value labels on bars
            for i, bar in enumerate(bars):
                width = bar.get_width()
                ax.text(width + 0.1, bar.get_y() + bar.get_height()/2, 
                       f'{int(width)}', ha='left', va='center', fontweight='bold')
        
        ax.set_title('Most Common Positions', fontsize=14, fontweight='bold')
        ax.set_xlabel('Number of Entries')
        
        self.position_analysis_chart.canvas.draw()
    
    def update_activity_heatmap(self, df: pd.DataFrame):
        """Update activity heatmap."""
        self.activity_heatmap_chart.clear_chart()
        
        if df.empty:
            return
        
        ax = self.activity_heatmap_chart.figure.add_subplot(111)
        
        # Create hour vs day of week heatmap
        df['day_num'] = df['created_at'].dt.dayofweek
        heatmap_data = df.groupby(['day_num', 'hour']).size().unstack(fill_value=0)
        
        if not heatmap_data.empty:
            # Create heatmap
            sns.heatmap(heatmap_data, annot=True, fmt='d', cmap='Blues',
                       xticklabels=[f'{h}:00' for h in range(24)],
                       yticklabels=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                       ax=ax, cbar_kws={'label': 'Number of Entries'})
        
        ax.set_title('Activity Heatmap (Hour vs Day)', fontsize=14, fontweight='bold')
        ax.set_xlabel('Hour of Day')
        ax.set_ylabel('Day of Week')
        
        self.activity_heatmap_chart.canvas.draw()
    
    def clear_all_charts(self):
        """Clear all charts when no data is available."""
        for chart in [self.entries_timeline_chart, self.company_distribution_chart,
                     self.position_analysis_chart, self.activity_heatmap_chart]:
            chart.clear_chart()
            ax = chart.figure.add_subplot(111)
            ax.text(0.5, 0.5, 'No Data Available', 
                   horizontalalignment='center', verticalalignment='center',
                   transform=ax.transAxes, fontsize=16, alpha=0.6)
            chart.canvas.draw()
