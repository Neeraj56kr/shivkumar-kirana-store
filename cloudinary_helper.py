"""
Cloudinary Helper Module
Handles image upload to Cloudinary for persistent storage on Render.
"""

import os
import cloudinary
import cloudinary.uploader
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

load_dotenv()

# Configure Cloudinary from environment variables
def configure_cloudinary():
    """Configure Cloudinary with environment variables."""
    cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME')
    api_key = os.getenv('CLOUDINARY_API_KEY')
    api_secret = os.getenv('CLOUDINARY_API_SECRET')
    
    if all([cloud_name, api_key, api_secret]):
        try:
            cloudinary.config(
                cloud_name=cloud_name,
                api_key=api_key,
                api_secret=api_secret,
                secure=True
            )
            print(f"Cloudinary configured successfully for cloud: {cloud_name}")
            return True
        except Exception as e:
            print(f"Error configuring Cloudinary: {e}")
            return False
    else:
        print("Cloudinary credentials missing in environment variables.")
        return False

# Check if Cloudinary is configured
CLOUDINARY_ENABLED = configure_cloudinary()


def upload_image(file, folder="kirana_products"):
    """
    Upload image to Cloudinary.
    
    Args:
        file: The uploaded file object from Flask request
        folder: Cloudinary folder name to organize images
    
    Returns:
        str: The Cloudinary URL if successful, None if failed
    """
    if not CLOUDINARY_ENABLED:
        print("Cloudinary not configured, skipping cloud upload")
        return None
    
    if not file or not file.filename:
        return None
    
    try:
        # Upload to Cloudinary
        result = cloudinary.uploader.upload(
            file,
            folder=folder,
            resource_type="image",
            transformation=[
                {"width": 500, "height": 500, "crop": "limit"},
                {"quality": "auto"},
                {"fetch_format": "auto"}
            ]
        )
        
        # Return the secure URL
        return result.get('secure_url')
    
    except Exception as e:
        print(f"Cloudinary upload error: {e}")
        return None


def delete_image(public_id):
    """
    Delete image from Cloudinary by public_id.
    
    Args:
        public_id: The Cloudinary public ID of the image
    
    Returns:
        bool: True if deleted successfully
    """
    if not CLOUDINARY_ENABLED:
        return False
    
    try:
        result = cloudinary.uploader.destroy(public_id)
        return result.get('result') == 'ok'
    except Exception as e:
        print(f"Cloudinary delete error: {e}")
        return False


def get_public_id_from_url(url):
    """
    Extract public_id from Cloudinary URL for deletion.
    
    Args:
        url: The Cloudinary URL
    
    Returns:
        str: The public_id or None
    """
    if not url or 'cloudinary' not in url:
        return None
    
    try:
        # URL format: https://res.cloudinary.com/cloud_name/image/upload/v123/folder/filename.ext
        parts = url.split('/upload/')
        if len(parts) == 2:
            # Remove version and extension
            path = parts[1]
            # Remove version (v1234567890/)
            if path.startswith('v'):
                path = '/'.join(path.split('/')[1:])
            # Remove extension
            public_id = path.rsplit('.', 1)[0]
            return public_id
    except:
        pass
    
    return None
