__author__ = 'cls2be'

from django.conf.urls import patterns, url

from file_demo import views

urlpatterns = patterns('',
    url(r'^upload_file/$', views.upload_file, name='upload_file')
)