import os

# Define the folder path
folder_path = "C:/Work/NVK48/สบน/ลูกจ้างชั่วคราว"  # Update this with the actual path to your folder

# Loop through the files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".jpg"):
        # Extract the numeric part of the filename
        numeric_part = filename.split(".")[0]
        numeric_part = numeric_part.zfill(4)  # Ensure it has 4 digits with leading zeros

        # Rename the file with "MA" prefix
        new_filename = f"PDMO{numeric_part}.jpg"
        
        # Construct the full old and new file paths
        old_filepath = os.path.join(folder_path, filename)
        new_filepath = os.path.join(folder_path, new_filename)
        
        # Rename the file
        os.rename(old_filepath, new_filepath)
        print(f"Renamed: {old_filepath} to {new_filepath}")
