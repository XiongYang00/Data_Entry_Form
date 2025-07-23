# Development Setup Guide

## Prerequisites
- Python 3.8 or higher
- Git

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/XiongYang00/Data_Entry_Form.git
cd Data_Entry_Form
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv .venv
.\.venv\Scripts\activate

# macOS/Linux
python -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
# Option 1: Use the launcher
run_app.bat  # Windows
./run_app.ps1  # PowerShell

# Option 2: Direct execution
python main_lite.py  # Recommended
python main.py       # Full version
python main_debug.py # Debug version
```

## Development Workflow

### Virtual Environment
The virtual environment (`.venv` folder) is automatically excluded from git commits via `.gitignore`. This ensures:
- Clean repository without large dependency files
- Each developer can have their own Python environment
- No conflicts between different Python versions

### Git Best Practices
1. **Always exclude virtual environments**: The `.gitignore` file handles this
2. **Include requirements.txt**: Allows others to recreate the environment
3. **Use meaningful commit messages**: Describe what features were added/changed
4. **Test before committing**: Run the application to ensure it works

### Project Structure
```
Data_Entry_Form/
├── .venv/              # Virtual environment (git ignored)
├── .github/            # GitHub specific files
├── config/             # Configuration modules
├── database/           # Database layer
├── ui/                 # User interface components
├── utils/              # Utility functions
├── main.py             # Full version entry point
├── main_lite.py        # Lite version (recommended)
├── main_debug.py       # Debug version
├── requirements.txt    # Python dependencies
├── README.md           # Project documentation
└── .gitignore         # Git ignore rules
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes
4. Test the application
5. Commit your changes: `git commit -m "Add your feature"`
6. Push to your branch: `git push origin feature/your-feature`
7. Create a Pull Request

## Troubleshooting

### Virtual Environment Issues
- Ensure you're in the correct directory
- Activate the virtual environment before installing packages
- Use `python -m pip list` to verify installed packages

### Application Issues
- Use `main_debug.py` for detailed error messages
- Check that all dependencies are installed
- Verify Python version compatibility

### Git Issues
- Ensure `.gitignore` is in the root directory
- Use `git status` to check what files will be committed
- Virtual environment should not appear in git status
