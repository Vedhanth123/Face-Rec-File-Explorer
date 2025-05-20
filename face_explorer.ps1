# Face Recognition File Explorer PowerShell Integration
# This script provides additional Windows integration features

# Get the directory of this script
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Define the virtual environment paths
$venvPath = Join-Path $scriptDir "FaceRec"
$venvActivate = Join-Path $venvPath "Scripts\Activate.ps1"

# Function to activate virtual environment
function Activate-VirtualEnv {
    # Check if virtual environment exists
    if (Test-Path $venvActivate) {
        Write-Host "Using virtual environment..." -ForegroundColor Green
        # Activate the virtual environment
        & $venvActivate
        return $true
    } else {
        Write-Host "Virtual environment not found." -ForegroundColor Yellow
        return $false
    }
}

function Install-Requirements {
    Write-Host "Checking and installing required Python packages..."
    
    # Check if we're in a virtual environment, if not try to activate it
    $inVenv = $false
    if ($env:VIRTUAL_ENV -eq $null) {
        $inVenv = Activate-VirtualEnv
    } else {
        $inVenv = $true
    }
    
    # Check if pip is available
    try {
        python -m pip --version | Out-Null
    }
    catch {
        Write-Host "Error: pip not found. Please make sure Python is installed correctly." -ForegroundColor Red
        return $false
    }
    
    # Install requirements from file
    python -m pip install -r requirements.txt
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error installing required packages. Please see error messages above." -ForegroundColor Red
        return $false
    }
    
    Write-Host "All required packages installed successfully." -ForegroundColor Green
    return $true
}

function Register-WindowsSearchIntegration {
    param(
        [string]$PhotosDir
    )
    
    Write-Host "Registering Windows search integration for: $PhotosDir"
    
    # Create a .propertystore file if it doesn't exist
    $propertyStorePath = Join-Path $PhotosDir ".propertystore"
    if (!(Test-Path $propertyStorePath)) {
        @"
<?xml version="1.0" encoding="UTF-8"?>
<propertystore>
  <property name="Person" displayName="Person" searchable="true" />
</propertystore>
"@ | Out-File -FilePath $propertyStorePath -Encoding utf8
        
        Write-Host "Created property store definition file: $propertyStorePath" -ForegroundColor Green
    }
    
    Write-Host "Windows search integration is configured." -ForegroundColor Green
    Write-Host "You can now search for people in Windows Explorer using the search box." -ForegroundColor Green
}

function Create-FaceReportByPerson {
    param(
        [string]$JsonFile = "face_data.json",
        [string]$OutputHtml = "face_report.html"
    )
    
    if (!(Test-Path $JsonFile)) {
        Write-Host "Error: JSON file not found: $JsonFile" -ForegroundColor Red
        return
    }
    
    try {
        $faceData = Get-Content $JsonFile -Raw | ConvertFrom-Json
        
        $htmlContent = @"
<!DOCTYPE html>
<html>
<head>
    <title>Face Recognition Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        h1 { color: #333; }
        .person { margin-bottom: 30px; border-bottom: 1px solid #ddd; padding-bottom: 20px; }
        .person-name { font-size: 24px; color: #2c3e50; margin-bottom: 10px; }
        .photo-count { color: #7f8c8d; margin-bottom: 20px; }
        .photo-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 10px; }
        .photo-item { border: 1px solid #ddd; padding: 5px; text-align: center; }
        .photo-item img { max-width: 100%; height: auto; }
        .photo-path { font-size: 12px; color: #666; word-break: break-all; }
    </style>
</head>
<body>
    <h1>Face Recognition Report</h1>
"@
        
        foreach ($person in $faceData.people.PSObject.Properties) {
            $name = $person.Name
            $photoCount = $person.Value.photo_count
            $photos = $person.Value.photos
            
            $htmlContent += @"
    <div class="person">
        <div class="person-name">$name</div>
        <div class="photo-count">Found in $photoCount photos</div>
        <div class="photo-grid">
"@
            
            foreach ($photo in $photos) {
                $htmlContent += @"
            <div class="photo-item">
                <div class="photo-path">$photo</div>
            </div>
"@
            }
            
            $htmlContent += @"
        </div>
    </div>
"@
        }
        
        $htmlContent += @"
</body>
</html>
"@
        
        $htmlContent | Out-File -FilePath $OutputHtml -Encoding utf8
        Write-Host "Face report created: $OutputHtml" -ForegroundColor Green
        
        # Open the HTML file
        Start-Process $OutputHtml
    }
    catch {
        Write-Host "Error creating face report: $_" -ForegroundColor Red
    }
}

function Show-Menu {
    Clear-Host
    Write-Host "Face Recognition File Explorer - PowerShell Edition" -ForegroundColor Cyan
    Write-Host "=================================================" -ForegroundColor Cyan
    Write-Host ""
    
    $photosDir = if ($script:PhotosDir) { $script:PhotosDir } else { Join-Path $PSScriptRoot "photos" }
    Write-Host "Current photos directory: $photosDir" -ForegroundColor Yellow
    Write-Host ""
    
    Write-Host "1. Set photos directory"
    Write-Host "2. Install required packages"
    Write-Host "3. Run face recognition scan and labeling"
    Write-Host "4. Register Windows search integration"
    Write-Host "5. Create face report"
    Write-Host "6. Exit"
    Write-Host ""
    
    $choice = Read-Host "Enter your choice (1-6)"
    
    switch ($choice) {
        "1" {
            $newDir = Read-Host "Enter new photos directory path"
            if (Test-Path $newDir) {
                $script:PhotosDir = $newDir
                Write-Host "Photos directory set to: $newDir" -ForegroundColor Green
            }
            else {
                Write-Host "Directory not found: $newDir" -ForegroundColor Red
            }
            Read-Host "Press Enter to continue..."
            Show-Menu
        }
        "2" {
            Install-Requirements
            Read-Host "Press Enter to continue..."
            Show-Menu
        }
        "3" {
            & python face_recognition_explorer.py --photos_dir "$photosDir" --scan
            Read-Host "Press Enter to continue..."
            Show-Menu
        }
        "4" {
            Register-WindowsSearchIntegration -PhotosDir $photosDir
            Read-Host "Press Enter to continue..."
            Show-Menu
        }
        "5" {
            Create-FaceReportByPerson -JsonFile "face_data.json" -OutputHtml "face_report.html"
            Read-Host "Press Enter to continue..."
            Show-Menu
        }
        "6" {
            return
        }
        default {
            Write-Host "Invalid choice. Please try again." -ForegroundColor Red
            Read-Host "Press Enter to continue..."
            Show-Menu
        }
    }
}

# Initialize script variables
$script:PhotosDir = Join-Path $PSScriptRoot "photos"

# Start the menu
Show-Menu
