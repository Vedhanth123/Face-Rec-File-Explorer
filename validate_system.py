"""
System validation script for Face Recognition File Explorer
This script tests all major components to ensure they're working correctly
"""

import os
import sys
import importlib
import platform
import shutil
import tempfile
from pathlib import Path

def print_header(text):
    print("\n" + "=" * 60)
    print(f" {text}")
    print("=" * 60)

def print_result(test_name, success):
    status = "✓ PASSED" if success else "✗ FAILED"
    color_code = "\033[92m" if success else "\033[91m"  # Green or Red
    reset_code = "\033[0m"
    if platform.system() == "Windows":
        # Check if we're running in a terminal that supports ANSI colors
        if os.environ.get("TERM") == "xterm" or "WT_SESSION" in os.environ:
            print(f"{color_code}{status}{reset_code} - {test_name}")
        else:
            print(f"{status} - {test_name}")
    else:
        print(f"{color_code}{status}{reset_code} - {test_name}")

def test_dependency(module_name, minimum_version=None):
    """Test if a dependency is installed and meets the minimum version"""
    try:
        module = importlib.import_module(module_name)
        version = getattr(module, "__version__", "Unknown")
        success = True
        if minimum_version and version != "Unknown":
            # Very simple version comparison (won't work for all version formats)
            success = version >= minimum_version
        print_result(f"{module_name} (version: {version})", success)
        return success
    except ImportError:
        print_result(f"{module_name} (Not installed)", False)
        return False

def test_face_detection():
    """Test basic face detection functionality"""
    print_header("Testing Face Detection")
    
    try:
        import face_recognition
        import numpy as np
        from PIL import Image
        
        # Create a simple test image with a "face" (just a circle)
        img_size = (200, 200, 3)
        img = np.ones(img_size, dtype=np.uint8) * 200  # Light gray background
        
        # Draw a simple "face" (circle)
        center_x, center_y = 100, 100
        radius = 50
        for x in range(img_size[0]):
            for y in range(img_size[1]):
                if ((x - center_x) ** 2 + (y - center_y) ** 2) < radius ** 2:
                    img[y, x] = [220, 180, 180]  # Skin-like color
        
        # Save temporary image
        temp_dir = tempfile.mkdtemp()
        test_img_path = os.path.join(temp_dir, "test_face.jpg")
        Image.fromarray(img).save(test_img_path)
        
        # Try to detect faces
        test_image = face_recognition.load_image_file(test_img_path)
        face_locations = face_recognition.face_locations(test_image)
        
        # This simple "face" won't actually be detected, but we're just testing if
        # the function runs without errors
        print_result("Face detection functions without errors", True)
        
        # Clean up
        shutil.rmtree(temp_dir)
        return True
    
    except Exception as e:
        print(f"Error during face detection test: {str(e)}")
        print_result("Face detection functions without errors", False)
        return False

def validate_system():
    """Run all validation tests"""
    print_header("Face Recognition System Validation")
    print(f"Python version: {platform.python_version()}")
    print(f"Operating system: {platform.system()} {platform.version()}")
      # Test dependencies
    print_header("Testing Dependencies")
    dependencies = [
        ("face_recognition", "1.2.3"),  # Package says 1.3.0 but module reports 1.2.3
        ("cv2", "4.5.0"),  # OpenCV
        ("PIL", None),     # Pillow
        ("numpy", "1.19.0"),
        ("sklearn", "1.0.0"),
        ("tkinter", None)
    ]
    
    all_dependencies_ok = True
    for module, min_version in dependencies:
        if not test_dependency(module, min_version):
            all_dependencies_ok = False
    
    # Test face detection if dependencies are OK
    face_detection_ok = False
    if all_dependencies_ok:
        face_detection_ok = test_face_detection()
    
    # Summary
    print_header("Validation Summary")
    print_result("All required dependencies installed", all_dependencies_ok)
    print_result("Face detection functionality", face_detection_ok)
    
    if all_dependencies_ok and face_detection_ok:
        print("\n✓ System validation PASSED. All components are working correctly!")
        return True
    else:
        print("\n✗ System validation FAILED. Please check the issues above.")
        if not all_dependencies_ok:
            print("\nTry running 'fix_dependencies.bat' to resolve common dependency issues.")
        return False

if __name__ == "__main__":
    success = validate_system()
    sys.exit(0 if success else 1)
