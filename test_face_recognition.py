import os
import argparse
import urllib.request
import shutil
import zipfile
import face_recognition
from PIL import Image, ImageDraw

def download_test_images(output_dir):
    """Download some sample images for testing face recognition"""
    os.makedirs(output_dir, exist_ok=True)
    
    # URL for a small set of test images
    test_images_url = "https://github.com/ageitgey/face_recognition/files/933564/test-images-2.zip"
    zip_path = os.path.join(output_dir, "test-images.zip")
    
    print(f"Downloading test images from {test_images_url}")
    try:
        urllib.request.urlretrieve(test_images_url, zip_path)
        
        print(f"Extracting test images to {output_dir}")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(output_dir)
            
        # Clean up zip file
        os.remove(zip_path)
        print(f"Test images downloaded and extracted to {output_dir}")
        return True
    except Exception as e:
        print(f"Error downloading test images: {e}")
        return False

def test_face_recognition(image_dir):
    """Test basic face recognition functionality"""
    image_files = [f for f in os.listdir(image_dir) 
                if os.path.isfile(os.path.join(image_dir, f)) and 
                f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    if not image_files:
        print(f"No image files found in {image_dir}")
        return False
    
    print(f"Testing face recognition on {len(image_files)} images")
    
    # Process each image
    for img_file in image_files:
        img_path = os.path.join(image_dir, img_file)
        print(f"Processing {img_path}")
        
        # Load image
        image = face_recognition.load_image_file(img_path)
        
        # Find faces
        face_locations = face_recognition.face_locations(image)
        print(f"Found {len(face_locations)} faces in {img_file}")
        
        # Create output image with faces highlighted
        pil_image = Image.fromarray(image)
        draw = ImageDraw.Draw(pil_image)
        
        for (top, right, bottom, left) in face_locations:
            draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255), width=2)
            
        # Save output image
        output_path = os.path.join(image_dir, f"detected_{img_file}")
        pil_image.save(output_path)
        print(f"Saved detected faces to {output_path}")
    
    print("Face recognition test completed successfully!")
    return True

def main():
    parser = argparse.ArgumentParser(description="Test face recognition functionality")
    parser.add_argument('--download', action='store_true', help='Download test images')
    parser.add_argument('--test_dir', type=str, default='test_images', 
                        help='Directory for test images')
    
    args = parser.parse_args()
    
    if args.download:
        if download_test_images(args.test_dir):
            print("Download completed successfully")
        else:
            print("Failed to download test images")
            return
    
    test_face_recognition(args.test_dir)

if __name__ == "__main__":
    main()
