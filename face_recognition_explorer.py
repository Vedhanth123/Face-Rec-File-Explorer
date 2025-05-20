import os
import pickle
import numpy as np
import cv2
import face_recognition
from PIL import Image, ImageDraw
import argparse
from pathlib import Path
import shutil
import json
import tkinter as tk
from tkinter import simpledialog, messagebox
from sklearn.cluster import DBSCAN
import imghdr
import concurrent.futures
import threading

class FaceRecognitionExplorer:
    def __init__(self, photos_dir, database_file='face_database.pkl'):
        """
        Initialize the face recognition system
        
        Args:
            photos_dir (str): Directory containing photos to process
            database_file (str): File to store face encodings and metadata
        """
        self.photos_dir = Path(photos_dir)
        self.database_file = database_file
        self.face_database = self._load_database()
        self._tk_root = None
        
    def _load_database(self):
        """Load existing face database or create new one"""
        if os.path.exists(self.database_file):
            with open(self.database_file, 'rb') as f:
                return pickle.load(f)
        else:
            return {
                'faces': {},  # name -> list of face encodings
                'photo_faces': {},  # photo_path -> list of (name, face_location)
                'unlabeled_faces': []  # list of (photo_path, face_encoding, face_location)
            }
        def save_database(self):
            """Save face database to disk"""
            with open(self.database_file, 'wb') as f:
                pickle.dump(self.face_database, f)
            
    def scan_photos(self, force_rescan=False, parallel=True, model="hog"):
        """
        Scan photos directory for faces
        
        Args:
            force_rescan (bool): Whether to rescan already processed photos
            parallel (bool): Whether to use parallel processing
            model (str): Face detection model ('hog' or 'cnn')
        """
        print(f"Scanning photos in {self.photos_dir}...")
        photo_paths = []
        
        # Find valid image files
        for ext in ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.gif']:
            photo_paths.extend(list(self.photos_dir.glob(f"**/{ext}")))
            
        # Filter already processed files
        if not force_rescan:
            photo_paths = [
                p for p in photo_paths 
                if str(p.relative_to(self.photos_dir)) not in self.face_database['photo_faces']
            ]
            
        print(f"Found {len(photo_paths)} photos to process")
        
        # Database lock for parallel processing
        db_lock = threading.Lock()
        processed_count = 0
        new_face_count = 0
        
        # Function to process a single image
        def process_image(photo_path):
            nonlocal processed_count, new_face_count
            
            rel_path = photo_path.relative_to(self.photos_dir)
            
            try:
                # Verify this is really an image file
                if not self._is_valid_image(photo_path):
                    return 0
                
                # Load image
                image = face_recognition.load_image_file(photo_path)
                
                # Find all faces in the image
                face_locations = face_recognition.face_locations(image, model=model)
                
                if not face_locations:
                    return 0
                    
                face_encodings = face_recognition.face_encodings(image, face_locations)
                
                # Store unlabeled faces for later naming
                face_count = len(face_encodings)
                
                if face_count > 0:
                    with db_lock:
                        for face_encoding, face_location in zip(face_encodings, face_locations):
                            self.face_database['unlabeled_faces'].append(
                                (str(rel_path), face_encoding, face_location)
                            )
                        new_face_count += face_count
                
                return face_count
                
            except Exception as e:
                print(f"Error processing {rel_path}: {e}")
                return 0
        
        # Process images (parallel or sequential)
        if parallel and len(photo_paths) > 10:
            with concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
                future_to_path = {
                    executor.submit(process_image, path): path for path in photo_paths
                }
                
                for i, future in enumerate(concurrent.futures.as_completed(future_to_path)):
                    photo_path = future_to_path[future]
                    rel_path = photo_path.relative_to(self.photos_dir)
                    face_count = future.result()
                    
                    processed_count += 1
                    print(f"Processing image {processed_count}/{len(photo_paths)}: {rel_path} - Found {face_count} faces")
                    
                    # Save progress periodically
                    if processed_count % 20 == 0:
                        with db_lock:
                            self.save_database()
        else:
            for i, photo_path in enumerate(photo_paths):
                rel_path = photo_path.relative_to(self.photos_dir)
                
                face_count = process_image(photo_path)
                processed_count += 1
                
                print(f"Processing image {processed_count}/{len(photo_paths)}: {rel_path} - Found {face_count} faces")
                
                # Save progress periodically
                if i % 10 == 0:
                    self.save_database()
                    
        self.save_database()
        print(f"Scan complete. Found {new_face_count} new faces.")
        print(f"Total unlabeled faces: {len(self.face_database['unlabeled_faces'])}")
        
    def _is_valid_image(self, file_path):
        """Check if file is a valid image"""
        try:
            if not os.path.isfile(file_path):
                return False
                
            # Use imghdr to identify if it's an image
            image_type = imghdr.what(file_path)
            if image_type is None:
                return False
                
            return True
        except Exception:
            return False
    
    def label_face(self, index, name):
        """
        Label a face with a name
        
        Args:
            index (int): Index of unlabeled face
            name (str): Person's name to assign
        """
        if index >= len(self.face_database['unlabeled_faces']):
            print(f"Invalid index: {index}")
            return False
            
        photo_path, face_encoding, face_location = self.face_database['unlabeled_faces'][index]
        
        # Add to named faces
        if name not in self.face_database['faces']:
            self.face_database['faces'][name] = []
        self.face_database['faces'][name].append(face_encoding)
        
        # Add to photo_faces
        if photo_path not in self.face_database['photo_faces']:
            self.face_database['photo_faces'][photo_path] = []
        self.face_database['photo_faces'][photo_path].append((name, face_location))
        
        # Remove from unlabeled
        self.face_database['unlabeled_faces'].pop(index)
        
        self.save_database()
        return True
    
    def show_unlabeled_face(self, index):
        """
        Show an unlabeled face for identification
        
        Args:
            index (int): Index of unlabeled face
        """
        if index >= len(self.face_database['unlabeled_faces']):
            print(f"Invalid index: {index}")
            return
            
        photo_path, _, face_location = self.face_database['unlabeled_faces'][index]
        full_path = self.photos_dir / photo_path
        
        if not full_path.exists():
            print(f"Photo file not found: {full_path}")
            return
            
        # Load image and highlight face
        image = cv2.imread(str(full_path))
        top, right, bottom, left = face_location
        cv2.rectangle(image, (left, top), (right, bottom), (0, 0, 255), 2)
        
        # Show image
        cv2.imshow(f"Face #{index}", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        def recognize_faces(self, tolerance=0.6, model="hog"):
            """
            Recognize and label all faces in photos using the current database
            
            Args:
                tolerance (float): Face matching tolerance (lower=stricter)
                model (str): Face detection model ('hog' or 'cnn')
            """
            print("Recognizing faces in all photos...")
            
            # Reset photo_faces
            self.face_database['photo_faces'] = {}
            
            photo_paths = []
            for ext in ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.gif']:
                photo_paths.extend(list(self.photos_dir.glob(f"**/{ext}")))
            
            # Get all known face encodings and names
            known_face_encodings = []
            known_face_names = []
            
            for name, encodings in self.face_database['faces'].items():
                for encoding in encodings:
                    known_face_encodings.append(encoding)
                    known_face_names.append(name)
            
            if not known_face_encodings:
                print("No known faces in database. Please label some faces first.")
                return
            
            for i, photo_path in enumerate(photo_paths):
                rel_path = photo_path.relative_to(self.photos_dir)
                print(f"Processing image {i+1}/{len(photo_paths)}: {rel_path}")
                
                try:
                    # Load image
                    image = face_recognition.load_image_file(photo_path)
                    
                    # Find all faces
                    face_locations = face_recognition.face_locations(image)
                    face_encodings = face_recognition.face_encodings(image, face_locations)
                    
                    faces_in_photo = []
                    
                    for face_encoding, face_location in zip(face_encodings, face_locations):
                        # Compare face to known faces
                        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                        
                        if not any(matches):
                            # Unknown face
                            self.face_database['unlabeled_faces'].append((str(rel_path), face_encoding, face_location))
                            continue
                        
                        # Use the closest match
                        best_match_index = np.argmin(face_distances)
                        if matches[best_match_index]:
                            name = known_face_names[best_match_index]
                            faces_in_photo.append((name, face_location))
                    
                    if faces_in_photo:
                        self.face_database['photo_faces'][str(rel_path)] = faces_in_photo
                        
                    # Save progress periodically
                    if i % 10 == 0:
                        self.save_database()
                        
                except Exception as e:
                    print(f"Error processing {rel_path}: {e}")
                    
            self.save_database()
            print("Recognition complete.")
            
    def create_windows_search_files(self, output_dir=None):
        """
        Create Windows search property files for all photos with faces
        
        Args:
            output_dir (str, optional): Directory to copy photos and property files to
        """
        if output_dir:
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
        else:
            output_path = self.photos_dir
            
        # Group photos by person
        person_photos = {}
        for photo_path, faces in self.face_database['photo_faces'].items():
            for name, _ in faces:
                if name not in person_photos:
                    person_photos[name] = []
                person_photos[name].append(photo_path)
                
        # Create search property files
        for name, photos in person_photos.items():
            print(f"Creating search files for {name} with {len(photos)} photos")
            
            for photo_path in photos:
                src_path = self.photos_dir / photo_path
                if not src_path.exists():
                    print(f"Source photo not found: {src_path}")
                    continue
                    
                # Copy photo to output directory if needed
                if output_dir:
                    # Preserve directory structure
                    dst_dir = output_path / Path(photo_path).parent
                    dst_dir.mkdir(parents=True, exist_ok=True)
                    dst_path = output_path / photo_path
                    shutil.copy2(src_path, dst_path)
                else:
                    dst_path = src_path
                
                # Create property file (.properties) with person tags
                prop_path = dst_path.parent / f"{dst_path.stem}.properties"
                with open(prop_path, 'w') as f:
                    f.write(f"Person={name}")
        
        print(f"Created Windows search files for {len(person_photos)} people.")
    
    def export_face_data(self, output_file='face_data.json'):
        """
        Export face data to JSON for other applications
        
        Args:
            output_file (str): JSON file to export to
        """
        export_data = {
            'people': {},
            'photos': {}
        }
        
        # Export people data
        for name in self.face_database['faces'].keys():
            export_data['people'][name] = {
                'photo_count': 0,
                'photos': []
            }
        
        # Export photo data
        for photo_path, faces in self.face_database['photo_faces'].items():
            people_in_photo = []
            for name, _ in faces:
                people_in_photo.append(name)
                export_data['people'][name]['photo_count'] += 1
                export_data['people'][name]['photos'].append(photo_path)
                
            export_data['photos'][photo_path] = {
                'people': people_in_photo
            }
            
        with open(output_file, 'w') as f:
            json.dump(export_data, f, indent=2)
            
        print(f"Exported face data to {output_file}")
            
    def visualize_faces(self, output_dir):
        """
        Create visualizations of recognized faces
        
        Args:
            output_dir (str): Directory to save visualizations
        """
        out_path = Path(output_dir)
        out_path.mkdir(parents=True, exist_ok=True)
        
        # Create individual face visualizations
        for photo_path, faces in self.face_database['photo_faces'].items():
            if not faces:
                continue
                
            try:
                full_path = self.photos_dir / photo_path
                if not full_path.exists():
                    continue
                    
                image = Image.open(full_path)
                draw = ImageDraw.Draw(image)
                
                # Draw rectangles and names
                for name, face_location in faces:
                    top, right, bottom, left = face_location
                    draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255), width=2)
                    draw.text((left, top - 20), name, fill=(0, 0, 255))
                
                # Save annotated image
                out_file = out_path / f"annotated_{Path(photo_path).name}"
                image.save(out_file)
                
            except Exception as e:
                print(f"Error visualizing {photo_path}: {e}")
                
        print(f"Saved face visualizations to {output_dir}")
    
    def cluster_faces(self, tolerance=0.6):
        """
        Cluster unlabeled faces to group similar faces together
        
        Args:
            tolerance (float): Threshold for face similarity (lower = stricter)
            
        Returns:
            list: List of clusters, where each cluster is a list of face indices
        """
        if not self.face_database['unlabeled_faces']:
            print("No unlabeled faces to cluster.")
            return []
            
        # Extract face encodings from unlabeled faces
        encodings = [face[1] for face in self.face_database['unlabeled_faces']]
        
        # Cluster faces using DBSCAN
        clustering = DBSCAN(metric="euclidean", n_jobs=-1, 
                           eps=tolerance, min_samples=1).fit(encodings)
                           
        # Group by cluster label
        clusters = {}
        for i, label in enumerate(clustering.labels_):
            if label not in clusters:
                clusters[label] = []
            clusters[label].append(i)
            
        # Sort clusters by size (largest first)
        sorted_clusters = sorted(clusters.values(), key=len, reverse=True)
        
        return sorted_clusters
        def interactive_labeling(self, tolerance=0.6, max_faces_per_prompt=5):
            """
            Interactive mode to label faces with a GUI
            
            Args:
                tolerance (float): Threshold for face similarity (lower = stricter)
                max_faces_per_prompt (int): Maximum number of faces to show per prompt
            """
            if not self.face_database['unlabeled_faces']:
                print("No unlabeled faces found. Run scan first.")
                return
                
            # Initialize tkinter for GUI dialogs
            if self._tk_root is None:
                self._tk_root = tk.Tk()
                self._tk_root.withdraw()  # Hide the main window
                
            # Show instructions
            messagebox.showinfo(
                "Interactive Labeling",
                "You'll be shown groups of similar faces.\n\n"
                "For each group:\n"
                "- Enter a person's name to label all faces in the group\n"
                "- Type 'skip' to skip the current group\n"
                "- Close the dialog or press Cancel to end the session\n\n"
                "Press OK to begin."
            )
                
            # Cluster similar faces
            print("Clustering similar faces...")
            clusters = self.cluster_faces(tolerance)
            print(f"Found {len(clusters)} distinct face clusters")
            
            # Process each cluster
            for i, cluster in enumerate(clusters):
                if not cluster:
                    continue
                    
                print(f"Processing cluster {i+1}/{len(clusters)} with {len(cluster)} faces")
                
                # Show representative faces from this cluster
                faces_to_show = min(len(cluster), max_faces_per_prompt)
                sample_indices = cluster[:faces_to_show]
                
                # Create a composite image of sample faces
                composite = self._create_cluster_composite(sample_indices)
                
                # Show composite image
                cv2.imshow(f"Face Cluster #{i+1}", composite)
                cv2.waitKey(100)  # Short delay to ensure window shows up
                
                # Ask for name
                name = simpledialog.askstring("Label Face", 
                                            f"Enter name for these faces (Cluster #{i+1}) or 'skip' to skip:",
                                            parent=self._tk_root)
                
                cv2.destroyAllWindows()
                
                if not name or name.lower() == 'skip':
                    print(f"Skipping cluster #{i+1}")
                    continue
                    
                # Label all faces in this cluster
                for idx in cluster:
                    photo_path, face_encoding, face_location = self.face_database['unlabeled_faces'][idx]
                    
                    # Add to named faces
                    if name not in self.face_database['faces']:
                        self.face_database['faces'][name] = []
                    self.face_database['faces'][name].append(face_encoding)
                    
                    # Add to photo_faces
                    if photo_path not in self.face_database['photo_faces']:
                        self.face_database['photo_faces'][photo_path] = []
                    self.face_database['photo_faces'][photo_path].append((name, face_location))
                
                # Remove labeled faces from unlabeled (in reverse order to avoid index issues)
                for idx in sorted(cluster, reverse=True):
                    # Adjust index for any previous removals
                    adjusted_idx = idx
                    for removed_idx in cluster:
                        if removed_idx < idx and removed_idx in self.face_database['unlabeled_faces']:
                            adjusted_idx -= 1
                    
                    if adjusted_idx < len(self.face_database['unlabeled_faces']):
                        self.face_database['unlabeled_faces'].pop(adjusted_idx)
                
                # Save after each cluster
                self.save_database()
                
            print(f"Interactive labeling complete. {len(self.face_database['unlabeled_faces'])} faces remain unlabeled.")
            
            # Clean up
            if self._tk_root:
                self._tk_root.destroy()
                self._tk_root = None
            
    def _create_cluster_composite(self, face_indices, size=(150, 150), cols=3):
        """Create a composite image of multiple faces from a cluster"""
        faces = []
        
        for idx in face_indices:
            if idx >= len(self.face_database['unlabeled_faces']):
                continue
                
            photo_path, _, face_location = self.face_database['unlabeled_faces'][idx]
            full_path = self.photos_dir / photo_path
            
            if not full_path.exists():
                continue
                
            try:
                # Load image and extract face
                image = cv2.imread(str(full_path))
                if image is None:
                    continue
                    
                top, right, bottom, left = face_location
                face = image[top:bottom, left:right]
                
                # Resize to common size
                face = cv2.resize(face, size)
                faces.append(face)
                
            except Exception as e:
                print(f"Error extracting face: {e}")
        
        if not faces:
            # Return a blank image if no faces could be loaded
            return np.ones((size[1], size[0] * cols, 3), dtype=np.uint8) * 255
            
        # Calculate grid dimensions
        rows = (len(faces) + cols - 1) // cols
        
        # Create composite image
        composite = np.ones((size[1] * rows, size[0] * cols, 3), dtype=np.uint8) * 255
        
        for i, face in enumerate(faces):
            row = i // cols
            col = i % cols
            y_start = row * size[1]
            x_start = col * size[0]
            composite[y_start:y_start+size[1], x_start:x_start+size[0]] = face
            
        return composite

    def group_photos_by_person(self, output_dir):
        """
        Group photos by person and organize them in folders
        
        Args:
            output_dir (str): Directory to save organized photos
        """
        print(f"Grouping photos by person in {output_dir}...")
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Create mapping of people to photos
        person_photos = {}
        for photo_path, faces in self.face_database['photo_faces'].items():
            for name, _ in faces:
                if name not in person_photos:
                    person_photos[name] = []
                person_photos[name].append(photo_path)
        
        # Create person folders and copy photos
        for name, photos in person_photos.items():
            # Create folder for person
            person_dir = output_path / name
            person_dir.mkdir(exist_ok=True)
            
            print(f"Copying {len(photos)} photos of {name} to {person_dir}")
            
            # Copy each photo
            for i, photo_path in enumerate(photos):
                src_path = self.photos_dir / photo_path
                if not src_path.exists():
                    print(f"  Source photo not found: {src_path}")
                    continue
                    
                # Use a numbered filename to avoid conflicts
                extension = src_path.suffix
                dst_path = person_dir / f"{name}_{i+1}{extension}"
                
                try:
                    shutil.copy2(src_path, dst_path)
                except Exception as e:
                    print(f"  Error copying {src_path}: {e}")
                    
        print(f"Grouped photos for {len(person_photos)} people in {output_dir}")
        
        # Create an index.html file to make it easy to browse the photos
        self._create_group_index_html(output_path, person_photos)
        
    def _create_group_index_html(self, output_dir, person_photos):
        """Create an HTML index for browsing grouped photos"""
        html_path = output_dir / "index.html"
        
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>Face Recognition - People Index</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; }}
        h1 {{ color: #333; }}
        .person-grid {{ 
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 20px;
        }}
        .person-card {{
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 15px;
            text-align: center;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            transition: transform 0.2s;
        }}
        .person-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }}
        .person-card h2 {{
            margin-top: 0;
            color: #2c3e50;
        }}
        .photo-count {{
            color: #7f8c8d;
            margin-bottom: 10px;
        }}
    </style>
