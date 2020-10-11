from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.files.base import ContentFile
from django.utils.http import urlencode
from django.urls import reverse
from io import BytesIO
import base64

from img_resizer.forms import ImageUploadForm, ResizeForm
from img_resizer.models import UploadedImage
from img_resizer.utils import download_image, resize_image


def index(request):
    images = UploadedImage.objects.all().order_by('-created_time')
    print(images)
    context = {'images': images}
    return render(request, 'img_resizer/index.html', context)


def upload(request):
    if request.method == 'POST':        
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            if request.FILES:
                new_image = UploadedImage(image=request.FILES['file_input'])
                new_image.save()
            if request.POST['url']:
                downloaded_image, file_name = download_image(request.POST['url'])
                new_image = UploadedImage(input_url=form.cleaned_data['url'])
                new_image.image.save(file_name,ContentFile(downloaded_image), save=True)
            return HttpResponseRedirect('/')
    else:
        form = ImageUploadForm()
    return render(request, 'img_resizer/upload_form.html', {'form': form})


def image_view(request, image_hash):
    image = UploadedImage.objects.get(image_hash=image_hash)
    if request.method == 'POST':
        form = ResizeForm(request.POST)
        if form.is_valid():
            width = form.cleaned_data['width']
            height = form.cleaned_data['height']
            resized_image = resize_image(image.image, int(width), int(height))
            resized_image = base64.b64encode(resized_image).decode('utf-8')  # load the bytes in the context as base64
            return render(request, 'img_resizer/resized_form.html', {'image': resized_image, 'form': form})

    form = ResizeForm(initial={'height': image.image.height, 'width': image.image.width})
    return render(request, 'img_resizer/image_view.html', {'image': image, 'form': form})
