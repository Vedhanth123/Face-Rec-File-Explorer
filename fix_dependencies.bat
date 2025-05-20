@echo off
REM filepath: c:\Code\Hobbies\Face Recognition File explorer\fix_dependencies.bat
echo Face Recognition Photo Organizer - Dependency Fix
echo =================================================
echo.

REM Check if virtual environment exists
if exist "FaceRec\Scripts\activate.bat" (
    echo Fixing dependencies in virtual environment...
    REM Run the PowerShell script with execution policy bypass and activate the venv
    powershell -ExecutionPolicy Bypass -Command "& {. '.\FaceRec\Scripts\Activate.ps1'; & '.\fix_dependency_versions.ps1'}"
) else (
    echo Virtual environment not found, creating one first...
    echo This may take some time, please be patient...
    REM Run the installation script first to create the virtual environment
    call install_windows.bat
    echo Now fixing dependencies...
    powershell -ExecutionPolicy Bypass -File "%~dp0fix_dependency_versions.ps1"
)

if %ERRORLEVEL% neq 0 (
    echo.
    echo Error: Could not fix dependencies. Please check the error messages above.
    pause
    exit /b 1
)
