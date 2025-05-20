"""
Test script for verifying the integration between the GUI and face recognition functionality.
This script checks if the GUI app and direct imports from face recognition explorer work.
"""
import os
import sys
import cv2
import numpy as np
import tkinter as tk

def test_imports():
    """Test that all required modules can be imported"""
    print("Testing imports...")
    
    modules = [
        ("cv2", "OpenCV"),
        ("numpy", "NumPy"),
        ("face_recognition", "face_recognition"),
        ("PIL", "Pillow"),
        ("tkinter", "Tkinter"),
        ("sklearn.cluster", "scikit-learn")
    ]
    
    all_success = True
    for module_name, display_name in modules:
        try:
            __import__(module_name)
            print(f"✓ {display_name} successfully imported")
        except ImportError as e:
            print(f"✗ {display_name} import failed: {e}")
            all_success = False
    
    return all_success

def test_direct_integration():
    """Test direct integration between GUI and face recognition"""
    print("\nTesting direct integration...")
    
    try:
        from face_recognition_explorer import FaceRecognitionExplorer
        from face_recognizer_app import FaceRecognizerApp
        print("✓ Both modules imported successfully!")
        
        # Create a dummy photos directory
        os.makedirs("test_photos", exist_ok=True)
        
        # Create a test image with a simple shape that resembles a face
        test_img = np.ones((200, 200, 3), dtype=np.uint8) * 200
        center = (100, 100)
        color = (100, 150, 200)
        cv2.circle(test_img, center, 70, color, -1)
        cv2.rectangle(test_img, (70, 50), (130, 80), (150, 170, 200), -1)  # Eyes
        cv2.ellipse(test_img, (100, 130), (30, 10), 0, 0, 180, (120, 80, 90), -1)  # Mouth
        
        test_img_path = os.path.join("test_photos", "test_face.jpg")
        cv2.imwrite(test_img_path, test_img)
        
        # Try to create an explorer instance
        explorer = FaceRecognitionExplorer("test_photos")
        print("✓ FaceRecognitionExplorer instance created successfully")
        
        # Try to initialize a UI instance (without showing it)
        root = tk.Tk()
        root.withdraw()
        app = FaceRecognizerApp(root)
        print("✓ FaceRecognizerApp instance created successfully")
        
        # Success!
        return True
    except Exception as e:
        print(f"✗ Integration test failed: {e}")
        return False
    finally:
        # Clean up test files
        try:
            if os.path.exists(test_img_path):
                os.remove(test_img_path)
            if os.path.exists("test_photos"):
                os.rmdir("test_photos")
        except Exception:
            pass

def main():
    print("GUI Integration Test")
    print("===================\n")
    
    imports_ok = test_imports()
    if not imports_ok:
        print("\n❌ Some imports failed. Please fix these issues before proceeding.")
        return False
    
    integration_ok = test_direct_integration()
    if not integration_ok:
        print("\n❌ Integration test failed. GUI might need to fall back to subprocess mode.")
        return False
    
    print("\n✅ All tests passed! The GUI should be able to use direct integration.")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
