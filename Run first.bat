@echo off
echo Checking Python installation...

:: Check if python command exists
where python >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH.
    echo Please install Python 3.10+ from https://www.python.org/downloads/windows/ and make sure to add it to PATH.
    pause
    exit /b 1
)

:: Show Python version
python --version

echo Installing required Python packages...
pip install --upgrade pip
pip install pyautogui customtkinter

:: Optional: check if tkinter is installed (try importing)
python -c "import tkinter" 2>nul
if errorlevel 1 (
    echo tkinter is not installed. Installing tkinter package...
    pip install tk
) else (
    echo tkinter is already installed.
)

echo.
echo Installation completed!
echo You can now run your script.
pause
