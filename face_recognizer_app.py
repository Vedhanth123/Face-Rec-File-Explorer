import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import subprocess
import threading
import sys
import webbrowser
from pathlib import Path
import cv2

# Import the FaceRecognitionExplorer class directly for better integration
try:
    from face_recognition_explorer import FaceRecognitionExplorer
    DIRECT_IMPORT_SUCCESS = True
except ImportError:
    # Fallback to subprocess if import fails
    DIRECT_IMPORT_SUCCESS = False
    print("Warning: Could not directly import FaceRecognitionExplorer class.")
    print("Will use subprocess method instead.")

class FaceRecognizerApp:
    def __init__(self, master):
        self.master = master
        master.title("Face Recognition Photo Organizer")
        master.geometry("800x600")
        master.configure(bg="#f5f5f5")
        
        # Default directories
        self.photos_dir = ""
        self.output_dir = ""
        
        # Create an instance of the FaceRecognitionExplorer if available
        self.explorer = None
        
        # Set up the UI
        self.setup_ui()
    
    def create_explorer_instance(self):
        """Create or update the FaceRecognitionExplorer instance"""
        if not DIRECT_IMPORT_SUCCESS:
            return False
            
        try:
            photos_dir = self.photos_dir_var.get()
            if not photos_dir:
                return False
                
            if not self.explorer:
                self.explorer = FaceRecognitionExplorer(photos_dir)
            elif str(self.explorer.photos_dir) != photos_dir:
                self.explorer = FaceRecognitionExplorer(photos_dir)
                
            return True
        except Exception as e:
            print(f"Error creating FaceRecognitionExplorer instance: {e}")
            return False
    
    def setup_ui(self):
        # Create main frame
        main_frame = tk.Frame(self.master, bg="#f5f5f5", padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = tk.Label(
            main_frame, 
            text="Face Recognition Photo Organizer", 
            font=("Helvetica", 18, "bold"),
            bg="#f5f5f5", 
            fg="#333333"
        )
        title_label.pack(pady=(0, 20))
        
        # Input directory frame
        input_frame = tk.LabelFrame(main_frame, text="Photo Directory", padx=10, pady=10, bg="#f5f5f5")
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.photos_dir_var = tk.StringVar()
        photos_dir_entry = tk.Entry(input_frame, textvariable=self.photos_dir_var, width=50)
        photos_dir_entry.pack(side=tk.LEFT, padx=(0, 10), fill=tk.X, expand=True)
        
        browse_btn = tk.Button(input_frame, text="Browse", command=self.browse_photos_dir)
        browse_btn.pack(side=tk.RIGHT)
        
        # Output directory frame
        output_frame = tk.LabelFrame(main_frame, text="Output Directory (Optional)", padx=10, pady=10, bg="#f5f5f5")
        output_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.output_dir_var = tk.StringVar()
        output_dir_entry = tk.Entry(output_frame, textvariable=self.output_dir_var, width=50)
        output_dir_entry.pack(side=tk.LEFT, padx=(0, 10), fill=tk.X, expand=True)
        
        browse_out_btn = tk.Button(output_frame, text="Browse", command=self.browse_output_dir)
        browse_out_btn.pack(side=tk.RIGHT)
        
        # Options frame
        options_frame = tk.LabelFrame(main_frame, text="Processing Options", padx=10, pady=10, bg="#f5f5f5")
        options_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Face detection model
        model_frame = tk.Frame(options_frame, bg="#f5f5f5")
        model_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(model_frame, text="Face Detection Model:", bg="#f5f5f5").pack(side=tk.LEFT)
        
        self.model_var = tk.StringVar(value="hog")
        tk.Radiobutton(model_frame, text="HOG (Fast)", variable=self.model_var, value="hog", bg="#f5f5f5").pack(side=tk.LEFT, padx=(10, 5))
        tk.Radiobutton(model_frame, text="CNN (Accurate)", variable=self.model_var, value="cnn", bg="#f5f5f5").pack(side=tk.LEFT)
        
        # Parallel processing
        self.parallel_var = tk.BooleanVar(value=True)
        tk.Checkbutton(options_frame, text="Use parallel processing (faster but uses more memory)", 
                      variable=self.parallel_var, bg="#f5f5f5").pack(anchor=tk.W, pady=5)
        
        # Force rescan
        self.rescan_var = tk.BooleanVar(value=False)
        tk.Checkbutton(options_frame, text="Force rescan of already processed photos", 
                      variable=self.rescan_var, bg="#f5f5f5").pack(anchor=tk.W, pady=5)
        
        # Face matching tolerance
        tolerance_frame = tk.Frame(options_frame, bg="#f5f5f5")
        tolerance_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(tolerance_frame, text="Face Matching Tolerance:", bg="#f5f5f5").pack(side=tk.LEFT)
        
        self.tolerance_var = tk.DoubleVar(value=0.6)
        tolerance_scale = tk.Scale(tolerance_frame, from_=0.4, to=0.8, resolution=0.05, 
                                  orient=tk.HORIZONTAL, variable=self.tolerance_var, 
                                  length=200, bg="#f5f5f5")
        tolerance_scale.pack(side=tk.LEFT, padx=(10, 5), fill=tk.X, expand=True)
        
        tk.Label(tolerance_frame, text="Lower = Stricter", bg="#f5f5f5", fg="#666666").pack(side=tk.LEFT)
        
        # Steps frame
        steps_frame = tk.LabelFrame(main_frame, text="Processing Steps", padx=10, pady=10, bg="#f5f5f5")
        steps_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Step buttons with descriptions
        steps = [
            ("1. Scan Photos", "Scan all photos for faces", self.scan_photos),
            ("2. Label Faces", "Interactively identify people in photos", self.interactive_labeling),
            ("3. Recognize Faces", "Find all photos of each person", self.recognize_faces),
            ("4. Group Photos", "Organize photos by person", self.group_photos),
            ("5. Browse Results", "Open the generated gallery in browser", self.browse_gallery)
        ]
        
        for i, (title, desc, command) in enumerate(steps):
            step_frame = tk.Frame(steps_frame, bg="#f5f5f5")
            step_frame.pack(fill=tk.X, pady=(0, 5))
            
            step_btn = tk.Button(step_frame, text=title, command=command, width=20)
            step_btn.pack(side=tk.LEFT)
            
            step_desc = tk.Label(step_frame, text=desc, bg="#f5f5f5", fg="#333333")
            step_desc.pack(side=tk.LEFT, padx=(10, 0))
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = tk.Label(main_frame, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def browse_photos_dir(self):
        directory = filedialog.askdirectory(title="Select Photos Directory")
        if directory:
            self.photos_dir = directory
            self.photos_dir_var.set(directory)
    
    def browse_output_dir(self):
        directory = filedialog.askdirectory(title="Select Output Directory")
        if directory:
            self.output_dir = directory
            self.output_dir_var.set(directory)
    
    def validate_inputs(self):
        photos_dir = self.photos_dir_var.get()
        if not photos_dir:
            messagebox.showerror("Error", "Please select a photos directory.")
            return False
        
        if not os.path.isdir(photos_dir):
            messagebox.showerror("Error", "The selected photos directory does not exist.")
            return False
        
        output_dir = self.output_dir_var.get()
        if output_dir and not os.path.isdir(output_dir):
            try:
                os.makedirs(output_dir, exist_ok=True)
            except Exception as e:
                messagebox.showerror("Error", f"Could not create output directory: {e}")
                return False
        
        return True
    
    def run_command(self, command, callback=None):
        if not self.validate_inputs():
            return
        
        photos_dir = self.photos_dir_var.get()
        output_dir = self.output_dir_var.get()
        
        # Use the virtual environment's Python if available
        python_path = "python"
        if os.path.exists(os.path.join("FaceRec", "Scripts", "python.exe")):
            python_path = os.path.join("FaceRec", "Scripts", "python.exe")
        
        cmd = [python_path, "face_recognition_explorer.py", "--photos_dir", photos_dir]
        
        # Add the specific command
        cmd.extend(command)
        
        # Add output directory if provided
        if output_dir:
            cmd.extend(["--output_dir", output_dir])
        
        # Update status
        self.status_var.set(f"Running: {' '.join(cmd)}")
        self.master.update()
        
        # Run the process
        def run_process():
            process = subprocess.Popen(
                cmd, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            # Read output in real-time
            for line in iter(process.stdout.readline, ''):
                print(line, end='')  # Print to console
                self.status_var.set(line.strip())
                self.master.update_idletasks()
            
            process.stdout.close()
            return_code = process.wait()
            
            if return_code == 0:
                self.status_var.set("Command completed successfully")
            else:
                self.status_var.set(f"Command failed with return code {return_code}")
            
            if callback:
                callback()
        
        # Run in a separate thread to not block the GUI
        thread = threading.Thread(target=run_process)
        thread.daemon = True
        thread.start()
    
    def scan_photos(self):
        if self.create_explorer_instance():
            try:
                # Direct integration mode
                self.status_var.set("Scanning photos for faces...")
                self.master.update()
                
                model = self.model_var.get()
                parallel = self.parallel_var.get()
                force_rescan = self.rescan_var.get()
                
                # Run in a separate thread to avoid freezing the UI
                def run_scan():
                    try:
                        self.explorer.scan_photos(force_rescan=force_rescan, parallel=parallel, model=model)
                        self.status_var.set("Scan completed successfully")
                    except Exception as e:
                        self.status_var.set(f"Error during scan: {e}")
                
                thread = threading.Thread(target=run_scan)
                thread.daemon = True
                thread.start()
            except Exception as e:
                self.status_var.set(f"Error: {e}")
                # Fallback to subprocess
                self.use_subprocess_scan()
        else:
            # Use subprocess method
            self.use_subprocess_scan()
    
    def use_subprocess_scan(self):
        model = self.model_var.get()
        parallel = "--parallel" if self.parallel_var.get() else ""
        force_rescan = "--force_rescan" if self.rescan_var.get() else ""
        
        command = ["--scan", "--model", model]
        if parallel:
            command.append(parallel)
        if force_rescan:
            command.append(force_rescan)
        
        self.run_command(command)
    
    def interactive_labeling(self):
        if self.create_explorer_instance():
            try:
                # Direct integration mode
                self.status_var.set("Starting interactive face labeling...")
                self.master.update()
                
                tolerance = float(self.tolerance_var.get())
                
                # Run in a separate thread
                def run_labeling():
                    try:
                        self.explorer.interactive_labeling(tolerance=tolerance)
                        self.status_var.set("Interactive labeling completed")
                    except Exception as e:
                        self.status_var.set(f"Error during labeling: {e}")
                
                thread = threading.Thread(target=run_labeling)
                thread.daemon = True
                thread.start()
            except Exception as e:
                self.status_var.set(f"Error: {e}")
                # Fallback to subprocess
                tolerance = self.tolerance_var.get()
                command = ["--interactive", "--tolerance", str(tolerance)]
                self.run_command(command)
        else:
            # Use subprocess method
            tolerance = self.tolerance_var.get()
            command = ["--interactive", "--tolerance", str(tolerance)]
            self.run_command(command)
    
    def recognize_faces(self):
        if self.create_explorer_instance():
            try:
                # Direct integration mode
                self.status_var.set("Recognizing faces in photos...")
                self.master.update()
                
                # Run in a separate thread
                def run_recognition():
                    try:
                        self.explorer.recognize_faces()
                        self.status_var.set("Recognition completed successfully")
                    except Exception as e:
                        self.status_var.set(f"Error during recognition: {e}")
                
                thread = threading.Thread(target=run_recognition)
                thread.daemon = True
                thread.start()
            except Exception as e:
                self.status_var.set(f"Error: {e}")
                # Fallback to subprocess
                command = ["--recognize"]
                self.run_command(command)
        else:
            # Use subprocess method
            command = ["--recognize"]
            self.run_command(command)
    
    def group_photos(self):
        if self.create_explorer_instance():
            try:
                # Direct integration mode
                output_dir = self.output_dir_var.get()
                if not output_dir:
                    output_dir = os.path.join(str(self.explorer.photos_dir), "grouped")
                
                self.status_var.set(f"Grouping photos by person in {output_dir}...")
                self.master.update()
                
                # Run in a separate thread
                def run_grouping():
                    try:
                        self.explorer.group_photos_by_person(output_dir)
                        self.status_var.set("Grouping completed successfully")
                        self.check_gallery()
                    except Exception as e:
                        self.status_var.set(f"Error during grouping: {e}")
                
                thread = threading.Thread(target=run_grouping)
                thread.daemon = True
                thread.start()
            except Exception as e:
                self.status_var.set(f"Error: {e}")
                # Fallback to subprocess
                command = ["--group"]
                self.run_command(command, self.check_gallery)
        else:
            # Use subprocess method
            command = ["--group"]
            self.run_command(command, self.check_gallery)
    
    def check_gallery(self):
        """Check if gallery exists and offer to open it"""
        output_dir = self.output_dir_var.get()
        if not output_dir:
            output_dir = os.path.join(self.photos_dir_var.get(), "grouped")
        
        html_path = os.path.join(output_dir, "index.html")
        if os.path.exists(html_path):
            if messagebox.askyesno("Gallery Created", 
                                 "Photo gallery has been created. Would you like to open it now?"):
                self.browse_gallery()
    
    def browse_gallery(self):
        """Open the generated gallery in the default web browser"""
        output_dir = self.output_dir_var.get()
        if not output_dir:
            output_dir = os.path.join(self.photos_dir_var.get(), "grouped")
        
        html_path = os.path.join(output_dir, "index.html")
        if os.path.exists(html_path):
            webbrowser.open(f"file://{os.path.abspath(html_path)}")
        else:
            messagebox.showerror("Error", 
                               "Gallery not found. Please run 'Group Photos' first.")


def main():
    root = tk.Tk()
    app = FaceRecognizerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
