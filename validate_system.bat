@echo off
REM filepath: c:\Code\Hobbies\Face Recognition File explorer\validate_system.bat
echo Face Recognition System Validation
echo ===============================
echo.

REM Activate virtual environment if it exists
if exist ".\FaceRec\Scripts\activate.bat" (
    call .\FaceRec\Scripts\activate.bat
    echo Virtual environment activated.
) else (
    echo Warning: Virtual environment not found. Using system Python.
    echo You may need to run install_windows.bat first.
    echo.
)

python validate_system.py

if %ERRORLEVEL% neq 0 (
    echo.
    echo Validation failed. Please check the errors above.
    echo Try running fix_dependencies.bat to resolve common issues.
)

echo.
pause
