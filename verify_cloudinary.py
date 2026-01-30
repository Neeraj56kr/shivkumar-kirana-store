import os
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv

load_dotenv()

cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME')
api_key = os.getenv('CLOUDINARY_API_KEY')
api_secret = os.getenv('CLOUDINARY_API_SECRET')

print(f"Cloud Name: {cloud_name}")
print(f"API Key: {api_key}")
print(f"API Secret: {api_secret} (Length: {len(api_secret) if api_secret else 0})")

if not all([cloud_name, api_key, api_secret]):
    print("MISSING CREDENTIALS!")
else:
    try:
        cloudinary.config(
            cloud_name=cloud_name,
            api_key=api_key,
            api_secret=api_secret,
            secure=True
        )
        print("Configuration attempted.")
        # Try a simple api call to verify
        # We can't easily upload without a file, but we can generate a url or check ping if possible.
        # Actually, let's just try to generate a url for a fake image, that doesn't validate auth though.
        # The best test is an upload or an api call.
        # Let's try to get resources (might need admin api) or just trust the config if no error raised yet?
        # Cloudinary config doesn't connect immediately. We need to do an operation.
        
        # Let's try to upload a tiny text file
        with open("test_upload.txt", "w") as f:
            f.write("test")
            
        print("Attempting test upload...")
        response = cloudinary.uploader.upload("test_upload.txt")
        print("UPLOAD SUCCESS!")
        print(response)
        
    except Exception as e:
        print(f"CONNECTION FAILED: {e}")
