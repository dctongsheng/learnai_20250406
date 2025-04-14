import os
import sys
from datetime import datetime
from PIL import Image
import requests
from io import BytesIO

# Import our image saving utilities
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.image_saver import (
    save_image_from_url, 
    save_image_from_bytes, 
    save_pil_image, 
    save_base64_image
)

def main():
    # Create a directory for saved images if it doesn't exist
    images_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "saved_images")
    os.makedirs(images_dir, exist_ok=True)
    
    # Generate a timestamp for unique filenames
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Example 1: Save an image from a URL
    image_url = "https://raw.githubusercontent.com/langchain-ai/langchain/master/docs/static/img/langchain_stack.png"
    url_save_path = os.path.join(images_dir, f"from_url_{timestamp}.png")
    save_image_from_url(image_url, url_save_path)
    
    # Example 2: Save an image using PIL
    try:
        # Download an image and convert to PIL Image
        response = requests.get(image_url)
        pil_image = Image.open(BytesIO(response.content))
        
        # Resize the image
        resized_image = pil_image.resize((300, 300))
        
        # Save the resized image
        pil_save_path = os.path.join(images_dir, f"resized_{timestamp}.png")
        save_pil_image(resized_image, pil_save_path)
    except Exception as e:
        print(f"Error in PIL example: {e}")
    
    print(f"\nAll images have been saved to: {images_dir}")

if __name__ == "__main__":
    main()
