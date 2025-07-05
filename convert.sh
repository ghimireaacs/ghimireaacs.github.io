#!/bin/bash

# README: This script converts all PNG and JPG files in the 'assets' directory to WebP format.
# It skips files in the 'favicon' subdirectory and deletes the original files after conversion.
# Run from the root of the project.

#!/bin/bash

# Navigate to the parent directory of your 'assets' folder before running this script.

find assets -type f \( -iname "*.png" -o -iname "*.jpg" \) \
    -not -path "assets/img/favicons/*" \
    -print0 | while IFS= read -r -d $'\0' file; do
    # Get the directory of the file
    dir=$(dirname "$file")
    # Get the filename without its extension
    base_name=$(basename "$file")
    base_name="${base_name%.*}" # Remove extension

    # Define the output WebP path
    output_webp="$dir/$base_name.webp"

    # Ensure the output directory exists
    mkdir -p "$dir"

    echo "Processing: $file -> $output_webp"

    # Convert the file and check for success, including metadata transfer
    if cwebp -metadata all "$file" -o "$output_webp"; then
        echo "Successfully converted '$file' to '${base_name}.webp' (metadata included). Deleting original."
        rm "$file"
    else
        echo "Failed to convert '$file'. Keeping original."
    fi
done