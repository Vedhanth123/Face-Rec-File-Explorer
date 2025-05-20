import os
import argparse
import urllib.request
import zipfile
import shutil
from pathlib import Path

def download_sample_data(output_dir):
    """Download sample dataset for testing the face recognition system"""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    print(f"Downloading sample dataset to {output_dir}...")
    
    # URLs for sample datasets
    datasets = {
        "lfw-sample": {
            "url": "http://vis-www.cs.umass.edu/lfw/lfw-deepfunneled.tgz",
            "filename": "lfw-deepfunneled.tgz",
            "extract_command": "tar -xzf"  # Use tar for .tgz files
        },
        "celebrity-faces": {
            "url": "https://github.com/ageitgey/face_recognition/files/933564/test-images-2.zip",
            "filename": "celebrity-faces.zip",
            "extract_command": None  # Will use Python's zipfile module
        }
    }
    
    # Choose which dataset to download (currently hardcoded to celebrity-faces for simplicity)
    dataset = datasets["celebrity-faces"]
    
    zip_path = output_path / dataset["filename"]
    
    try:
        # Download the dataset
        print(f"Downloading from {dataset['url']}...")
        urllib.request.urlretrieve(dataset["url"], zip_path)
        
        # Extract the dataset
        print(f"Extracting to {output_dir}...")
        
        if dataset["extract_command"] is None:
            # Use Python's zipfile module
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(output_path)
        else:
            # Use external command
            os.system(f"cd {output_path} && {dataset['extract_command']} {dataset['filename']}")
        
        # Clean up the downloaded archive
        os.remove(zip_path)
        
        print("Sample dataset downloaded and extracted successfully!")
        return True
        
    except Exception as e:
        print(f"Error downloading sample data: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Download sample data for face recognition testing")
    parser.add_argument("--output_dir", type=str, default="sample_photos",
                       help="Directory to save sample photos (default: sample_photos)")
    
    args = parser.parse_args()
    
    download_sample_data(args.output_dir)

if __name__ == "__main__":
    main()
