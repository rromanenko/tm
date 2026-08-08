import os
import platform
from PIL import Image
import pillow_avif  # This automatically enables AVIF support in Pillow

# --- Configuration ---
WINDOWS_BASE_DIR = r"C:\Downloads\jpg"
LINUX_BASE_DIR = os.path.expanduser("~/Pictures/")

IGNORED_EXTENSIONS = ["jpg", "jpeg", "mp4", "png", "mov"]
# ---------------------

def get_base_directory():
    """Returns the base directory configured for the current platform."""
    current_platform = platform.system()

    if current_platform == "Windows":
        return WINDOWS_BASE_DIR

    if current_platform == "Linux":
        return LINUX_BASE_DIR

    raise RuntimeError(
        f"Unsupported operating system: {current_platform}. "
        "Only Windows and Linux are supported."
    )

def convert_to_jpg(file_path):
    """Converts a supported image format to JPG and saves it in the same directory."""
    try:
        with Image.open(file_path) as img:
            # Convert to RGB because JPEG does not support transparency.
            rgb_img = img.convert("RGB")

            # Create the new filename by replacing the original extension with .jpg
            base_name = os.path.splitext(file_path)[0]
            new_file_path = f"{base_name}.jpg"

            # Save as JPEG
            rgb_img.save(new_file_path, "JPEG")

            # Get the original file extension for the log message
            original_format = os.path.splitext(file_path)[1].lstrip(".").upper()

            print(f"  [+] Successfully converted {original_format} to: {new_file_path}")

    except Exception as e:
        print(f"  [!] Error converting '{file_path}': {e}")

def scan_files(base_dir, ignored_exts):
    ignored_set = {ext.lower() for ext in ignored_exts}
    abs_base_dir = os.path.abspath(base_dir)
    
    if not os.path.isdir(abs_base_dir):
        print(f"Error: The directory '{abs_base_dir}' does not exist.")
        return

    for root, _, files in os.walk(abs_base_dir):
        for filename in files:
            _, ext = os.path.splitext(filename)
            ext_clean = ext.lstrip('.').lower()
            
            # Print and process files not in the ignore list
            if ext_clean not in ignored_set:
                full_path = os.path.join(root, filename)
                print(full_path)

            # Check for conversion triggers
            if ext_clean in {"webp", "avif", "jfif"}:
                convert_to_jpg(full_path)

if __name__ == "__main__":
    try:
        base_directory = get_base_directory()
        scan_files(base_directory, IGNORED_EXTENSIONS)
    except RuntimeError as error:
        print(f"Error: {error}")