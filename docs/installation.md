# Installation Guide

## Prerequisites
1. Windows 11 operating system
2. Python 3.13.3 or higher
3. Administrator privileges
4. Git (optional, for cloning the repository)

## Installation Steps

### 1. Clone or Download the Repository
```bash
git clone <repository-url>
# or download and extract the ZIP file
```

### 2. Install Python Dependencies
Open a command prompt in the project directory and run:
```bash
pip install -r requirements.txt
```

### 3. Verify Installation
To verify that all dependencies are installed correctly, run:
```bash
python -c "import cv2, pyautogui, pynput, mss, psutil, win32gui, pygame, keyboard, customtkinter"
```

## Running the Application

### Method 1: Using the Batch File
1. Right-click on `run_admin.bat`
2. Select "Run as administrator"

### Method 2: Using Command Prompt
1. Open Command Prompt as administrator
2. Navigate to the project directory:
```bash
cd path\to\project
```
3. Run the application:
```bash
python gui.py
```

## Troubleshooting

### Common Issues

1. **Permission Denied**
   - Ensure you're running the application as administrator
   - Check if your antivirus is blocking the application

2. **Missing Dependencies**
   - Run `pip install -r requirements.txt` again
   - Check Python version: `python --version`

3. **GUI Not Starting**
   - Verify all dependencies are installed
   - Check if you have the required Windows permissions

### Getting Help
If you encounter any issues not covered here, please:
1. Check the [User Guide](user-guide.md)
2. Review the [Development Guide](development.md)
3. Contact the project maintainers 