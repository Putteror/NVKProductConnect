import os

# Specify the directory where your images are located
image_directory = "C:/Users/putter/Downloads/8000 edit"

# Get a list of all files in the directory
file_list = os.listdir(image_directory)

# Iterate over each file in the directory
for file_name in file_list:
    # Check if the file has a .JPG extension
    if file_name.endswith(".JPG"):
        # Generate the new file name by replacing .JPG with .jpg
        new_file_name = file_name.replace(".JPG", ".jpg")
        
        # Construct the full paths for the old and new files
        old_file_path = os.path.join(image_directory, file_name)
        new_file_path = os.path.join(image_directory, new_file_name)
        
        # Rename the file
        os.rename(old_file_path, new_file_path)
