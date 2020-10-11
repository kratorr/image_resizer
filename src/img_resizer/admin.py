from django.contrib import admin

# Register your models here.
from img_resizer.models import UploadedImage

admin.site.register(UploadedImage)