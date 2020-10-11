from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.files.base import ContentFile
from django.utils.http import urlencode
from django.urls import reverse
from .forms import ImgUploadForm, ResizeForm
from .models import UploadedImage
from .utils import download_image, resize_image


def index(request):
    images = UploadedImage.objects.all().order_by('-created_time')
    print(images)
    context = {'images': images}
    return render(request, 'img_resizer/index.html', context)


def upload(request):
    if request.method == 'POST':        
        form = ImgUploadForm(request.POST, request.FILES)
        if form.is_valid():
            if request.FILES:
                new_image = UploadedImage(image=request.FILES['file_input'])
                new_image.save()
            if request.POST['url']:            
                downloaded_image, file_name = download_image(request.POST['url'])
                new_image = UploadedImage()            
                new_image.image.save(file_name, ContentFile(downloaded_image), save=True)
            return HttpResponseRedirect('/')
    else:
        form = ImgUploadForm()
    return render(request, 'img_resizer/upload_form.html', {'form': form})


def image_view(request, image_hash):

    form = ResizeForm()


    if None not in (width, height, size):
        size_in_bytes = int(size)*1024
        image = UploadedImage.objects.get(image_hash=image_hash)
        resized_image = resize_image(image.image, int(width), int(height), size_in_bytes)

        with open(resized_image, "rb") as f:
            return HttpResponse(f.read(), content_type="image/jpeg") 

    if request.method == 'POST':
        get_args_str = urlencode({
            'width': request.POST['width'],
            'height': request.POST['height'], 
        })
 
        url ='{}?{}'.format(request.path, get_args_str)
        return redirect(url)
    
    image = UploadedImage.objects.get(image_hash=image_hash)
    return render(request, 'img_resizer/image_view.html', {'image': image, 'form': form})
    