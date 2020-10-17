from PIL import Image
import requests
from tempfile import NamedTemporaryFile
from io import BytesIO


def resize_image(source_image, width, height, format):
    image = Image.open(source_image)
    print(image)
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
        resized_image = image.resize((int(width), int(height)))

    with BytesIO() as buffer:
        resized_image.save(buffer, format=format)
        data = buffer.getvalue()
    return data


def download_image(url):
    response = requests.get(url, stream=True)
    if response.ok:
        file_name = url.split('/')[-1]
        image = response.content
        return image, file_name