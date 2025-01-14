import os

def rename_files_sequentially(directory):
    """
    Rename all files in the given directory to 1, 2, ..., n, maintaining their extensions.
    :param directory: Path to the folder containing the files to be renamed.
    """
    try:
        # Get a list of all files in the directory
        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        # print(files)
    #     # Sort files to ensure renaming in a consistent order
    #     files.sort()
        
    #     # Rename files
        for i, filename in enumerate(files, start=1):
            # Extract file extension
            extension = os.path.splitext(filename)[1]
            
            # Construct new filename
            new_name = f"{i}{extension}"
            print(new_name)
            # Rename file
            os.rename(os.path.join(directory, filename), os.path.join(directory, new_name))
        
        print(f"Successfully renamed {len(files)} files.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Directory containing files to rename
directory_path = input("Enter the path to the directory: ")

# Call the function
rename_files_sequentially(directory_path)
