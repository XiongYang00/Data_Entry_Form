<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# GitHub Copilot Instructions for Data Entry Pro

## Project Overview
This is a modern desktop data entry application built with PyQt6. The application features:
- Real-time database synchronization using SQLite
- Modern toggle sidebar navigation
- Professional data entry forms with validation
- Spreadsheet-like data viewer with in-cell editing
- Dark theme with modern styling

## Code Style & Standards
- Use type hints for all function parameters and return values
- Follow PEP 8 naming conventions
- Use docstrings for all classes and methods
- Prefer composition over inheritance
- Use PyQt6 signals for component communication

## Architecture Patterns
- **MVC Pattern**: Separate UI, business logic, and data layers
- **Signal-Slot Pattern**: Use PyQt6 signals for loose coupling
- **Observer Pattern**: Database sync notifications
- **Strategy Pattern**: Theme and styling application

## PyQt6 Specific Guidelines
- Use modern PyQt6 imports (not PyQt5 compatibility)
- Prefer QWidget compositions over complex inheritance
- Use QPropertyAnimation for smooth UI transitions
- Apply consistent styling through stylesheets
- Handle signals/slots properly to avoid memory leaks

## Database Guidelines
- Use context managers for database connections
- Implement proper error handling for database operations
- Use parameterized queries to prevent SQL injection
- Handle concurrent access gracefully

## UI/UX Guidelines
- Maintain consistent spacing and margins (16px, 24px, 32px)
- Use the defined color scheme in config/settings.py
- Implement proper validation with user-friendly error messages
- Ensure accessibility with proper focus management
- Use modern styling with rounded corners and gradients

## Common Patterns
```python
# Signal definition
signal_name = pyqtSignal(type)

# Database operation with error handling
try:
    with self.db_manager.get_connection() as conn:
        # database operations
except Exception as e:
    # proper error handling

# Modern PyQt6 styling
widget.setStyleSheet(f"""
    QWidget {{
        background-color: {BACKGROUND_COLOR};
        border-radius: 8px;
    }}
""")
```

## Testing Considerations
- Test database operations with edge cases
- Verify UI responsiveness across different screen sizes
- Test real-time sync functionality
- Validate form inputs thoroughly

## Performance Guidelines
- Lazy load data for large datasets
- Use QTimer for periodic updates
- Implement proper cleanup in closeEvent
- Optimize database queries with appropriate indexes
