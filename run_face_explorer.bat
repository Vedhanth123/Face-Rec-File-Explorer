@echo off
echo Face Recognition File Explorer
echo ============================

REM Check if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.6+ from https://www.python.org/downloads/
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

REM Check if required packages are installed
python -c "import face_recognition, cv2" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Installing required packages...
    echo Please wait, this may take a while...
    
    REM Try to install with requirements file first
    if exist "requirements.txt" (
        python -m pip install -r requirements.txt
    ) else (
        python -m pip install face_recognition opencv-python==4.5.5.64 numpy==1.23.5 pillow
    )
    
    REM Check if packages installed correctly
    python -c "import face_recognition, cv2" >nul 2>&1
    if %ERRORLEVEL% NEQ 0 (
        echo Failed to install required packages.
        echo Please run install_windows.bat to properly configure the environment.
        echo Or run fix_dependencies.bat to fix common issues.
        pause
        exit /b 1
    )
)

REM Default photos directory
set PHOTOS_DIR=%~dp0photos
if not exist "%PHOTOS_DIR%" mkdir "%PHOTOS_DIR%"

:menu
cls
echo Face Recognition File Explorer
echo ============================
echo.
echo Current photos directory: %PHOTOS_DIR%
echo.
echo 1. Set photos directory
echo 2. Scan photos for faces
echo 3. Show unlabeled face
echo 4. Label face
echo 5. Interactive labeling (name multiple faces at once)
echo 6. Recognize faces in all photos
echo 7. Group photos by person
echo 8. Create Windows search files
echo 9. Visualize recognized faces
echo 10. Export face data to JSON
echo 11. Exit
echo.

set /p choice="Enter your choice (1-11): "

if "%choice%"=="1" goto set_dir
if "%choice%"=="2" goto scan
if "%choice%"=="3" goto show
if "%choice%"=="4" goto label
if "%choice%"=="5" goto interactive
if "%choice%"=="6" goto recognize
if "%choice%"=="7" goto group
if "%choice%"=="8" goto create_search
if "%choice%"=="9" goto visualize
if "%choice%"=="10" goto export
if "%choice%"=="11" goto end

echo Invalid choice. Please try again.
pause
goto menu

:set_dir
echo.
echo Current photos directory: %PHOTOS_DIR%
echo.
set /p new_dir="Enter new photos directory path (or press Enter to keep current): "
if not "%new_dir%"=="" set PHOTOS_DIR=%new_dir%
goto menu

:scan
echo.
set /p force="Force rescan of already processed photos? (y/n): "
set /p parallel="Use parallel processing (faster but uses more memory)? (y/n): "
set /p model="Face detection model (hog=faster, cnn=more accurate): "

if /i "%force%"=="y" (
    if /i "%parallel%"=="y" (
        call run_with_venv.bat face_recognition_explorer.py --photos_dir "%PHOTOS_DIR%" --scan --force_rescan --parallel --model %model%
    ) else (
        call run_with_venv.bat face_recognition_explorer.py --photos_dir "%PHOTOS_DIR%" --scan --force_rescan --model %model%
    )
) else (
    if /i "%parallel%"=="y" (
        call run_with_venv.bat face_recognition_explorer.py --photos_dir "%PHOTOS_DIR%" --scan --parallel --model %model%
    ) else (
        call run_with_venv.bat face_recognition_explorer.py --photos_dir "%PHOTOS_DIR%" --scan --model %model%
    )
)
pause
goto menu

:show
echo.
set /p index="Enter index of unlabeled face to show: "
call run_with_venv.bat face_recognition_explorer.py --photos_dir "%PHOTOS_DIR%" --show %index%
pause
goto menu

:label
echo.
set /p index="Enter index of unlabeled face: "
set /p name="Enter name for this face: "
call run_with_venv.bat face_recognition_explorer.py --photos_dir "%PHOTOS_DIR%" --label %index% --name "%name%"
pause
goto menu

:interactive
echo.
set /p tolerance="Enter tolerance value for face matching (0.4-0.7, lower=stricter): "
call run_with_venv.bat face_recognition_explorer.py --photos_dir "%PHOTOS_DIR%" --interactive --tolerance %tolerance%
pause
goto menu

:recognize
echo.
call run_with_venv.bat face_recognition_explorer.py --photos_dir "%PHOTOS_DIR%" --recognize
pause
goto menu

:group
echo.
set /p output_dir="Enter directory to save grouped photos (or press Enter for default): "
if not "%output_dir%"=="" (
    call run_with_venv.bat face_recognition_explorer.py --photos_dir "%PHOTOS_DIR%" --group --output_dir "%output_dir%"
) else (
    call run_with_venv.bat face_recognition_explorer.py --photos_dir "%PHOTOS_DIR%" --group
)
pause
goto menu

:create_search
echo.
set /p output_dir="Enter output directory (or press Enter to modify original files): "
if not "%output_dir%"=="" (
    call run_with_venv.bat face_recognition_explorer.py --photos_dir "%PHOTOS_DIR%" --create_search --output_dir "%output_dir%"
) else (
    call run_with_venv.bat face_recognition_explorer.py --photos_dir "%PHOTOS_DIR%" --create_search
)
pause
goto menu

:visualize
echo.
set /p output_dir="Enter directory to save visualizations (or press Enter for default): "
if not "%output_dir%"=="" (
    python face_recognition_explorer.py --photos_dir "%PHOTOS_DIR%" --visualize --output_dir "%output_dir%"
) else (
    python face_recognition_explorer.py --photos_dir "%PHOTOS_DIR%" --visualize
)
pause
goto menu

:export
echo.
python face_recognition_explorer.py --photos_dir "%PHOTOS_DIR%" --export
pause
goto menu

:end
echo.
echo Thank you for using Face Recognition File Explorer!
echo.
