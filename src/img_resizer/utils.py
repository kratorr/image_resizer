from PIL import Image
import requests
from tempfile import NamedTemporaryFile
from io import BytesIO


def resize_image(image, width, height, size_limit):
    input_image = Image.open(image)
    resized_image = input_image.resize((width, height)).convert('RGB')
    tmpfile = NamedTemporaryFile()
    out = BytesIO()
    resized_image.save(out, format='JPEG')
    quality = 75
    with BytesIO() as buffer:
            resized_image.save(buffer, format="JPEG")
            data = buffer.getvalue()
    filesize = len(data)

    return tmpfile.name + '.jpg'

    
    

def download_image(url):
    request = requests.get(url, stream=True)
    file_name = url.split('/')[-1]
    image = request.content
    return image, file_name