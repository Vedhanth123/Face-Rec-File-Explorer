# Face Recognition Photo Organizer - Google Colab Version
# This notebook lets you process photos using GPU acceleration in Google Colab

import os
import pickle
import numpy as np
import cv2
import face_recognition
from PIL import Image
import argparse
from pathlib import Path
import shutil
import json
from sklearn.cluster import DBSCAN
import imghdr
import concurrent.futures
import threading
import zipfile
import io
from google.colab import files
import matplotlib.pyplot as plt
from tqdm.notebook import tqdm
import time

# Mount Google Drive
from google.colab import drive

# Configuration (change these paths as needed)
DEFAULT_BASE_DIR = '/content/drive/MyDrive/FaceRecognitionProject'
PHOTOS_DIR = f'{DEFAULT_BASE_DIR}/photos'  # Where the uploaded photos will be extracted
DATABASE_FILE = f'{DEFAULT_BASE_DIR}/face_database.pkl'  # Where to save the face database
OUTPUT_DIR = f'{DEFAULT_BASE_DIR}/output'  # Where to save results

class CoLabFaceRecognitionExplorer:
    def __init__(self, photos_dir=None, database_file=None, output_dir=None, mount_drive=True):
        """
        Initialize the face recognition system
        
        Args:
            photos_dir (str): Directory containing photos to process
            database_file (str): File to store face encodings and metadata
            output_dir (str): Directory to store output files
            mount_drive (bool): Whether to try mounting Google Drive
        """
        # Mount Google Drive if requested
        self.drive_mounted = False
        if mount_drive:
            try:
                drive.mount('/content/drive')
                self.drive_mounted = True
                print("Google Drive mounted successfully!")
            except Exception as e:
                print(f"Warning: Could not mount Google Drive: {e}")
                print("Data will NOT persist between sessions!")

        # Use default directories if none provided
        self.photos_dir = Path(photos_dir or PHOTOS_DIR)
        self.database_file = database_file or DATABASE_FILE
        self.output_dir = Path(output_dir or OUTPUT_DIR)
        
        # Create necessary directories
        os.makedirs(self.photos_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Load or create database
        self.face_database = self._load_database()
        
        # Keep track of last save time for auto-saving
        self.last_save_time = time.time()
        self.auto_save_interval = 60  # seconds
        
    def _load_database(self):
        """Load existing face database or create new one"""
        if os.path.exists(self.database_file):
            try:
                with open(self.database_file, 'rb') as f:
                    print(f"Loading existing database from {self.database_file}")
                    return pickle.load(f)
            except Exception as e:
                print(f"Error loading database: {e}")
                print("Creating new database...")
        
        # Create new database if file doesn't exist or couldn't be loaded
        return {
            'faces': {},  # name -> list of face encodings
            'photo_faces': {},  # photo_path -> list of (name, face_location)
            'unlabeled_faces': [],  # list of (photo_path, face_encoding, face_location)
            'metadata': {
                'created_at': time.time(),
                'last_updated': time.time(),
                'labeled_people': 0,
                'total_photos': 0,
                'total_faces': 0
            }
        }
    
    def save_database(self, force=False):
        """
        Save face database to disk
        
        Args:
            force (bool): Whether to save even if auto-save interval hasn't elapsed
        """
        current_time = time.time()
        
        # Only save if forced or auto-save interval has elapsed
        if force or (current_time - self.last_save_time) > self.auto_save_interval:
            # Update metadata
            self.face_database['metadata']['last_updated'] = current_time
            self.face_database['metadata']['labeled_people'] = len(self.face_database['faces'])
            self.face_database['metadata']['total_photos'] = len(self.face_database['photo_faces'])
            self.face_database['metadata']['total_faces'] = sum(len(encodings) for encodings in self.face_database['faces'].values())
            
            # Save to disk
            try:
                with open(self.database_file, 'wb') as f:
                    pickle.dump(self.face_database, f)
                print(f"Database saved to {self.database_file}")
                
                # If in Google Drive, create a backup periodically
                if self.drive_mounted and force:
                    backup_file = f"{self.database_file}.bak"
                    shutil.copy(self.database_file, backup_file)
                    print(f"Backup created at {backup_file}")
                    
                self.last_save_time = current_time
            except Exception as e:
                print(f"Error saving database: {e}")
                
    def upload_photos(self, extract_to_subfolders=True):
        """
        Upload photos to Google Colab
        
        Args:
            extract_to_subfolders (bool): Whether to extract zip files to subfolders
        """
        print("Please upload photos (zip file recommended for multiple photos)...")
        uploaded = files.upload()
        
        uploaded_count = 0
        
        for filename, content in uploaded.items():
            if filename.endswith('.zip'):
                # Extract zip file
                print(f"Extracting zip file {filename}...")
                
                # Create a subfolder based on zip name if requested
                if extract_to_subfolders:
                    folder_name = os.path.splitext(filename)[0]
                    extract_path = os.path.join(self.photos_dir, folder_name)
                    os.makedirs(extract_path, exist_ok=True)
                else:
                    extract_path = self.photos_dir
                    
                with zipfile.ZipFile(io.BytesIO(content), 'r') as zip_ref:
                    # Count extracted files
                    file_count = len(zip_ref.namelist())
                    zip_ref.extractall(extract_path)
                    uploaded_count += file_count
            else:
                # Save individual file
                save_path = os.path.join(self.photos_dir, filename)
                with open(save_path, 'wb') as f:
                    f.write(content)
                uploaded_count += 1
                    
        print(f"Uploaded {uploaded_count} files to {self.photos_dir}")
        
        # List photo directories
        print("\nPhoto directories:")
        for item in os.listdir(self.photos_dir):
            item_path = os.path.join(self.photos_dir, item)
            if os.path.isdir(item_path):
                file_count = sum(len(files) for _, _, files in os.walk(item_path))
                print(f" - {item}/: {file_count} files")
