# python
# move-image-to-created-timestamp-dir.py 
## Requirement:
###	Organize the original image files by categorizing them based on the year and month they were captured.
## Solution: 
###	move-image-to-created-timestamp-dir.py  
####	1. Reads all files within the specified source directory.
####	2. Extracts the EXIF metadata from each file, specifically the DateTimeOriginal field.
####	3. Creates a directory structure in the format YYYY/YYYY-MM based on the DateTimeOriginal value.
####	4. Moves the file to the corresponding directory within this structure.
####	5. If the DateTimeOriginal metadata is unavailable, lastmodified timestamp is used to move the file to a directory structured as YYYY/YYYY-MM/YYYY-MM-mtime
####	Inputs: source directory and destination directory
####	Instructions:
#####		Create a copy of the original directory and use this copy as the source directory to preserve the integrity of the original files.
#####		Provide a new and empty directory as the destination directory for the organized files.
