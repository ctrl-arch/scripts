import os

# -------------- USER CONFIGURATION ------------------

# Full path to the folder containing the files you want to rename
folder_path = r"D:\path\to\your\source\folder"  # <- Update this to your actual folder path

# Define the replacement rules (old_text, new_text)
# These are applied in the order listed
replacements = [
    ("Apple", "Orange"),
    ("Orange", "Apple")
]

# ----------------------------------------------------

# Loop through each item in the folder
for filename in os.listdir(folder_path):
    # Skip subfolders — only rename files
    if not os.path.isfile(os.path.join(folder_path, filename)):
        continue

    new_filename = filename

    # Apply all replacement rules to the current filename
    for old_str, new_str in replacements:
        new_filename = new_filename.replace(old_str, new_str)

    # Rename the file only if a change occurred
    if new_filename != filename:
        old_path = os.path.join(folder_path, filename)
        new_path = os.path.join(folder_path, new_filename)
        os.rename(old_path, new_path)
        print(f"Renamed: {filename} → {new_filename}")
