import os
import requests
from PIL import Image
from io import BytesIO
import base64

def save_image_from_url(url, save_path, create_dirs=True):
    """
    Download an image from a URL and save it to the specified path.
    
    Args:
        url (str): The URL of the image to download
        save_path (str): The local path where the image should be saved
        create_dirs (bool): Whether to create directories in the save path if they don't exist
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Create directories if they don't exist
        if create_dirs:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        # Download the image
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        # Save the image
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"Image saved successfully to {save_path}")
        return True
    
    except Exception as e:
        print(f"Error saving image: {e}")
        return False

def save_image_from_bytes(image_bytes, save_path, create_dirs=True):
    """
    Save image data from bytes to the specified path.
    
    Args:
        image_bytes (bytes): The image data as bytes
        save_path (str): The local path where the image should be saved
        create_dirs (bool): Whether to create directories in the save path if they don't exist
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Create directories if they don't exist
        if create_dirs:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        # Save the image
        with open(save_path, 'wb') as f:
            f.write(image_bytes)
        
        print(f"Image saved successfully to {save_path}")
        return True
    
    except Exception as e:
        print(f"Error saving image: {e}")
        return False

def save_pil_image(pil_image, save_path, format=None, create_dirs=True):
    """
    Save a PIL Image object to the specified path.
    
    Args:
        pil_image (PIL.Image): The PIL Image object to save
        save_path (str): The local path where the image should be saved
        format (str, optional): The format to save as (e.g., 'PNG', 'JPEG')
        create_dirs (bool): Whether to create directories in the save path if they don't exist
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Create directories if they don't exist
        if create_dirs:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        # Save the image
        pil_image.save(save_path, format=format)
        
        print(f"Image saved successfully to {save_path}")
        return True
    
    except Exception as e:
        print(f"Error saving image: {e}")
        return False

def save_base64_image(base64_string, save_path, create_dirs=True):
    """
    Save a base64 encoded image to the specified path.
    
    Args:
        base64_string (str): The base64 encoded image string
        save_path (str): The local path where the image should be saved
        create_dirs (bool): Whether to create directories in the save path if they don't exist
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Remove data URL prefix if present
        if ',' in base64_string:
            base64_string = base64_string.split(',', 1)[1]
        
        # Decode the base64 string
        image_data = base64.b64decode(base64_string)
        
        # Create directories if they don't exist
        if create_dirs:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        # Save the image
        with open(save_path, 'wb') as f:
            f.write(image_data)
        
        print(f"Image saved successfully to {save_path}")
        return True
    
    except Exception as e:
        print(f"Error saving image: {e}")
        return False
