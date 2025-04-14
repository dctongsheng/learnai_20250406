import os
import sys
import time
from datetime import datetime
from PIL import ImageGrab

# Import our image saving utility
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.image_saver import save_pil_image

def save_clipboard_image():
    """
    Save an image from the clipboard to a file.
    
    Returns:
        str: Path to the saved image, or None if no image was in the clipboard
    """
    try:
        # Get image from clipboard
        img = ImageGrab.grabclipboard()
        
        if img is None:
            print("No image found in clipboard.")
            return None
            
        # Create a directory for saved images if it doesn't exist
        images_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "saved_images")
        os.makedirs(images_dir, exist_ok=True)
        
        # Generate a filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        image_filename = f"clipboard_{timestamp}.png"
        image_path = os.path.join(images_dir, image_filename)
        
        # Save the image
        save_pil_image(img, image_path)
        
        return image_path
        
    except Exception as e:
        print(f"Error saving clipboard image: {e}")
        return None

def main():
    print("Copy an image to your clipboard (e.g., take a screenshot), then press Enter...")
    input()
    
    image_path = save_clipboard_image()
    
    if image_path:
        print(f"Image saved to: {image_path}")
    else:
        print("Failed to save image from clipboard.")

if __name__ == "__main__":
    main()
