from django import forms

class ImgUploadForm(forms.Form):
    url = forms.CharField(label='Enter URL', max_length=100, required=False)
    file_input = forms.FileField(label='Choose your image', required=False)

    def clean(self):
        cleaned_data = super().clean()
        url = cleaned_data.get("url")
        file_input = cleaned_data.get("file_input")
    
        if url and file_input:
            raise forms.ValidationError('Please fill only one field.')
        if url is '' and file_input is None:
            raise forms.ValidationError('Please fill one field')
        return cleaned_data


class ResizeForm(forms.Form):
    width = forms.IntegerField(label='Ширина')
    height = forms.IntegerField(label='Высота')