import os
import shutil


def static_to_public():
	if os.path.exists("docs"):
		shutil.rmtree("docs")
	merge_directories("static", "docs")public

def merge_directories(source_dir, target_dir):
    """
    Recursively copies all contents from source_dir into target_dir.
    If target_dir does not exist, it will be created.
    If a file already exists in target_dir, it will be overwritten.
    """

    # Ensure the target directory exists
    os.makedirs(target_dir, exist_ok=True)

    # Loop through all files and folders in the source directory
    for item in os.listdir(source_dir):
        source_path = os.path.join(source_dir, item)
        target_path = os.path.join(target_dir, item)

        if os.path.isdir(source_path):
            # If it's a subfolder, recursively call this function to merge it
            merge_directories(source_path, target_path)
        else:
            # If it's a file, copy it over (preserves metadata with copy2)
            shutil.copy2(source_path, target_path)

# --- Example Usage ---
# merge_directories("path/to/source", "path/to/destination")
