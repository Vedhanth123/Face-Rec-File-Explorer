# Install dlib and face_recognition using pre-compiled wheels for Windows
# This approach avoids the need for Visual C++ build tools

# Define error handler
function Show-Error {
    param($Message)
    Write-Host "ERROR: $Message" -ForegroundColor Red
    Write-Host "Press any key to exit..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}

# Check Python version
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Found $pythonVersion" -ForegroundColor Green
}
catch {
    Show-Error "Python is not installed or not in PATH. Please install Python 3.6+ from https://www.python.org/downloads/"
}

# Ensure pip is up to date
Write-Host "Upgrading pip to latest version..." -ForegroundColor Yellow
python -m pip install --upgrade pip

# Create a virtual environment if it doesn't exist
if (-not (Test-Path ".\FaceRec")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv FaceRec
}

# Activate the virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
if ($PSVersionTable.PSVersion.Major -ge 5) {
    .\FaceRec\Scripts\Activate.ps1
}
else {
    Show-Error "PowerShell version 5 or higher is required."
}

# Install dlib from pre-compiled wheel
Write-Host "Installing pre-compiled dlib wheel..." -ForegroundColor Yellow
python -m pip install --upgrade https://github.com/jloh02/dlib/releases/download/v19.22/dlib-19.22.99-cp310-cp310-win_amd64.whl

# Check if dlib installed successfully
$dlibInstalled = python -c "import dlib; print('OK')" 2>$null
if ($dlibInstalled -ne "OK") {
    Write-Host "Failed to install dlib. Trying alternative method..." -ForegroundColor Red
    
    # Try an alternative wheel source
    python -m pip install --upgrade https://github.com/eigenform/face-recognizer-wheelhouses/raw/main/dlib-19.24.0-cp310-cp310-win_amd64.whl
    
    # Check again
    $dlibInstalled = python -c "import dlib; print('OK')" 2>$null
    if ($dlibInstalled -ne "OK") {
        Show-Error "Could not install dlib. Please install Visual Studio 2019 with C++ build tools and try again."
    }
}

# Now install face_recognition (it will use the pre-installed dlib)
Write-Host "Installing face_recognition..." -ForegroundColor Yellow
python -m pip install face_recognition

# Check if face_recognition installed properly
$faceRecognitionInstalled = python -c "import face_recognition; print('OK')" 2>$null
if ($faceRecognitionInstalled -ne "OK") {
    Show-Error "Failed to install face_recognition package."
}

# Install specific compatible versions of packages
Write-Host "Installing compatible versions of packages..." -ForegroundColor Yellow
# Install numpy first with specific version for OpenCV compatibility
python -m pip install numpy==1.23.5
# Install OpenCV with specific version
python -m pip install opencv-python==4.5.5.64
# Install other required packages
python -m pip install pillow scikit-learn

# Verify all packages are installed
Write-Host "`nVerifying installed packages..." -ForegroundColor Green
python -c "import face_recognition, cv2, PIL, numpy, sklearn; print('All packages installed successfully!')"
$opencvVersion = python -c "import cv2; print(f'OpenCV version: {cv2.__version__}')"
$numpyVersion = python -c "import numpy; print(f'NumPy version: {numpy.__version__}')"
Write-Host $opencvVersion -ForegroundColor Cyan
Write-Host $numpyVersion -ForegroundColor Cyan

Write-Host "`nSetup completed! You can now run the face recognition application." -ForegroundColor Green
Write-Host "Run 'launch_gui.bat' to start the graphical interface" -ForegroundColor Cyan