</head>
<body>
    <h1>Face Recognition - People Index</h1>
    <p>Click on a person to see all their photos</p>
    
    <div class="person-grid">
"""
        
        for name, photos in person_photos.items():
            html_content += f"""
        <a href="{name}/">
            <div class="person-card">
                <h2>{name}</h2>
                <div class="photo-count">{len(photos)} photos</div>
            </div>
        </a>
"""
        
        html_content += """
    </div>
</body>
</html>
"""
        
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_content)
            
        print(f"Created index page at {html_path}")
        
        # Create individual person pages
        for name, photos in person_photos.items():
            self._create_person_gallery(output_dir / name, name, photos)
    
    def _create_person_gallery(self, person_dir, name, photo_paths):
        """Create an HTML gallery for a specific person"""
        html_path = person_dir / "index.html"
        
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>Photos of {name}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; }}
        h1 {{ color: #333; }}
        .back-link {{ margin-bottom: 20px; }}
        .photo-grid {{ 
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 15px;
        }}
        .photo-card {{
            border: 1px solid #ddd;
            border-radius: 5px;
            overflow: hidden;
        }}
        .photo-card img {{
            width: 100%;
            height: auto;
            display: block;
        }}
        .photo-info {{
            padding: 10px;
            background-color: #f9f9f9;
        }}
    </style>
</head>
<body>
    <div class="back-link">
        <a href="../index.html">← Back to all people</a>
    </div>
    <h1>Photos of {name}</h1>
    
    <div class="photo-grid">
"""
        
        # List all files in person directory
        files = [f for f in person_dir.iterdir() if f.is_file() and f.suffix.lower() in ('.jpg', '.jpeg', '.png')]
        
        for photo_file in files:
            if photo_file.name == "index.html":
                continue
                
            rel_path = photo_file.name
            html_content += f"""
        <div class="photo-card">
            <img src="{rel_path}" alt="Photo of {name}">
            <div class="photo-info">
                {rel_path}
            </div>
        </div>
"""
        
        html_content += """
    </div>
</body>
</html>
"""
        
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_content)

