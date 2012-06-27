from django.conf.urls.defaults import patterns, include, url
from csvdialer import views


urlpatterns = patterns(
    'csvdialer.views',
    url(r'^robocall/$', views.robocall, name='robocall'),
    url(r'^telml/call/(?P<encoded_url>.*?)/$', views.telml_call, name='telml_call'),
)
