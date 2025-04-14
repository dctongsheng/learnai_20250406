#!/usr/bin/env python3
"""
Image Saving Utility - Main Script

This script provides a command-line interface to save images from various sources.
"""

import os
import sys
import argparse
from datetime import datetime

# Import our image saving utilities
from utils.image_saver import (
    save_image_from_url, 
    save_image_from_bytes, 
    save_pil_image, 
    save_base64_image
)

def setup_output_dir(output_dir=None):
    """Set up the output directory for saved images."""
    if not output_dir:
        # Use default directory
        output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "saved_images")
    
    # Create the directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    return output_dir

def save_from_url(args):
    """Save an image from a URL."""
    output_dir = setup_output_dir(args.output_dir)
    
    # Generate filename if not provided
    if not args.filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        args.filename = f"from_url_{timestamp}.jpg"
    
    save_path = os.path.join(output_dir, args.filename)
    
    # Download and save the image
    success = save_image_from_url(args.url, save_path)
    
    if success:
        print(f"Image saved to: {save_path}")
    else:
        print("Failed to save image.")

def save_from_clipboard(args):
    """Save an image from the clipboard."""
    try:
        from PIL import ImageGrab
    except ImportError:
        print("Error: PIL/Pillow is required for clipboard operations.")
        print("Install it with: pip install pillow")
        return
    
    # Get image from clipboard
    img = ImageGrab.grabclipboard()
    
    if img is None:
        print("No image found in clipboard.")
        return
    
    output_dir = setup_output_dir(args.output_dir)
    
    # Generate filename if not provided
    if not args.filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        args.filename = f"clipboard_{timestamp}.png"
    
    save_path = os.path.join(output_dir, args.filename)
    
    # Save the image
    success = save_pil_image(img, save_path)
    
    if success:
        print(f"Image saved to: {save_path}")
    else:
        print("Failed to save image.")

def save_from_file(args):
    """Save an image from a file (copy to new location)."""
    if not os.path.exists(args.source):
        print(f"Error: Source file '{args.source}' does not exist.")
        return
    
    output_dir = setup_output_dir(args.output_dir)
    
    # Generate filename if not provided
    if not args.filename:
        args.filename = os.path.basename(args.source)
    
    save_path = os.path.join(output_dir, args.filename)
    
    try:
        # Read the source file
        with open(args.source, 'rb') as f:
            image_bytes = f.read()
        
        # Save to the destination
        success = save_image_from_bytes(image_bytes, save_path)
        
        if success:
            print(f"Image saved to: {save_path}")
        else:
            print("Failed to save image.")
            
    except Exception as e:
        print(f"Error saving image: {e}")

def download_from_webpage(args):
    """Download images from a webpage."""
    try:
        # Import the web image downloader
        sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "examples"))
        from web_image_downloader import download_images
    except ImportError:
        print("Error: Required modules for web downloading are not available.")
        print("Make sure you have installed: requests, beautifulsoup4")
        return
    
    output_dir = setup_output_dir(args.output_dir)
    
    # Create a subdirectory for this download
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    download_dir = os.path.join(output_dir, f"web_download_{timestamp}")
    
    # Download images
    download_images(args.url, download_dir, args.max, args.min_size)

def main():
    parser = argparse.ArgumentParser(description='Save images from various sources')
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # URL parser
    url_parser = subparsers.add_parser('url', help='Save an image from a URL')
    url_parser.add_argument('url', help='URL of the image')
    url_parser.add_argument('--output-dir', '-o', help='Output directory')
    url_parser.add_argument('--filename', '-f', help='Output filename')
    
    # Clipboard parser
    clipboard_parser = subparsers.add_parser('clipboard', help='Save an image from the clipboard')
    clipboard_parser.add_argument('--output-dir', '-o', help='Output directory')
    clipboard_parser.add_argument('--filename', '-f', help='Output filename')
    
    # File parser
    file_parser = subparsers.add_parser('file', help='Save an image from a file (copy to new location)')
    file_parser.add_argument('source', help='Source file path')
    file_parser.add_argument('--output-dir', '-o', help='Output directory')
    file_parser.add_argument('--filename', '-f', help='Output filename')
    
    # Web parser
    web_parser = subparsers.add_parser('web', help='Download images from a webpage')
    web_parser.add_argument('url', help='URL of the webpage')
    web_parser.add_argument('--output-dir', '-o', help='Output directory')
    web_parser.add_argument('--max', '-m', type=int, default=10, help='Maximum number of images to download')
    web_parser.add_argument('--min-size', '-s', type=int, default=10000, help='Minimum size of images in bytes')
    
    args = parser.parse_args()
    
    if args.command == 'url':
        save_from_url(args)
    elif args.command == 'clipboard':
        save_from_clipboard(args)
    elif args.command == 'file':
        save_from_file(args)
    elif args.command == 'web':
        download_from_webpage(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
