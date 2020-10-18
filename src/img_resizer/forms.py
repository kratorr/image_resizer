from django import forms

import requests
import hashlib

from .models import UploadedImage


class ImageUploadForm(forms.Form):
    url = forms.URLField(label='Ссылка', required=False)
    file_input = forms.ImageField(label='Файл', required=False)
    image_hash = forms.CharField(widget=forms.HiddenInput(), required=False)

    def clean(self):
        cleaned_data = super().clean()
        url = cleaned_data.get("url")
        file_input = cleaned_data.get("file_input")
        if url and file_input:
            raise forms.ValidationError('Выберите только один варинат')
        if url is '' and file_input is None:
            raise forms.ValidationError('Выберите хотя бы один вариант')
        return cleaned_data

    def clean_file_input(self):
        data = self.cleaned_data['file_input'] 
        hash_sha1 = hashlib.sha1()
        for chunk in data.chunks():
            hash_sha1.update(chunk)
        image_hash = hash_sha1.hexdigest()
        instance = UploadedImage.objects.filter(image_hash=image_hash)
        if instance.exists():
            raise forms.ValidationError("Изображение уже находится в базе")
        return data


class ResizeForm(forms.Form):
    width = forms.IntegerField(label='Ширина', min_value=1, required=False)
    height = forms.IntegerField(label='Высота', min_value=1, required=False)


def is_url_image(image_url):
   image_formats = ("image/png", "image/jpeg", "image/jpg")
   r = requests.head(image_url)
   if r.headers["content-type"] in image_formats:
      return True
   return False