from django import forms

import requests

from .models import UploadedImage

class ImageUploadForm(forms.Form):
    url = forms.URLField(label='Ссылка', required=False)
    file_input = forms.FileField(label='Файл', required=False)

    def clean(self):
        cleaned_data = super().clean()
        url = cleaned_data.get("url")
        file_input = cleaned_data.get("file_input")
    
        if url and file_input:
            raise forms.ValidationError('Выберите только один варинат')
        if url is '' and file_input is None:
            raise forms.ValidationError('Выберите хотя бы один вариант')

        return cleaned_data


class ResizeForm(forms.Form):
    width = forms.IntegerField(label='Ширина', min_value=1, required=False)
    height = forms.IntegerField(label='Высота', min_value=1, required=False)


def is_url_image(image_url):
   image_formats = ("image/png", "image/jpeg", "image/jpg")
   r = requests.head(image_url)
   if r.headers["content-type"] in image_formats:
      return True
   return False