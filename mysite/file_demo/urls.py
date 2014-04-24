__author__ = 'cls2be'

from django.conf.urls import patterns, url

from file_demo import views

urlpatterns = patterns('',
    url(r'^upload_file/$', views.upload_file, name='upload_file'),
    url(r'^login/$', views.login_view, name='login_view'),
    url(r'^cookie_test/$', views.cookie_test, name='cookie_test'),
    url(r'^check_username/$', views.check_username, name='check_username'),
    url(r'^register/$', views.register, name='register'),
    url(r'^change_password/$', views.change_password, name='change_password'),
    url(r'^json_request/$', views.json_request, name='json_request'),
    url(r'^delete_file/$', views.delete_file, name='delete_file'),
    url(r'^download_file/$', views.download_file, name='download_file'),
)