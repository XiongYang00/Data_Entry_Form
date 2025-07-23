# Data Entry Pro - Modern Desktop Application

A professional desktop data entry application built with PyQt6, featuring real-time database synchronization and a modern, sleek interface.

## Features

- **Modern Toggle Sidebar**: Collapsible navigation with smooth animations
- **Data Entry Form**: Professional form with validation and grouped fields
- **Spreadsheet View**: Excel-like data viewer with in-cell editing
- **Real-time Sync**: Automatic updates when database changes
- **Shared Database**: SQLite database on shared network folder
- **Professional UI**: Dark theme with modern styling
- **Search & Filter**: Quick search across all data fields
- **Data Validation**: Input validation with user-friendly error messages

## Requirements

- Python 3.8+
- PyQt6
- SQLite3 (included with Python)
- Watchdog (for file monitoring)

## Installation

1. Clone or download this project
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure database path in `config/settings.py`:
   ```python
   SHARED_FOLDER_PATH = r"\\server\shared\database"  # Your shared folder path
   ```

## Usage

Run the application:

### Option 1: Using the Launcher (Recommended)
```bash
# Windows Batch File
run_app.bat

# PowerShell Script  
.\run_app.ps1
```

### Option 2: Direct Python Execution
```bash
# Lite Version (Recommended for Windows - No timer issues)
python main_lite.py

# Full Version (With real-time sync)
python main.py

# Debug Version (For troubleshooting)
python main_debug.py
```

### Version Differences

#### Lite Version (`main_lite.py`) - **Recommended**
- ✅ All core features working
- ✅ No Windows handle exhaustion issues
- ✅ Manual refresh button for data updates
- ❌ No automatic real-time sync

#### Full Version (`main.py`)
- ✅ All features including real-time sync
- ⚠️ May have timer handle issues on Windows
- ✅ Automatic database change detection

#### Debug Version (`main_debug.py`)
- ✅ Extensive logging for troubleshooting
- ✅ Exception handling and stack traces
- ✅ Based on lite version for stability

### Features Overview

#### Toggle Sidebar
- Click the arrow button to collapse/expand the sidebar
- Switch between Data Entry and Data Viewer modes
- Modern animations and styling

#### Data Entry Form
- Enter new records with validation
- Grouped fields for better organization
- Auto-save with user feedback
- Clear form functionality

#### Data Viewer
- Spreadsheet-like interface
- Double-click cells to edit
- Search and filter functionality
- Sort by clicking column headers
- Delete selected records
- Real-time refresh when database changes

#### Real-time Synchronization
- Automatic detection of database changes
- Refresh data when other users make changes
- File system monitoring with polling fallback

## Project Structure

```
data_entry_app/
├── main.py                 # Application entry point
├── requirements.txt        # Dependencies
├── config/                 # Configuration modules
│   ├── settings.py        # App settings
│   └── database.py        # Database configuration
├── database/              # Database layer
│   ├── models.py          # Data models
│   ├── manager.py         # Database operations
│   └── sync.py            # Real-time sync
├── ui/                    # User interface
│   ├── main_window.py     # Main window
│   ├── sidebar.py         # Navigation sidebar
│   ├── entry_form.py      # Data entry form
│   └── data_viewer.py     # Data viewer/editor
└── utils/                 # Utilities
    ├── validators.py      # Input validation
    └── file_watcher.py    # File monitoring
```

## Configuration

### Database Settings
Edit `config/settings.py` to configure:
- Database file path
- Shared folder location
- Refresh intervals
- UI themes and colors

### Themes
The application supports dark and light themes. Toggle in `config/settings.py`:
```python
DARK_THEME = True  # Set to False for light theme
```

## Database Schema

The application uses SQLite with the following main table:

```sql
CREATE TABLE data_entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT,
    phone TEXT,
    company TEXT,
    position TEXT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by TEXT DEFAULT 'Unknown'
);
```

## Troubleshooting

### Database Access Issues
- Ensure the shared folder path is accessible
- Check network permissions
- Verify SQLite file permissions

### Real-time Sync Not Working
- Check if the database file exists
- Verify file system permissions
- Ensure network connectivity to shared folder

### UI Issues
- Update graphics drivers
- Try switching themes in settings
- Check PyQt6 installation

## License

This project is open source and available under the MIT License.
