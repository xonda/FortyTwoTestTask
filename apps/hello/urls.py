from django.conf.urls import patterns, url
from .views import home

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns(
    '',
    url(r'^$', home, name='home'),
)
