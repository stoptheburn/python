# python
Repo for some of my python scripts 
#move-image-to-created-timestamp-dir.py - This python script 
##Requirement:
###	Organize the original image files by categorizing them based on the year and month they were captured.
##Solution: 
###	move-image-to-created-timestamp-dir.py  
####	Reads all files in a given directory. Reads the EXIF metadata, created the directory YYYY/YYYY-MM based on dateTimeOriginal field and moves file underneath this directory. 
####	If the DateTimeOriginal metadata is unavailable, the file is moved to a directory structured as YYYY/YYYY-MM/YYYY-MM-mtime
####	Inputs: source directory and destination directory
####	Instructions:
#####		Create a copy of the original directory and use this copy as the source directory to preserve the integrity of the original files.
#####		Provide a new and empty directory as the destination directory for the organized files.
