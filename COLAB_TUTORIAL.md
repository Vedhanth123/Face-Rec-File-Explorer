# Face Recognition System - Google Colab Tutorial

This guide explains how to use the Face Recognition System in Google Colab to organize your photos by faces with GPU acceleration.

## Overview

This system allows you to:

- Process large collections of photos quickly using Google Colab's GPU
- Detect and cluster similar faces automatically
- Label people in your photos
- Search for photos containing specific people
- Persist your data between Colab sessions using Google Drive

## Getting Started

### 1. Upload to Google Colab

1. Go to [Google Colab](https://colab.research.google.com/)
2. Click on **File** > **Upload notebook**
3. Upload the `Face_Recognition_System.ipynb` file from this folder

### 2. Enable GPU Acceleration

1. Click on **Runtime** > **Change runtime type**
2. Set **Hardware accelerator** to **GPU**
3. Click **Save**

### 3. Run the Notebook

Follow the instructions in the notebook, running each cell sequentially:

1. Install required libraries
2. Mount your Google Drive
3. Upload the `face_recognition_colab.py` file or paste the code
4. Initialize the explorer with paths to your Google Drive
5. Upload your photos
6. Scan photos for faces
7. Visualize and label face clusters
8. Recognize faces in all photos
9. Export results

## Data Persistence

Your data will be stored in the following locations in your Google Drive:

```
/MyDrive/FaceRecognitionProject/
├── photos/           # Your uploaded photos
├── output/           # Generated output files
└── face_database.pkl # Face database with encodings and labels
```

This ensures your data persists between different Colab sessions.

## Tips for Optimal Use

1. **Upload photos in batches**: If you have thousands of photos, consider processing them in smaller batches to avoid timeouts.

2. **Adjust clustering tolerance**: The `tolerance` parameter (default 0.6) determines how strictly faces are matched. Lower values (e.g., 0.5) create more clusters but with higher precision. Higher values (e.g., 0.7) create fewer clusters but might mix different people.

3. **Save frequently**: Run the `save_database()` cell periodically to ensure your work is saved to Google Drive.

4. **Process time**: Face detection is computationally intensive. A collection of 1,000 photos might take 10-30 minutes depending on photo size and GPU availability.

5. **Session timeouts**: Google Colab sessions disconnect after extended inactivity. If this happens, simply reconnect and run from where you left off - your data is preserved in Google Drive.

## Transferring Between Local and Colab

You can move your face database between local and Colab versions:

1. **Local → Colab**: Use the `upload_database()` function in the notebook
2. **Colab → Local**: Download the database using `export_results()` and place it in your local project folder

## Troubleshooting

- **Memory errors**: Reduce the batch size or image dimensions in the code
- **"Session crashed"**: Split your photo collection into smaller batches
- **Face detection issues**: Try adjusting the `model` parameter between 'hog' (faster) and 'cnn' (more accurate)
