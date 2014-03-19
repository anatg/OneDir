from django.db import models
from django.core.files.storage import FileSystemStorage

fs = FileSystemStorage(location='/home/cls2be/Django_Projects/files/')

# Create your models here.
class Data(models.Model):
    file = models.FileField(upload_to='.', storage=fs, blank=False, null=False)
    def __str__(self):
        return self.file.name
