# Database Configuration
DATABASE_PATH = "shared_database.db"
SHARED_FOLDER_PATH = r"\\server\shared\database"  # Update this to your actual shared folder

# Application Settings
APP_NAME = "Data Entry Pro"
APP_VERSION = "1.0.0"
WINDOW_TITLE = "Data Entry Pro - Modern Database Application"

# UI Settings
SIDEBAR_WIDTH = 250
SIDEBAR_COLLAPSED_WIDTH = 60
ANIMATION_DURATION = 300

# Database Settings
AUTO_REFRESH_INTERVAL = 10000  # milliseconds (10 seconds)
MAX_RECORDS_DISPLAY = 1000

# Theme Settings
DARK_THEME = True
PRIMARY_COLOR = "#2196F3"
ACCENT_COLOR = "#FFC107"
BACKGROUND_COLOR = "#1e1e1e" if DARK_THEME else "#ffffff"
TEXT_COLOR = "#ffffff" if DARK_THEME else "#000000"
