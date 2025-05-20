@echo off
echo Face Recognition File Explorer - Setup
echo ====================================
echo.

rem Check if running as administrator
net session >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Warning: This script is not running as administrator.
    echo Some operations may fail if administrator privileges are required.
    echo.
    echo Press any key to continue anyway...
    pause >nul
)

rem Check if PowerShell is available
where powershell >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Error: PowerShell is not available on this system.
    echo This script requires PowerShell to run the setup process.
    echo.
    echo Please install PowerShell and try again.
    pause
    exit /b 1
)

echo Running setup script with PowerShell...
echo.

rem Run the setup.ps1 script with execution policy bypass
powershell -ExecutionPolicy Bypass -File "%~dp0setup.ps1"

if %ERRORLEVEL% neq 0 (
    echo.
    echo Setup failed. Please check the error messages above.
    pause
    exit /b 1
)

echo.
echo Setup completed successfully!
echo.
