@echo off
REM filepath: c:\Code\Hobbies\Face Recognition File explorer\run_explorer.bat
echo Face Recognition Explorer - Robust Launcher
echo =========================================
echo.

REM Set script paths
set "SCRIPT_DIR=%~dp0"
set "PS_SCRIPT=%SCRIPT_DIR%face_explorer.ps1"
set "VENV_PYTHON=%SCRIPT_DIR%FaceRec\Scripts\python.exe"

REM Ensure we're using the virtual environment's Python first
set PATH=%SCRIPT_DIR%FaceRec\Scripts;%PATH%

REM Check if Python is installed
where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.6+ from https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "%VENV_PYTHON%" (
    echo Virtual environment not found. Running install script first...
    call "%SCRIPT_DIR%install_windows.bat"
    if %ERRORLEVEL% NEQ 0 (
        echo Failed to create virtual environment. See errors above.
        pause
        exit /b 1
    )
)

REM Run the PowerShell script with all arguments
powershell -ExecutionPolicy Bypass -File "%PS_SCRIPT%" %*

REM Check for errors
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo An error occurred while running the application.
    echo If you're seeing import errors, try running fix_dependencies.bat
    echo.
    pause
)

echo.
pause
