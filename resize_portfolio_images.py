#!/usr/bin/env python3
"""
Portfolio Image Resizer Script - Dual Version
Creates both preview (800x600) and slider (1200x800) versions of each image.

Preview images: 800x600px (4:3 ratio) - for portfolio grid
Slider images: 1200x800px (3:2 ratio) - for project detail pages
"""

import os
import sys
from PIL import Image
import argparse

def resize_image(input_path, output_path, target_size, quality=85, crop_mode=True):
    """
    Resize an image to target size with smart cropping.
    
    Args:
        input_path: Path to input image
        output_path: Path to output image
        target_size: Tuple of (width, height)
        quality: JPEG quality (1-100)
        crop_mode: If True, crop to fill. If False, add white padding.
    """
    try:
        with Image.open(input_path) as img:
            # Convert to RGB if necessary
            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGB')
            
            if crop_mode:
                # Smart cropping approach - resize then crop to fill
                img_ratio = img.width / img.height
                target_ratio = target_size[0] / target_size[1]
                
                if img_ratio > target_ratio:
                    # Image is wider than target - crop width
                    new_height = target_size[1]
                    new_width = int(target_size[1] * img_ratio)
                    resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                    
                    # Crop from center
                    left = (new_width - target_size[0]) // 2
                    top = 0
                    right = left + target_size[0]
                    bottom = target_size[1]
                    
                    final_img = resized.crop((left, top, right, bottom))
                else:
                    # Image is taller than target - crop height
                    new_width = target_size[0]
                    new_height = int(target_size[0] / img_ratio)
                    resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                    
                    # Crop from center
                    left = 0
                    top = (new_height - target_size[1]) // 2
                    right = target_size[0]
                    bottom = top + target_size[1]
                    
                    final_img = resized.crop((left, top, right, bottom))
            else:
                # Original padding approach
                img_ratio = img.width / img.height
                target_ratio = target_size[0] / target_size[1]
                
                # Resize maintaining aspect ratio
                if img_ratio > target_ratio:
                    # Image is wider than target
                    new_width = target_size[0]
                    new_height = int(target_size[0] / img_ratio)
                else:
                    # Image is taller than target
                    new_height = target_size[1]
                    new_width = int(target_size[1] * img_ratio)
                
                # Resize image
                resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # Create new image with target size and paste resized image
                final_img = Image.new('RGB', target_size, (255, 255, 255))
                
                # Calculate position to center the image
                x_offset = (target_size[0] - new_width) // 2
                y_offset = (target_size[1] - new_height) // 2
                
                final_img.paste(resized_img, (x_offset, y_offset))
            
            # Save with appropriate format
            if output_path.lower().endswith('.jpg') or output_path.lower().endswith('.jpeg'):
                final_img.save(output_path, 'JPEG', quality=quality, optimize=True)
            else:
                final_img.save(output_path, 'PNG', optimize=True)
            
            print(f"✓ Resized {input_path} to {target_size[0]}x{target_size[1]} -> {output_path}")
            
    except Exception as e:
        print(f"✗ Error processing {input_path}: {str(e)}")

def process_portfolio_images(portfolio_dir, backup=True):
    """
    Process all images in the portfolio directory.
    Creates both preview and slider versions for each image.
    
    Args:
        portfolio_dir: Path to portfolio images directory
        backup: Whether to create backup of original images
    """
    # Define target sizes
    preview_size = (800, 600)    # 4:3 ratio for grid preview
    slider_size = (1200, 800)    # 3:2 ratio for slider
    
    # Create backup directory if requested
    if backup:
        backup_dir = os.path.join(portfolio_dir, 'backup_original')
        os.makedirs(backup_dir, exist_ok=True)
        print(f"Backup directory created: {backup_dir}")
    
    # Create subdirectories for organized output
    preview_dir = os.path.join(portfolio_dir, 'preview')
    slider_dir = os.path.join(portfolio_dir, 'slider')
    os.makedirs(preview_dir, exist_ok=True)
    os.makedirs(slider_dir, exist_ok=True)
    print(f"Preview directory: {preview_dir}")
    print(f"Slider directory: {slider_dir}")
    
    # Supported image extensions
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp'}
    
    # Process each image
    for filename in os.listdir(portfolio_dir):
        if not os.path.isfile(os.path.join(portfolio_dir, filename)):
            continue
            
        file_ext = os.path.splitext(filename)[1].lower()
        if file_ext not in image_extensions:
            continue
        
        input_path = os.path.join(portfolio_dir, filename)
        
        # Create backup if requested
        if backup:
            backup_path = os.path.join(backup_dir, filename)
            if not os.path.exists(backup_path):
                import shutil
                shutil.copy2(input_path, backup_path)
                print(f"Backed up: {filename}")
        
        # Create both preview and slider versions
        base_name = os.path.splitext(filename)[0]
        ext = os.path.splitext(filename)[1]
        
        # Preview version (800x600) - use cropping for better fill
        preview_filename = f"{base_name}_preview{ext}"
        preview_path = os.path.join(preview_dir, preview_filename)
        resize_image(input_path, preview_path, preview_size, crop_mode=True)
        
        # Slider version (1200x800) - use cropping for better fill
        slider_filename = f"{base_name}_slider{ext}"
        slider_path = os.path.join(slider_dir, slider_filename)
        resize_image(input_path, slider_path, slider_size, crop_mode=True)

def main():
    parser = argparse.ArgumentParser(description='Resize portfolio images to recommended dimensions')
    parser.add_argument('--portfolio-dir', 
                       default='static/img/portfolio',
                       help='Path to portfolio images directory (default: static/img/portfolio)')
    parser.add_argument('--no-backup', 
                       action='store_true',
                       help='Skip creating backup of original images')
    
    args = parser.parse_args()
    
    # Check if directory exists
    if not os.path.exists(args.portfolio_dir):
        print(f"Error: Directory '{args.portfolio_dir}' does not exist!")
        print("Please provide the correct path to your portfolio images directory.")
        sys.exit(1)
    
    print("Portfolio Image Resizer - Dual Version (Smart Cropping)")
    print("=" * 50)
    print(f"Processing images in: {args.portfolio_dir}")
    print(f"Preview size: 800x600px (4:3 ratio) - Smart cropped")
    print(f"Slider size: 1200x800px (3:2 ratio) - Smart cropped")
    print(f"Backup original images: {not args.no_backup}")
    print()
    
    # Process images
    process_portfolio_images(args.portfolio_dir, backup=not args.no_backup)
    
    print("\n" + "=" * 50)
    print("Resizing complete!")
    print("\nFile structure created:")
    print(f"├── {args.portfolio_dir}/")
    print(f"│   ├── backup_original/     # Original images")
    print(f"│   ├── preview/             # 800x600px for grid (cropped)")
    print(f"│   └── slider/              # 1200x800px for detail pages (cropped)")
    print("\nNext steps:")
    print("1. Update templates to use preview/ and slider/ images")
    print("2. Test the portfolio display")
    print("3. Delete original images if satisfied")

if __name__ == "__main__":
    main()
