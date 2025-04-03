"""Utility functions for image generation."""

import os
import base64
import logging

log = logging.getLogger(__name__)


def save_generated_image(image_data, save_path: str, index: int = 0) -> str:
    """Save a generated image to disk.
    
    Args:
        image_data: Image data object from OpenAI API response
        save_path: Directory to save the image in
        index: Index for the filename
        
    Returns:
        str: Path to the saved file
    """
    if not hasattr(image_data, "b64_json") or not image_data.b64_json:
        return None
        
    os.makedirs(save_path, exist_ok=True)
    
    # Define filename with index
    base_filename = f"image_{index+1}"
    file_path = os.path.join(save_path, f"{base_filename}.png")
    
    # Decode base64 image
    img_data = base64.b64decode(image_data.b64_json)
    with open(file_path, "wb") as f:
        f.write(img_data)
    
    return file_path 