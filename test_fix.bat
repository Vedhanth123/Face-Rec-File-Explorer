@echo off
REM filepath: c:\Code\Hobbies\Face Recognition File explorer\test_fix.bat
echo Testing Face Recognition Environment
echo ================================
echo.

REM Force the resolution of the virtual environment's Python by setting it at the beginning of PATH
set PATH=%~dp0FaceRec\Scripts;%PATH%

echo Testing Python location...
where python
echo.

echo Testing OpenCV import...
python -c "import cv2; print('OpenCV version:', cv2.__version__)"
echo.

echo Testing all imports...
python -c "import face_recognition, cv2, PIL, numpy, sklearn; print('All imports successful!')"
echo.

echo If you see "All imports successful!" above, the environment is working correctly.
echo You can now run the application using launch_gui.bat
echo.

pause
