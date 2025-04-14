import os
import sys
import argparse
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import random

# Import our image saving utility
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.image_saver import save_image_from_url

def is_valid_url(url):
    """Check if the URL is valid."""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def extract_image_urls(url, min_size=10000):
    """
    Extract image URLs from a webpage.
    
    Args:
        url (str): The URL of the webpage
        min_size (int): Minimum size of images to download in bytes
        
    Returns:
        list: List of image URLs
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        img_tags = soup.find_all('img')
        
        image_urls = []
        for img in img_tags:
            # Get image URL
            img_url = img.get('src') or img.get('data-src')
            if not img_url:
                continue
                
            # Make absolute URL
            img_url = urljoin(url, img_url)
            
            # Check if URL is valid
            if not is_valid_url(img_url):
                continue
                
            # Check image size if min_size is specified
            if min_size > 0:
                try:
                    head_response = requests.head(img_url, headers=headers)
                    content_length = head_response.headers.get('content-length')
                    if content_length and int(content_length) < min_size:
                        continue
                except:
                    pass
                    
            image_urls.append(img_url)
            
        return image_urls
        
    except Exception as e:
        print(f"Error extracting image URLs: {e}")
        return []

def download_images(url, output_dir, max_images=10, min_size=10000):
    """
    Download images from a webpage.
    
    Args:
        url (str): The URL of the webpage
        output_dir (str): Directory to save images
        max_images (int): Maximum number of images to download
        min_size (int): Minimum size of images to download in bytes
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Extract image URLs
    print(f"Extracting image URLs from {url}...")
    image_urls = extract_image_urls(url, min_size)
    
    if not image_urls:
        print("No images found.")
        return
        
    print(f"Found {len(image_urls)} images.")
    
    # Limit the number of images to download
    if max_images > 0:
        image_urls = image_urls[:max_images]
    
    # Download images
    for i, img_url in enumerate(image_urls):
        try:
            # Generate filename from URL
            filename = os.path.basename(urlparse(img_url).path)
            if not filename or '.' not in filename:
                filename = f"image_{i+1}.jpg"
                
            save_path = os.path.join(output_dir, filename)
            
            # Download and save the image
            print(f"Downloading {i+1}/{len(image_urls)}: {img_url}")
            save_image_from_url(img_url, save_path)
            
            # Add a small delay to avoid overwhelming the server
            time.sleep(random.uniform(0.5, 1.5))
            
        except Exception as e:
            print(f"Error downloading {img_url}: {e}")
    
    print(f"\nDownloaded images saved to: {output_dir}")

def main():
    parser = argparse.ArgumentParser(description='Download images from a webpage')
    parser.add_argument('url', help='URL of the webpage')
    parser.add_argument('--output', '-o', default='downloaded_images', help='Output directory')
    parser.add_argument('--max', '-m', type=int, default=10, help='Maximum number of images to download')
    parser.add_argument('--min-size', '-s', type=int, default=10000, help='Minimum size of images in bytes')
    
    args = parser.parse_args()
    
    # Create a timestamped directory
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    output_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "saved_images",
        f"{args.output}_{timestamp}"
    )
    
    download_images(args.url, output_dir, args.max, args.min_size)

if __name__ == "__main__":
    main()
