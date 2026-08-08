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

def convert_avif_to_jpg(file_path):
    """Converts an AVIF image to JPG and saves it in the same directory."""
    try:
        with Image.open(file_path) as img:
            # Convert to RGB to strip any transparency
            rgb_img = img.convert("RGB")

            base_name = os.path.splitext(file_path)[0]
            new_file_path = f"{base_name}.jpg"

            rgb_img.save(new_file_path, "JPEG")
            print(f"  [+] Successfully converted AVIF to: {new_file_path}")

    except Exception as e:
        print(f"  [!] Error converting AVIF '{file_path}': {e}")

def convert_jfif_to_jpg(file_path):
    """Converts a JFIF image to JPG and saves it in the same directory."""
    try:
        with Image.open(file_path) as img:
            # JPG uses RGB format.
            rgb_img = img.convert("RGB")

            # Create the new filename by replacing the extension
            base_name = os.path.splitext(file_path)[0]
            new_file_path = f"{base_name}.jpg"

            rgb_img.save(new_file_path, "JPEG")
            print(f"  [+] Successfully converted JFIF to: {new_file_path}")

    except Exception as e:
        print(f"  [-] Error converting JFIF file {file_path}: {e}")
        return None

def convert_webp_to_jpg(file_path):
    """Converts a WebP image to JPG and saves it in the same directory."""
    try:
        with Image.open(file_path) as img:
            # JPG does not support transparency (Alpha channel). 
            # We must convert the image to standard RGB.
            rgb_img = img.convert("RGB")
            
            # Create the new filename by replacing the extension
            base_name = os.path.splitext(file_path)[0]
            new_file_path = f"{base_name}.jpg"
            
            rgb_img.save(new_file_path, "JPEG")
            print(f"  [+] Successfully converted WEBP to: {new_file_path}")
            
    except Exception as e:
        print(f"  [!] Error converting WEBP '{file_path}': {e}")



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
                if ext_clean == "webp":
                    convert_webp_to_jpg(full_path)
                elif ext_clean == "avif":
                    convert_avif_to_jpg(full_path)
                elif ext_clean == "jfif":
                    convert_jfif_to_jpg(full_path)


if __name__ == "__main__":
    try:
        base_directory = get_base_directory()
        scan_files(base_directory, IGNORED_EXTENSIONS)
    except RuntimeError as error:
        print(f"Error: {error}")