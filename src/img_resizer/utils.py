from PIL import Image, ImageOps
import requests
from tempfile import NamedTemporaryFile
from io import BytesIO


def resize_image(source_image, width, height, format):
    image = Image.open(source_image)
    size = (width, height)
    if not width or not height:
        source_width, source_height = image.size
        if width:
            new_height = width * source_height / source_width
            new_size = (int(width), int(new_height))
        if height:
            new_width = height * source_width / source_height
            new_size = (int(new_width), int(height))

        resized_image = image.resize(new_size)
    else:
        image.thumbnail(size)
        resized_image = image

    with BytesIO() as buffer:
        resized_image.save(buffer, format=format)
        data = buffer.getvalue()
    return data


def download_image(url):
    image_formats = ("image/png", "image/jpeg", "image/jpg")
    response = requests.get(url, stream=True)
    if response.ok:
        if response.headers["content-type"] in image_formats:
            file_name = url.split('/')[-1]
            image = response.content
            return image, file_name
