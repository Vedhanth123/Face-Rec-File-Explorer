# Setup script for Face Recognition File Explorer
# This will install all required dependencies

# Check if Python is installed
try {
    $pythonVersion = python --version
    Write-Host "Found $pythonVersion"
}
catch {
    Write-Host "Error: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.6+ from https://www.python.org/downloads/" -ForegroundColor Yellow
    Write-Host "Press any key to exit..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}

# Check if pip is available
try {
    python -m pip --version
    Write-Host "Pip is available"
}
catch {
    Write-Host "Error: pip not available. Attempting to install pip..." -ForegroundColor Yellow
    python -m ensurepip
}

# Install required Python packages
Write-Host "Installing required packages..." -ForegroundColor Green
try {
    # Fix the requirements.txt file first in case it's incorrect
    $requirements = Get-Content .\requirements.txt -ErrorAction SilentlyContinue
    if (-not $requirements) {
        # Create the file if it doesn't exist or is empty
        $requirements = @(
            "face_recognition>=1.3.0",
            "opencv-python>=4.5.0",
            "pillow>=8.0.0",
            "numpy>=1.19.0",
            "scikit-learn>=1.0.0"
        )
        $requirements | Out-File -FilePath .\requirements.txt -Encoding ascii
        Write-Host "Created requirements.txt file" -ForegroundColor Green
    }

    # Install from requirements file
    python -m pip install -r requirements.txt
    
    # Also ensure tkinter is available (system-dependent)
    Write-Host "Checking if tkinter is available..." -ForegroundColor Green
    $tkCheck = python -c "import tkinter; print('Tkinter is available')" 2>&1
    
    if ($tkCheck -like "*No module named 'tkinter'*") {
        Write-Host "Warning: tkinter is not available, which is needed for GUI features." -ForegroundColor Yellow
        Write-Host "To install tkinter on Windows:" -ForegroundColor Yellow
        Write-Host "1. Run the Python installer again" -ForegroundColor Yellow
        Write-Host "2. Select 'Modify'" -ForegroundColor Yellow
        Write-Host "3. Check 'tcl/tk and IDLE' in the optional features" -ForegroundColor Yellow
    }
    else {
        Write-Host "Tkinter is available" -ForegroundColor Green
    }
    
    # Special handling for dlib (which face_recognition depends on)
    Write-Host "Ensuring dlib is properly installed..." -ForegroundColor Green
    $dlibCheck = python -c "import dlib; print('dlib is available')" 2>&1
    
    if ($dlibCheck -like "*No module named 'dlib'*") {
        Write-Host "Attempting to install dlib..." -ForegroundColor Yellow
        # Try the pre-compiled wheel if available
        python -m pip install dlib 
        
        # Check again
        $dlibCheck = python -c "import dlib; print('dlib is available')" 2>&1
        if ($dlibCheck -like "*No module named 'dlib'*") {
            Write-Host "Warning: Could not install dlib automatically." -ForegroundColor Red
            Write-Host "You may need to install it manually from: https://github.com/ageitgey/face_recognition#installation" -ForegroundColor Yellow
        }
        else {
            Write-Host "dlib successfully installed" -ForegroundColor Green
        }
    }
    else {
        Write-Host "dlib is available" -ForegroundColor Green
    }
    
    Write-Host "All required packages installed successfully!" -ForegroundColor Green
}
catch {
    Write-Host "Error installing packages: $_" -ForegroundColor Red
    Write-Host "You may need to install some packages manually." -ForegroundColor Yellow
    Write-Host "See https://github.com/ageitgey/face_recognition#installation for help with dlib installation." -ForegroundColor Yellow
}

# Check if the virtual environment exists and activate it
if (Test-Path -Path ".\FaceRec\Scripts\Activate.ps1") {
    Write-Host "Virtual environment found. Activating..." -ForegroundColor Green
    & .\FaceRec\Scripts\Activate.ps1
}
else {
    Write-Host "No virtual environment found. Creating one..." -ForegroundColor Yellow
    python -m venv FaceRec
    if (Test-Path -Path ".\FaceRec\Scripts\Activate.ps1") {
        & .\FaceRec\Scripts\Activate.ps1
        
        # Install packages in the virtual environment
        python -m pip install -r requirements.txt
        Write-Host "Virtual environment created and activated with all packages installed!" -ForegroundColor Green
    }
    else {
        Write-Host "Could not create virtual environment. Will use system Python." -ForegroundColor Yellow
    }
}

Write-Host "`nSetup completed successfully!" -ForegroundColor Green
Write-Host "To start the Face Recognition File Explorer, run:" -ForegroundColor Green
Write-Host "  - GUI version: .\launch_gui.bat" -ForegroundColor Cyan
Write-Host "  - Command line version: .\run_face_explorer.bat" -ForegroundColor Cyan
Write-Host "`nPress any key to continue..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
