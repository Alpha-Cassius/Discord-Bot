import requests
import io
from PIL import Image

API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-dev"
HEADERS = {"Authorization": "Bearer YOUR_HUGGINGFACE_API"} # Replace with your actual api 

def generate_image(prompt):
    response = requests.post(API_URL, headers=HEADERS, json={"inputs": prompt})

    if response.status_code == 200:
        image_bytes = response.content
        image = Image.open(io.BytesIO(image_bytes))
        image.save("image.jpg")  # Save the image
        return ["image.jpg", 1]
    else:
        return [f"Error: {response.status_code}, {response.text}", 0]
