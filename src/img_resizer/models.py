from django.db import models
import hashlib
# Create your models here.


class UploadedImage(models.Model):
    image = models.ImageField(unique=True)
    input_url = models.URLField(blank=True)
    image_hash = models.CharField(unique=True, max_length=32)
    created_time = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        hash_sha1 = hashlib.sha1()
        for chunk in self.image.chunks():
            hash_sha1.update(chunk)
        self.image_hash = hash_sha1.hexdigest()
        super(UploadedImage, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return "/%s/" % self.image_hash
    
    def get_hash(self):
        return self.image_hash