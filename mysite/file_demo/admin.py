from django.contrib import admin
from file_demo.models import Data, UserFiles, UserFilesAdmin

# Register your models here.
admin.site.register(Data)
admin.site.register(UserFiles, UserFilesAdmin)