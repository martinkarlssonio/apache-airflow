#!/bin/bash
### This script removes all files and subfolders, good during development!

# Directories to clean
directories=("config" "data" "logs" "plugins")

# Loop through each directory
for dir in "${directories[@]}"; do
    # Check if directory exists
    if [ -d "$dir" ]; then
        echo "Cleaning directory: $dir"
        # Find and delete all files excluding .keepme
        find "$dir" -type f ! -name '.keepme' -exec echo Deleting file: {} \; -exec rm {} \;
        # Find and delete all directories except the root directories
        find "$dir" -mindepth 1 -type d -exec echo Deleting directory: {} \; -exec rm -r {} \;
    else
        echo "Directory does not exist: $dir"
    fi
done

echo "Cleanup complete."
