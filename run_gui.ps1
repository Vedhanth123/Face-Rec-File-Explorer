# PowerShell script to launch the face recognizer GUI application with proper Python environment
# filepath: c:\Code\Hobbies\Face Recognition File explorer\run_gui.ps1

# Define colors for console output
$Green = @{ForegroundColor = "Green" }
$Yellow = @{ForegroundColor = "Yellow" }
$Red = @{ForegroundColor = "Red" }
$Cyan = @{ForegroundColor = "Cyan" }

Write-Host "Face Recognition Photo Organizer" @Green
Write-Host "===============================" @Green
Write-Host

# Check if virtual environment exists
if (Test-Path ".\FaceRec\Scripts\Activate.ps1") {
    Write-Host "Activating virtual environment..." @Yellow
    try {
        & .\FaceRec\Scripts\Activate.ps1
        Write-Host "Virtual environment activated." @Cyan
    }
    catch {
        Write-Host "Error activating virtual environment: $_" @Red
        Write-Host "Will try to continue with system Python..." @Yellow
    }
}
else {
    Write-Host "Virtual environment not found. Using system Python." @Yellow
    Write-Host "For better results, run install_windows.bat first." @Yellow
}

# Test if required dependencies are available
try {
    Write-Host "Checking dependencies..." @Yellow
    $output = python -c "import face_recognition, cv2, PIL, numpy, sklearn, tkinter; print('OK')" 2>&1
    if ($output -ne "OK") {
        throw "Dependency check failed"
    }
    Write-Host "All dependencies available." @Cyan
}
catch {
    Write-Host "Error: Some dependencies are missing." @Red
    Write-Host "Running fix_dependencies script..." @Yellow
    
    if (Test-Path ".\fix_dependency_versions.ps1") {
        & .\fix_dependency_versions.ps1
    }
    else {
        Write-Host "Could not find fix_dependency_versions.ps1" @Red
        Write-Host "Please run fix_dependencies.bat manually." @Red
        pause
        exit 1
    }
}

# Launch the GUI
Write-Host "Launching Face Recognition GUI..." @Green
python face_recognizer_app.py

# Check exit code
if ($LASTEXITCODE -ne 0) {
    Write-Host "GUI application exited with error code $LASTEXITCODE" @Red
    Write-Host "Check the error messages above for more information." @Red
    Write-Host "If you're having dependency issues, try running fix_dependencies.bat" @Yellow
}
else {
    Write-Host "GUI application closed successfully." @Green
}

# Deactivate virtual environment if we're in one
if (Get-Command -Name deactivate -ErrorAction SilentlyContinue) {
    deactivate
}

pause
