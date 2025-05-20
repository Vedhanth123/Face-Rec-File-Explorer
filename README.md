# Face Recognition File Explorer

This project allows you to scan, recognize, and search for faces in your photo collection. It integrates with Windows Explorer search by creating property files that make photos searchable by person name.

## Getting Started

For quick usage instructions, see the [QUICK_GUIDE.md](QUICK_GUIDE.md) file.

For more detailed documentation:

- [GETTING_STARTED.md](GETTING_STARTED.md): Comprehensive setup guide
- [GUI_HELP.md](GUI_HELP.md): How to use the graphical interface
- [QUICK_START_INTERACTIVE.md](QUICK_START_INTERACTIVE.md): Interactive labeling guide
- [HOW_IT_WORKS.md](HOW_IT_WORKS.md): Technical details

## Features

- **Face Detection**: Automatically detect faces in photos
- **Face Recognition**: Recognize people across multiple photos
- **Interactive Labeling**: Group similar faces and label multiple people at once
- **Face Clustering**: Group similar faces together automatically
- **Photo Organization**: Sort photos by person into folders with HTML galleries
- **Windows Integration**: Create property files that make photos searchable by person name in Windows Explorer
- **Visualization**: Create annotated photos with recognized faces
- **Export**: Export face data to JSON for other applications
- **Parallel Processing**: Speed up scanning of large photo collections

## Requirements

- Python 3.6+
- Required libraries:
  - face_recognition
  - opencv-python
  - pillow

## Installation

### Windows Installation (Recommended)

1. Clone or download this repository
2. Run the Windows installation script that uses pre-compiled packages:
   ```
   install_windows.bat
   ```
   This script will install all required dependencies without needing Visual C++ build tools.

### Manual Installation

If the Windows installation script doesn't work for you:

1. Install required Python libraries:

   ```
   pip install face_recognition opencv-python==4.5.5.64 pillow numpy==1.23.5 scikit-learn
   ```

   Note: The `face_recognition` library requires `dlib`, which can be difficult to install on Windows. Options:

   - Use a pre-compiled wheel: `pip install https://github.com/jloh02/dlib/releases/download/v19.22/dlib-19.22.99-cp310-cp310-win_amd64.whl`
   - Install Visual Studio 2019 with C++ build tools, then `pip install dlib`
   - See the [face_recognition documentation](https://github.com/ageitgey/face_recognition) for detailed installation instructions

### Fixing Dependency Issues

If you encounter errors related to NumPy or OpenCV compatibility, run:

```
fix_dependencies.bat
```

This will install specific compatible versions of NumPy and OpenCV that work together with face_recognition.

## Usage

### Quick Start

There are two ways to use this tool:

#### Graphical User Interface (Recommended)

Run the GUI application for a user-friendly interface:

```
launch_gui.bat
```

#### Command-Line Interface

Run the batch file for a text-based interactive menu:

```
run_face_explorer.bat
```

### Step-by-Step Process

1. **Set Photos Directory**: Point the tool to your photos folder
2. **Scan Photos**: Detect all faces in your photo collection
3. **Interactive Labeling**: The tool will show you groups of similar faces for naming
4. **Recognize Faces**: Use the labeled faces to identify people in all photos
5. **Group Photos**: Organize photos by person into folders
6. **Create Search Files**: Generate Windows-compatible property files for searching
7. **Browse Photos**: Use the HTML gallery to browse photos by person or search in Windows Explorer

### Command-Line Interface

For advanced users, you can use the Python script directly:

```
python face_recognition_explorer.py --photos_dir "path/to/photos" --scan
python face_recognition_explorer.py --photos_dir "path/to/photos" --show 0
python face_recognition_explorer.py --photos_dir "path/to/photos" --label 0 --name "John Doe"
python face_recognition_explorer.py --photos_dir "path/to/photos" --recognize
python face_recognition_explorer.py --photos_dir "path/to/photos" --create_search --output_dir "path/to/output"
```

## Windows Search Integration

This tool creates `.properties` files alongside your photos with "Person" tags. When you search in Windows Explorer, it will check these property files and show you photos with matching person names.

## Tips for Best Results

1. **Photo Quality**: Better face detection with clear, well-lit photos
2. **Multiple Samples**: Label multiple photos of each person for better recognition
3. **Face Angles**: Include photos with different face angles and expressions
4. **Processing Time**: Face detection and recognition can be slow for large collections
5. **GPU Acceleration**: For large collections, consider setting up GPU acceleration for faster processing

## Troubleshooting

- **Installation Issues**: If you have trouble installing `dlib` or `face_recognition`, check the [face_recognition installation guide](https://github.com/ageitgey/face_recognition#installation)
- **Recognition Accuracy**: If recognition is poor, try labeling more faces of the same person
- **Performance**: Processing large photo collections can be slow. Consider processing in smaller batches.

## Future Improvements

- Add a graphical user interface
- Improve recognition accuracy with additional models
- Add batch processing capabilities
- Implement automatic face clustering for easier labeling
