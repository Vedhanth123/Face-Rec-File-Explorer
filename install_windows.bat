@echo off
echo Face Recognition Photo Organizer - Windows Installation
echo =============================================
echo.
echo This script will install dlib and face_recognition without requiring Visual C++ build tools.
echo.

rem Check if PowerShell is available
where powershell >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Error: PowerShell is not available on this system.
    echo This script requires PowerShell to run the installation process.
    echo.
    echo Please install PowerShell and try again.
    pause
    exit /b 1
)

echo Running installation script with PowerShell...
echo.

rem Run the PowerShell script with execution policy bypass
powershell -ExecutionPolicy Bypass -File "%~dp0install_windows.ps1"

if %ERRORLEVEL% neq 0 (
    echo.
    echo Installation failed. Please check the error messages above.
    pause
    exit /b 1
)

echo.
echo Installation completed successfully!
echo.
echo You can now run the application with:
echo   launch_gui.bat
echo.
pause
