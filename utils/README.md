# Image Saving Utilities

This directory contains utilities for saving images from various sources to your local filesystem.

## Overview

The `image_saver.py` module provides several functions for saving images:

- `save_image_from_url`: Download and save an image from a URL
- `save_image_from_bytes`: Save image data from bytes
- `save_pil_image`: Save a PIL Image object
- `save_base64_image`: Save a base64 encoded image

## Usage Examples

### Save an image from a URL

```python
from utils.image_saver import save_image_from_url

# Download and save an image
url = "https://example.com/image.jpg"
save_path = "saved_images/my_image.jpg"
save_image_from_url(url, save_path)
```

### Save image data from bytes

```python
from utils.image_saver import save_image_from_bytes

# Save image data
with open("image_data.bin", "rb") as f:
    image_bytes = f.read()
    
save_path = "saved_images/from_bytes.jpg"
save_image_from_bytes(image_bytes, save_path)
```

### Save a PIL Image

```python
from PIL import Image
from utils.image_saver import save_pil_image

# Open and resize an image
img = Image.open("original.jpg")
resized_img = img.resize((300, 300))

# Save the resized image
save_path = "saved_images/resized.jpg"
save_pil_image(resized_img, save_path, format="JPEG")
```

### Save a base64 encoded image

```python
from utils.image_saver import save_base64_image

# Save a base64 encoded image
base64_string = "iVBORw0KGgoAAAANSUhEUgAA..."  # Base64 encoded image data
save_path = "saved_images/from_base64.png"
save_base64_image(base64_string, save_path)
```

## Example Scripts

Check out the `examples` directory for more comprehensive examples:

- `save_images_example.py`: Basic examples of saving images
- `web_image_downloader.py`: Download images from a webpage

## Running the Web Image Downloader

The web image downloader script allows you to download images from a webpage:

```bash
python examples/web_image_downloader.py https://example.com --output my_images --max 20 --min-size 50000
```

Arguments:
- `url`: The URL of the webpage to download images from
- `--output`, `-o`: Output directory name (default: 'downloaded_images')
- `--max`, `-m`: Maximum number of images to download (default: 10)
- `--min-size`, `-s`: Minimum size of images in bytes (default: 10000)
