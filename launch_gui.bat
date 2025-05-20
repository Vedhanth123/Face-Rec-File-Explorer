@echo off
echo Face Recognition Photo Organizer
echo ==============================

REM Check if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.6+ from https://www.python.org/downloads/
    echo Or run setup.bat first to configure the environment
    pause
    exit /b 1
)

REM Check if virtual environment exists and use it if available
if exist "FaceRec\Scripts\activate.bat" (
    echo Using virtual environment...
    call "FaceRec\Scripts\activate.bat"
) else (
    echo Virtual environment not found. Will use system Python.
    echo Consider running install_windows.bat first for best results.
)

REM Verify that we can import the necessary packages after activation
python -c "import face_recognition, cv2" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Installing required packages...
    python -m pip install -r requirements.txt
    if %ERRORLEVEL% NEQ 0 (
        echo Failed to install required packages.
        echo Please run install_windows.bat to properly configure the environment.
        pause
        exit /b 1
    )
)

REM Check for tkinter which is required for GUI
python -c "import tkinter" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Warning: tkinter is not installed, which is required for the GUI.
    echo Please reinstall Python and make sure to check "tcl/tk and IDLE" during installation.
    pause
)

REM Launch the GUI application
echo Starting Face Recognition Photo Organizer...
call run_with_venv.bat face_recognizer_app.py

REM Check if application exited with an error
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Application exited with error code %ERRORLEVEL%
    echo If you're having trouble, try running setup.bat to fix dependencies.
    pause
)
