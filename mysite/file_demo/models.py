from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import json_helper


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
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    directory = models.TextField()
    file = models.FileField(upload_to=file, storage=fs, blank=False, null=False)
    def size(self):
        return str(self.file.size) + ' bytes'

    def __str__(self):
        return 'USER: ' + self.user.username + '  LOCATION: ' + self.file.name + \
               '     SIZE: ' + str(self.file.size) + ' bytes'

class UserFilesAdmin(admin.ModelAdmin):
    list_display = ['user', 'file', 'size']
    list_display_links = ['file']
    search_fields = ['user__username', 'file']


from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

@receiver(pre_delete, sender=UserFiles)
def userfiles_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    json_helper.delete_file(settings.MEDIA_ROOT+'users/'+str(instance.user.username)+'/', instance.file.name,
                                    settings.MEDIA_ROOT+'users/'+str(instance.user.username)+'/'+instance.file.name)
    instance.file.delete(False)
