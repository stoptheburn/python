#!/opt/homebrew/bin/python3.11
"""
Developer: 		RS
Date Created: 		2012-01-01
Date Modified: 		2024-12-06
libraries installed: 	pillow, pillow_heif, datetime, argparse
Problem Statement:   	When I backup all the picutres from my phone onto my hdd, they are all placed in the same directory
			The photo app on Samsung TV has difficulty listing 20,000+ picutres in a given directory.
			It makes sense to create directories with smaller no. of pic files
Imputs:			Source Directory         	
       			Destination Directory         	
Example arguments:	python3 move-image-to-created-timestamp-dir.py --srv <src_dir> --dest <dest_dir> [ --debug True ]
Description:         	The script reads the metadata of each image & movie files from the source directory
			Grabs the DateTimeOriginal value from EXIF meta data.
			If this info is not available, grabs the last modified timestamps of the file
			Based on the timestamp, it creates directories in the following format
			YYYY/YYYY-MM and moves all the media files from the source dir underneath the destination directory
"""
import argparse
import os, time, platform
import shutil
from PIL import Image
from pillow_heif import register_heif_opener
from datetime import datetime

debug = False

def DEBUG(mystr):
    if debug:
        print("DEBUG: " + mystr )

# Register HEIC format support
register_heif_opener()

# Returns created data in YYYY-MM format
def get_mtime_from_os(image_path):
    try:
        created = os.path.getmtime(image_path)
        year,month,day,hour,minute,second = time.localtime(created)[:-3] # why this last but 3 ?
        mymtime =  ("%04d-%02d"%(year,month))
        DEBUG("get_mtime_from_os(): Returning: " + mymtime ) 
        return mymtime
    except Exception as e:
        print(f"Error reading EXIF from {image_path}: {e}")

def get_date_from_exif(image_path):
    try:
        image = Image.open(image_path)
    except Exception as e:
        print(f"Error reading EXIF from {image_path}: {e}")

    try:
        exif_data = image._getexif()
    except Exception as e:
        print(f"\t\t\t" + image_path + ": Trying 'getexif()' instead")
        exif_data = image.getexif()

    try:
        if exif_data:
            date_taken = exif_data.get(36867)  # DateTimeOriginal tag
            if date_taken:
                return datetime.strptime(date_taken, "%Y:%m:%d %H:%M:%S")
            date_taken = exif_data.get(306)  # DateTime tag
            if date_taken:
                print(f"INFO: " + image_path + ": Found DateTime Instead")
                return datetime.strptime(date_taken, "%Y:%m:%d %H:%M:%S")
    except Exception as e:
        print(f"Error reading EXIF from {image_path}: {e}")

    return None

def move_image_from_src_to_dest_hash_dir(target_dir, file_path, file_name ):
    try:
        # Create directory for Year-Month
        os.makedirs(target_dir, exist_ok=True)

        # Move file to target directory
        shutil.move(file_path, os.path.join(target_dir, file_name))
        print(f"Moved {file_name} to {target_dir}")
    except Exception as e:
        print(f"Error processing {file_name}: {e}")

def organize_images_by_date(source_dir, dest_dir):
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    for file_name in os.listdir(source_dir):
        file_path = os.path.join(source_dir, file_name)
        if os.path.isfile(file_path):
            try:
                date_taken = get_date_from_exif(file_path)
                if date_taken:
                    ## Convert data_taken into YYYY-MM format
                    target_dir = os.path.join(dest_dir, f"{date_taken.year}", f"{date_taken.year}-{date_taken.month:02d}")

                    ## Create directory for Year-Month and move image file there
                    move_image_from_src_to_dest_hash_dir(target_dir, file_path, file_name )
                else:
                    # Try to process image files that don't have DateTime or DateTimeOriginal flags. Use os timestamp
                    print(f"No date found for {file_name}, switching to OS create time.")
                    hash_dir = get_mtime_from_os(file_path)
                    #target_dir = os.path.join(dest_dir, f"{hash_dir[:4]}", f"{hash_dir}", ('/' + hash_dir + '-mtime'))
                    target_dir = os.path.join(dest_dir + '/' + hash_dir[:4] + '/' + hash_dir + '/' + hash_dir + '-mtime' )
                    move_image_from_src_to_dest_hash_dir(target_dir, file_path, file_name )
            except Exception as e:
                print(f"Error processing {file_name}: {e}")
                try:
                    # Try to process mov, mp4 files
                    hash_dir = get_mtime_from_os(file_path)
                    #target_dir = os.path.join(dest_dir, f"{hash_dir[:4]}", f"{hash_dir}", ('/' + hash_dir + '-mtime'))
                    target_dir = os.path.join(dest_dir + '/' + hash_dir[:4] + '/' + hash_dir + '/' + hash_dir + '-mtime' )
                    move_image_from_src_to_dest_hash_dir(target_dir, file_path, file_name )
                except Exception as e:
                    print(f"Error processing {file_name}: {e}")

def make_parser():
    parser = argparse.ArgumentParser(description='Parse Jpeg Metadata and hash img files.')
    parser.add_argument('-s', '--src', help='Give result path. E.g. $HOME/Documents/Pictures/src')
    parser.add_argument('-d', '--dest', help='Give result path. E.g. $HOME/Documents/Pictures/dest')
    parser.add_argument('-D', '--debug', action='store_true', help='Enable debug mode')
    return parser

def main():
    global debug
    parser = make_parser()
    arguments = parser.parse_args()
    print(arguments)
    if not arguments.src:
        parser.print_help()
        return
    elif not arguments.dest:
        parser.print_help()
        return
    else:
        src_dir = arguments.src
        dest_dir = arguments.dest
        if arguments.debug:
            debug = True

    try:
        DEBUG("main():  Src Dir: " + arguments.src  ) 
        DEBUG("main(): Dest Dir: " + arguments.dest ) 

        # Replace with your source and destination directories
        source_directory = arguments.src
        destination_directory = arguments.dest

        organize_images_by_date(source_directory, destination_directory)

    except Exception as e:
       return f"An error occurred: {e}"

if __name__ == '__main__':
    main()


