from PIL import Image
import requests
from tempfile import NamedTemporaryFile
from io import BytesIO


def resize_image(image, width, height):
    input_image = Image.open(image)
    resized_image = input_image.resize((width, height)).convert('RGB')

    with BytesIO() as buffer:
        resized_image.save(buffer, format="JPEG")
        data = buffer.getvalue()
    return data


def download_image(url):
    request = requests.get(url, stream=True)
    file_name = url.split('/')[-1]
    image = request.content
    return image, file_name