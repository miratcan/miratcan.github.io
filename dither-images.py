#!/usr/bin/env python3
"""
Apply retro dithering effect to all images in build directory
"""
import os
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("Error: Pillow is required. Install with: pip install Pillow")
    sys.exit(1)


def dither_image(filepath, max_width=500, dark_color=(0, 0, 0), light_color=(178, 164, 151)):
    """Apply dithering to a single image with custom colors"""
    try:
        # Open image
        img = Image.open(filepath)

        # Resize if width > max_width while maintaining aspect ratio
        if img.width > max_width:
            aspect_ratio = img.height / img.width
            new_height = int(max_width * aspect_ratio)
            img = img.resize((max_width, new_height), Image.LANCZOS)

        # Convert to RGB if needed (handles RGBA, palette mode, etc)
        if img.mode not in ('RGB', 'L'):
            img = img.convert('RGB')

        # Convert to 1-bit (black & white with Floyd-Steinberg dithering)
        dithered_bw = img.convert('1', dither=Image.FLOYDSTEINBERG)

        # Create a new RGB image with custom colors
        # Map black (0) to dark_color and white (255) to light_color
        width, height = dithered_bw.size
        colored = Image.new('RGB', (width, height))
        pixels = colored.load()
        bw_pixels = dithered_bw.load()

        for y in range(height):
            for x in range(width):
                # 0 = black in 1-bit image, 255 = white
                if bw_pixels[x, y] == 0:
                    pixels[x, y] = dark_color
                else:
                    pixels[x, y] = light_color

        # Save as PNG for clean 2-color output (no JPEG artifacts)
        # Change extension to .png if needed
        original_filepath = filepath
        if filepath.lower().endswith(('.jpg', '.jpeg')):
            filepath = filepath.rsplit('.', 1)[0] + '.png'
            # Remove old JPEG file after converting to PNG
            if original_filepath != filepath and os.path.exists(original_filepath):
                os.remove(original_filepath)

        colored.save(filepath, 'PNG', optimize=True)
        return True
    except Exception as e:
        print(f"Warning: Could not dither {filepath}: {e}")
        return False


def process_directory(build_path):
    """Recursively find and dither all images"""
    image_extensions = ('.png', '.jpg', '.jpeg', '.gif')
    processed_count = 0
    skipped_count = 0

    for root, dirs, files in os.walk(build_path):
        for filename in files:
            if filename.lower().endswith(image_extensions):
                filepath = os.path.join(root, filename)
                if dither_image(filepath):
                    processed_count += 1
                else:
                    skipped_count += 1

    return processed_count, skipped_count


def fix_html_image_references(build_path):
    """Fix HTML files to reference .png instead of .jpg/.jpeg"""
    fixed_count = 0
    for root, dirs, files in os.walk(build_path):
        for filename in files:
            if filename.endswith('.html'):
                filepath = os.path.join(root, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # Replace .jpg and .jpeg with .png in image references
                    original_content = content
                    content = content.replace('.jpg"', '.png"')
                    content = content.replace('.jpeg"', '.png"')
                    content = content.replace('.jpg)', '.png)')
                    content = content.replace('.jpeg)', '.png)')

                    if content != original_content:
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(content)
                        fixed_count += 1
                except Exception as e:
                    print(f"Warning: Could not fix HTML references in {filepath}: {e}")

    return fixed_count


if __name__ == '__main__':
    build_path = sys.argv[1] if len(sys.argv) > 1 else 'build'

    if not os.path.exists(build_path):
        print(f"Error: Build directory '{build_path}' does not exist")
        sys.exit(1)

    print(f"Dithering images in {build_path}...")
    processed, skipped = process_directory(build_path)
    print(f"✓ Dithered {processed} images")
    if skipped > 0:
        print(f"⚠ Skipped {skipped} images due to errors")

    # Fix HTML references to point to .png files
    print("Fixing HTML image references...")
    fixed = fix_html_image_references(build_path)
    print(f"✓ Fixed {fixed} HTML files")
