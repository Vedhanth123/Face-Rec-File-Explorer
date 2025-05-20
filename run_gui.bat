@echo off
REM filepath: c:\Code\Hobbies\Face Recognition File explorer\run_gui.bat
echo Face Recognition Photo Organizer
echo ===============================
echo.

REM Run the PowerShell script with execution policy bypass
powershell -ExecutionPolicy Bypass -File "%~dp0run_gui.ps1"

if %ERRORLEVEL% neq 0 (
    echo.
    echo Error: Could not run GUI application. Check the error messages above.
    pause
    exit /b 1
)
