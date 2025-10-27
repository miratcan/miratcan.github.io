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


def dither_image(filepath):
    """Apply dithering to a single image"""
    try:
        # Open image
        img = Image.open(filepath)

        # Convert to RGB if needed (handles RGBA, palette mode, etc)
        if img.mode not in ('RGB', 'L'):
            img = img.convert('RGB')

        # Convert to 1-bit (black & white with Floyd-Steinberg dithering)
        dithered = img.convert('1', dither=Image.FLOYDSTEINBERG)

        # Save back to same file
        dithered.save(filepath, optimize=True)
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
