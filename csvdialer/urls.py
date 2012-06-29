from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from csvdialer import views

urlpatterns = patterns(
    'csvdialer.views',
    url(r'^robocall/$', views.robocall, name='robocall'),
    url(r'^telml/play/(?P<encoded_url>.*?)/$', views.telml_play, name='telml_play'),
    url(r'^telml/say/(?P<encoded_url>.*?)/$', views.telml_say, name='telml_say'),
)
