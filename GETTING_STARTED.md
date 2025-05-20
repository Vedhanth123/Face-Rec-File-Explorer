# Getting Started with Face Recognition File Explorer

## System Requirements

- Windows 10 or 11 (for full Windows Explorer integration)
- Python 3.6 or higher
- At least 4GB RAM (8GB+ recommended for large photo collections)
- Sufficient disk space for your photos

## Installation Instructions

1. **Install Python**:

   - Download and install Python from [python.org](https://www.python.org/downloads/)
   - Make sure to check "Add Python to PATH" during installation

2. **Install Required Packages**:

   - Open a command prompt and navigate to the project directory
   - Run: `pip install -r requirements.txt`
   - Note: The face_recognition package requires dlib, which may need additional setup on some systems

3. **Verify Installation**:
   - Run the test script: `python test_face_recognition.py --download --test_dir test_images`
   - This will download sample images and test the face recognition functionality

## Quick Start Guide

1. **Prepare Your Photos**:

   - Copy or move your photos to a folder
   - The system will scan this folder and all subfolders for photos

2. **Launch the Tool**:

   - Run `run_face_explorer.bat` for the batch file interface, or
   - Run `powershell -ExecutionPolicy Bypass -File face_explorer.ps1` for the PowerShell interface

3. **Set Photos Directory**:

   - Choose option 1 from the menu
   - Enter the full path to your photos folder

4. **Scan Photos**:

   - Choose option 2 (or "Scan photos for faces")
   - Wait for the scan to complete (this may take some time for large collections)

5. **Label Faces**:

   - Choose option 3 (or "Show unlabeled face") to see a detected face
   - Then use option 4 (or "Label face") to assign a name to that face
   - Repeat this process for several photos of each person you want to recognize

6. **Recognize Faces**:

   - Choose option 5 (or "Recognize faces in all photos")
   - This will identify people in all photos based on your labeled examples

7. **Create Windows Search Files**:
   - Choose option 6 (or "Create Windows search files")
   - This creates property files that Windows Explorer can search

## Using Windows Search

After creating the search files, you can find photos by person name:

1. Open Windows Explorer and navigate to your photos folder
2. Type a person's name in the search box in the top right
3. Windows will find all photos containing that person

## Advanced Features

- **PowerShell Integration**: Use the PowerShell script for additional features like HTML reports
- **Face Visualization**: Generate annotated images showing recognized faces
- **JSON Export**: Export face data for use in other applications
- **Command Line Interface**: Use the Python script directly for automation

## Troubleshooting

- **Face Detection Issues**: If faces aren't being detected, ensure your photos have clear, well-lit faces
- **Recognition Accuracy**: The more examples you label per person, the better the recognition will be
- **Performance**: Processing large collections can be slow; consider working with smaller batches
- **Installation Problems**: If you have trouble with dlib/face_recognition, check the [installation guide](https://github.com/ageitgey/face_recognition#installation)

## Next Steps

- Try labeling at least 5-10 faces for each person for better recognition
- Organize your photo collection with consistent folder structures
- Set up regular scans for new photos
- Consider backing up your face database (face_database.pkl) file
