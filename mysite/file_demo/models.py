from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage

fs = FileSystemStorage()

# Create your models here.
class Data(models.Model):
    file = models.FileField(upload_to='.', storage=fs, blank=False, null=False)
    def __str__(self):
        return self.file.name

def file(self, filename):
    url = "users/%s/%s/%s" % (self.user.username, self.directory, filename)
    return url

class UserFiles(models.Model):
    user = models.ForeignKey(User)
    directory = models.TextField()
    file = models.FileField(upload_to=file, storage=fs, blank=False, null=False)
    def __str__(self):
        return 'User: ' + self.user.username + ', file: ' + self.file.name
