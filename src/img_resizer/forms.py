import requests
import hashlib


from django import forms


from .models import UploadedImage
from .utils import download_image


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

        image_formats = ("image/png", "image/jpeg", "image/jpg")
        if url:
            response = requests.head(url, stream=True)
            if response.ok:
                if response.headers["content-type"] not in image_formats:
                    raise forms.ValidationError("Неподдерживаемый формат изображения")


    def clean_file_input(self):
        data = self.cleaned_data['file_input']
        if data:
            hash_sha1 = hashlib.sha1()
            for chunk in data.chunks():
                hash_sha1.update(chunk)
            image_hash = hash_sha1.hexdigest()
            if UploadedImage.objects.filter(image_hash=image_hash).exists():
             raise forms.ValidationError("Изображение уже находится в базе")
        return data


class ResizeForm(forms.Form):
    width = forms.IntegerField(label='Ширина' , required=False)
    height = forms.IntegerField(label='Высота', required=False)

    def clean(self):
        cleaned_data = super().clean()
        if not self.cleaned_data['width'] and not self.cleaned_data['height']:
            raise forms.ValidationError('Введите хотя бы одно значение')

    def clean_width(self):
        data = self.cleaned_data['width']
        if data is None:
            return data
        if int(data) <= 0:
            raise forms.ValidationError("Размер меньше или равен 0")
        return data

    def clean_height(self):
        data = self.cleaned_data['height']
        if data is None:
            return data
        if int(data) <= 0:
            raise forms.ValidationError("Размер меньше или равен 0")
        return data
