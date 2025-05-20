@echo off
REM filepath: c:\Code\Hobbies\Face Recognition File explorer\run_with_venv.bat
REM This is a helper script to ensure Python commands run with the virtual environment

echo Running with virtual environment: %*
echo.

REM Check if virtual environment exists
if not exist "FaceRec\Scripts\activate.bat" (
    echo Error: Virtual environment not found.
    echo Please run install_windows.bat first to create the virtual environment.
    pause
    exit /b 1
)

REM Activate virtual environment and run the command
call "FaceRec\Scripts\activate.bat"
python %*

REM If there was an error
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Error occurred. If you're seeing import errors, try:
    echo   - run fix_dependencies.bat to fix dependency issues
    echo   - run validate_system.bat to check if all components work
    echo.
    pause
)

REM Deactivate at the end
call "FaceRec\Scripts\deactivate.bat"
