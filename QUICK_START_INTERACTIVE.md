# Quick Start Guide - Interactive Photo Grouping

This guide focuses on the key feature you requested: **grouping photos by faces with interactive naming**.

## Getting Started in 5 Minutes

1. **Launch the application**

   - Double-click `launch_gui.bat`

2. **Select your photos folder**

   - Click "Browse" and choose the folder containing your photos
   - (Optional) Set an output location for organized photos

3. **Scan for faces**

   - Click "Scan Photos" to analyze all photos
   - Wait for the scan to complete

4. **Name people interactively**

   - Click "Label Faces"
   - You'll see groups of similar faces
   - Type a name for each group when prompted
   - Type "skip" to skip any group you're not sure about

5. **Organize photos by person**

   - Click "Group Photos"
   - Photos will be organized into folders by person name
   - An HTML gallery will be created

6. **Browse your organized collection**
   - Click "Browse Results" to open the gallery
   - Click on a person to see all their photos

## Example Workflow

Let's say you have a folder with 500 vacation photos containing family and friends:

1. **Scan the photos**
   - System finds 1,200 faces across all photos
2. **Interactive labeling**
   - System shows you a group of 15 similar faces
   - You type "John" to label all of them
   - System shows another group
   - You type "Sarah"
   - Continue until all major groups are labeled
3. **Recognize all faces**
   - System uses your labels to identify people in all photos
   - Any new faces will be grouped for future labeling
4. **Group and browse**
   - Photos are organized by person
   - You can now easily find all photos of each person

## When New Photos Are Added

1. Run the application again
2. Scan only for new photos (uncheck "Force rescan")
3. Label any new faces that appear
4. Re-run recognition and grouping

## Tips for Best Results

- **Good lighting**: Face detection works best with well-lit photos
- **Face visibility**: The face should be clearly visible
- **Multiple examples**: Label multiple examples of each person
- **Similar faces**: If someone looks very different in different photos (e.g., with/without glasses), label examples of both looks
