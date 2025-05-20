# Face Recognition Photo Organizer - GUI Guide

This guide explains how to use the graphical interface for organizing your photos by faces.

## Overview

The GUI application provides an easy way to process your photos:

1. Scan photos for faces
2. Interactively label people's faces
3. Recognize people across all photos
4. Organize photos by person
5. Browse the results in a generated gallery

## Step-by-step Usage

### Setup

1. **Launch the application**: Run `launch_gui.bat`
2. **Select Photos Directory**: Click "Browse" and select the folder containing your photos
3. **Select Output Directory** (Optional): Select where to save the organized photos. If not specified, they'll be saved in a "grouped" subfolder within your photos directory

### Configuration Options

- **Face Detection Model**:

  - HOG: Faster but less accurate
  - CNN: More accurate but slower

- **Parallel Processing**: Enable for faster scanning (uses more memory)
- **Force Rescan**: Re-process photos that have already been scanned
- **Face Matching Tolerance**: Adjust how strict the face matching should be (lower = stricter matching)

### Processing Steps

Follow these steps in order:

#### 1. Scan Photos

- Click "Scan Photos" to analyze your photo collection
- The system will find all faces in your photos
- This may take some time depending on your collection size
- Progress is shown in the status bar at the bottom

#### 2. Label Faces

- Click "Label Faces" to start interactive labeling
- You'll be shown groups of similar faces
- Enter the person's name to label the entire group
- Type "skip" to skip a group
- Press Cancel to end the labeling session
- The more faces you label, the better the recognition will be

#### 3. Recognize Faces

- Click "Recognize Faces" to identify people in all photos
- The system will use your labeled examples to recognize people
- Unknown faces will be kept for future labeling

#### 4. Group Photos

- Click "Group Photos" to organize photos by person
- Photos will be copied to the output directory, organized in folders by person name
- An HTML gallery will also be generated for easy browsing

#### 5. Browse Results

- Click "Browse Results" to open the generated gallery in your web browser
- Navigate through people and photos using the HTML interface
- You can also browse the organized folders directly

## Tips for Best Results

- Label at least 5-10 faces for each person for better recognition
- Adjust the face matching tolerance if you're getting incorrect matches
- Use the CNN model for more accurate detection if speed is not an issue
- Run the scan process periodically as you add new photos

## Troubleshooting

- **No faces detected**: Make sure your photos have clear, well-lit faces
- **Poor recognition**: Label more examples of each person
- **Program crashes**: Try disabling parallel processing to reduce memory usage
- **Long processing time**: Use the HOG model for faster but less accurate detection
