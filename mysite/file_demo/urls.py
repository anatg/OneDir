__author__ = 'cls2be'

from django.conf.urls import patterns, url

from file_demo import views

urlpatterns = patterns('',
    url(r'^upload_file/$', views.upload_file, name='upload_file'),
    url(r'^login/$', views.login_view, name='login_view'),
    url(r'^cookie_test/$', views.cookie_test, name='cookie_test')
)