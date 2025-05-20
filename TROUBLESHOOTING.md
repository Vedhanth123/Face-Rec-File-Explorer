# Troubleshooting Installation Issues

This guide covers common problems and solutions for installing the Face Recognition File Explorer.

## Issues Installing dlib on Windows

### Issue: "You must use Visual Studio to build a python extension on Windows"

This error occurs because dlib requires C++ compilation tools to build from source.

**Solution 1: Use our Windows installation script**

```
install_windows.bat
```

This script will install pre-compiled versions of dlib that don't require Visual Studio.

**Solution 2: Install Visual Studio with C++ build tools**

1. Download [Visual Studio Community](https://visualstudio.microsoft.com/vs/community/)
2. During installation, select "Desktop development with C++"
3. After installation, try installing dlib again:
   ```
   pip install dlib
   ```

**Solution 3: Install a pre-compiled wheel manually**

For Python 3.10 on Windows 64-bit:

```
pip install https://github.com/jloh02/dlib/releases/download/v19.22/dlib-19.22.99-cp310-cp310-win_amd64.whl
```

For other versions, search for compatible wheels at:

- https://github.com/eigenform/face-recognizer-wheelhouses
- https://github.com/jloh02/dlib/releases/

## Issues with tkinter

### Issue: "No module named 'tkinter'"

This occurs when Python is installed without tkinter, which is needed for the GUI.

**Solution:**

1. Reinstall Python
2. During installation, enable "tcl/tk and IDLE" option
3. Alternatively, install tkinter for your distribution:
   - Windows: Included with standard Python installation
   - Linux (Ubuntu): `sudo apt-get install python3-tk`
   - macOS: `brew install python-tk@3.10` (adjust for your Python version)

## Issues with opencv-python

### Issue: "ImportError: DLL load failed while importing cv2"

This occurs when OpenCV can't find necessary system libraries.

**Solution:**

Try installing an older version of OpenCV:

```
pip uninstall opencv-python
pip install opencv-python==4.5.5.64
```

### Issue: "ModuleNotFoundError: No module named 'cv2'"

This occurs when Python can't find the OpenCV module, often due to virtual environment issues.

**Solution 1: Use our fix dependencies script**

```
fix_dependencies.bat
```

**Solution 2: Ensure proper virtual environment activation**

```
.\FaceRec\Scripts\activate
python -c "import cv2"
```

**Solution 3: Use our robust launcher**

Instead of running the Python script directly, use:

```
run_explorer.bat --photos_dir "path/to/photos" --interactive
```

This script ensures correct environment setup before running.

### Issue: "ImportError: numpy.core.multiarray failed to import"

This error occurs when there's a compatibility issue between NumPy and OpenCV versions.

**Solution:**

Install a compatible version of NumPy:

```
pip uninstall -y numpy
pip install numpy==1.23.5
```

Then reinstall OpenCV with a compatible version:

```
pip uninstall -y opencv-python
pip install opencv-python==4.5.5.64
```

## Issues with face_recognition

### Issue: "ModuleNotFoundError: No module named 'face_recognition'"

**Solution:**

Install face_recognition after installing dlib:

```
pip install dlib
pip install face_recognition
```

## General Troubleshooting

If you continue to experience issues:

1. Create a fresh virtual environment:

   ```
   python -m venv fresh_env
   fresh_env\Scripts\activate
   ```

2. Install packages one by one to identify where the issue occurs:

   ```
   pip install dlib
   pip install face_recognition
   pip install opencv-python
   pip install pillow
   pip install scikit-learn
   ```

3. Check Python version compatibility:

   - This project works best with Python 3.8-3.10
   - dlib can be problematic with the latest Python versions

4. For further assistance, please create an issue on our GitHub repository.
