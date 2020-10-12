import base64

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.core.files.base import ContentFile

from .forms import ImageUploadForm, ResizeForm
from .models import UploadedImage
from .utils import download_image, resize_image


def index(request):
    images = UploadedImage.objects.all().order_by('-created_time')
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
                # TODO валидировать что по урлу лежит именно изображние
                downloaded_image, file_name = download_image(request.POST['url'])
                new_image = UploadedImage(input_url=form.cleaned_data['url'])
                new_image.image.save(file_name, ContentFile(downloaded_image), save=True)
            return redirect('image_view', image_hash=new_image.image_hash)
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
            # TODO при передаче одного параметра(ширина или высота) во время ресайза соблюдать пропорции
            resized_image_bytes = resize_image(image.image, width, height)
            resized_image = base64.b64encode(resized_image_bytes).decode('utf-8')
            return render(request, 'img_resizer/image_view.html', {'image': resized_image, 'form': form, 'resized': True})
    form = ResizeForm(initial={'height': image.image.height, 'width': image.image.width})
    return render(request, 'img_resizer/image_view.html', {'image': image, 'form': form, 'resized': False})
