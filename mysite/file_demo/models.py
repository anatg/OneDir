from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage

fs = FileSystemStorage()

# Create your models here.
class Data(models.Model):
    file = models.FileField(upload_to='.', storage=fs, blank=False, null=False)
    def __str__(self):
        return self.file.name

#TODO: Add another way to give this function a directory structure
def file(self, filename):
    url = "users/%s/%s" % (self.user.username, filename)
    return url

#TODO: Figure out how to pass directory structure from view to file function here
class UserFiles(models.Model):
    user = models.ForeignKey(User)
    file = models.FileField(upload_to=file, storage=fs, blank=False, null=False)
    def __str__(self):
        return 'User: ' + self.user.username + ', file: ' + self.file.name