def main():
    parser = argparse.ArgumentParser(description='Face Recognition File Explorer')
    parser.add_argument('--photos_dir', type=str, required=True, help='Directory with photos')
    parser.add_argument('--scan', action='store_true', help='Scan photos for faces')
    parser.add_argument('--force_rescan', action='store_true', help='Force rescan of already processed photos')
    parser.add_argument('--parallel', action='store_true', help='Use parallel processing for scanning')
    parser.add_argument('--model', type=str, choices=['hog', 'cnn'], default='hog', 
                       help='Face detection model (hog is faster, cnn is more accurate)')
    parser.add_argument('--label', type=int, help='Label a face by index')
    parser.add_argument('--name', type=str, help='Name for labeling a face')
    parser.add_argument('--show', type=int, help='Show an unlabeled face by index')
    parser.add_argument('--interactive', action='store_true', help='Interactive face labeling with GUI')
    parser.add_argument('--tolerance', type=float, default=0.6, help='Face matching tolerance (lower=stricter)')
    parser.add_argument('--recognize', action='store_true', help='Recognize faces in photos')
    parser.add_argument('--create_search', action='store_true', help='Create Windows search files')
    parser.add_argument('--output_dir', type=str, help='Output directory for copied photos with search properties')
    parser.add_argument('--visualize', action='store_true', help='Create visualizations of recognized faces')
    parser.add_argument('--export', action='store_true', help='Export face data to JSON')
    parser.add_argument('--group', action='store_true', help='Group photos by person name')
    
    args = parser.parse_args()
    
    explorer = FaceRecognitionExplorer(args.photos_dir)
    
    if args.scan:
        explorer.scan_photos(args.force_rescan, args.parallel, args.model)
    
    if args.show is not None:
        explorer.show_unlabeled_face(args.show)
    
    if args.interactive:
        explorer.interactive_labeling(args.tolerance)
    
    if args.label is not None and args.name:
        if explorer.label_face(args.label, args.name):
            print(f"Face #{args.label} labeled as '{args.name}'")
    
    if args.recognize:
        explorer.recognize_faces()
    
    if args.create_search:
        explorer.create_windows_search_files(args.output_dir)
        
    if args.group:
        output_dir = args.output_dir or os.path.join(str(explorer.photos_dir), "grouped")
        explorer.group_photos_by_person(output_dir)
        
    if args.visualize:
        output_dir = args.output_dir or "visualizations"
        explorer.visualize_faces(output_dir)
        
    if args.export:
        explorer.export_face_data()

if __name__ == "__main__":
    main()
