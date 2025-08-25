# File Renamer Utility

A simple Python script to **rename multiple files in bulk** using defined string replacements. This is useful for reorganizing datasets, normalizing naming conventions, or swapping terms in file names (e.g., "Apple" ↔ "Orange").

---

## What It Does

- Loops through all files in a specified folder  
- Applies a list of text replacements to file names  
- Renames the files accordingly  
- Prints the old and new names for easy tracking  

---

## What’s Getting Swapped

Here's how it works:

- If a filename contains `"Apple"`, that part will be changed to `"Orange"`.  
- If a filename contains `"Orange"`, that part will be changed to `"Apple"`.

---

## How to Use

1. **Edit the Script:**

   - Set the `folder_path` variable to your target folder path  
   - Update the `replacements` list with your own string pairs to replace  

2. **Run the Script:**

   ```bash
   python rename_files.py
