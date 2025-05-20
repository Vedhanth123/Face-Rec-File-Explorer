# Script to fix NumPy and OpenCV compatibility issues

Write-Host "Face Recognition Photo Organizer - Dependency Fix" -ForegroundColor Cyan
Write-Host "=================================================" -ForegroundColor Cyan
Write-Host

# Activate virtual environment if it exists
if (Test-Path ".\FaceRec\Scripts\Activate.ps1") {
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    .\FaceRec\Scripts\Activate.ps1
} else {
    Write-Host "Virtual environment not found. Using system Python." -ForegroundColor Yellow
    Write-Host "You may need to run install_windows.bat first." -ForegroundColor Yellow
    Write-Host
}

Write-Host "Fixing NumPy and OpenCV compatibility issues..." -ForegroundColor Yellow

# Uninstall current NumPy and OpenCV
Write-Host "Uninstalling current NumPy and OpenCV..." -ForegroundColor Yellow
python -m pip uninstall -y numpy opencv-python

# Install specific compatible versions
Write-Host "Installing compatible NumPy version..." -ForegroundColor Yellow
python -m pip install numpy==1.23.5

Write-Host "Installing compatible OpenCV version..." -ForegroundColor Yellow
python -m pip install opencv-python==4.5.5.64

# Verify installation
Write-Host "Verifying installation..." -ForegroundColor Yellow
$result = python -c "import numpy, cv2; print(f'NumPy version: {numpy.__version__}'); print(f'OpenCV version: {cv2.__version__}')" 2>&1

if ($LASTEXITCODE -eq 0) {
    Write-Host "`nSuccess! Dependencies are now compatible." -ForegroundColor Green
    Write-Host $result -ForegroundColor Cyan
    Write-Host "`nYou can now run the face recognition application." -ForegroundColor Green
} else {
    Write-Host "`nThere was a problem with the installation:" -ForegroundColor Red
    Write-Host $result -ForegroundColor Red
    Write-Host "`nPlease check TROUBLESHOOTING.md for more information." -ForegroundColor Yellow
}

Write-Host "`nPress any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
