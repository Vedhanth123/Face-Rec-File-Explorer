# Face Recognition Photo Organizer - Quick Guide

## Starting the Application

To start the application, run one of these commands:

```
launch_gui.bat
```

or

```
.\run_with_venv.bat face_recognizer_app.py
```

## Working with Face Recognition

### Basic Workflow

1. **Scan Photos**: Select a folder with photos and click "Scan Photos"
2. **Label Faces**: Use "Label Faces" to identify people in your photos
3. **Recognize Faces**: Find all photos containing the labeled people
4. **Group Photos**: Organize photos by person into folders
5. **Browse Results**: View the organized photos in your browser

### Detailed Steps

#### 1. Scan Photos

- Select the folder containing your photos using "Browse"
- Choose detection model: "hog" (faster) or "cnn" (more accurate)
- Check "Parallel Processing" for faster scanning on multi-core systems
- Click "Scan Photos" to begin
- The scan may take several minutes depending on how many photos you have

#### 2. Label Faces

- After scanning, click "Label Faces"
- The system will show groups of similar faces
- Enter names for the people shown or type "skip" to skip
- You can adjust the tolerance setting for face matching:
  - Lower values (0.4-0.5) require closer matches (fewer false positives)
  - Higher values (0.6-0.7) allow more variation (fewer false negatives)

#### 3. Recognize Faces

- After labeling, click "Recognize Faces"
- This process applies the labels to all photos
- New, unlabeled faces will be added to the database

#### 4. Group Photos

- Choose an output directory (optional)
- Click "Group Photos"
- The system will:
  - Create folders for each person
  - Copy photos into the appropriate folders
  - Create an HTML gallery for easy browsing

#### 5. Browse Results

- Click "Browse Results" to open the HTML gallery
- You can navigate between people and view all their photos

## Tips for Best Results

- Use clear, well-lit photos for best face detection
- The first time you scan, be patient - it may take time
- Label at least 5-10 photos of each person for better recognition
- Use the "Interactive" labeling for faster identification
- If photos are mislabeled, you can fix them by rescanning and relabeling

## Command Line Usage

You can also use the system from the command line for more options:

```
.\run_with_venv.bat face_recognition_explorer.py --photos_dir "path\to\photos" --help
```

This will show all available command line options.

## Troubleshooting

If you encounter issues:

1. Run `validate_system.bat` to check if all components are working
2. Run `fix_dependencies.bat` if you see import errors
3. Check TROUBLESHOOTING.md for detailed solutions

For more detailed documentation, see:

- GETTING_STARTED.md
- HOW_IT_WORKS.md
- QUICK_START_INTERACTIVE.md
