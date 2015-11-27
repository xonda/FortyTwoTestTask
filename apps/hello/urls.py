from django.conf.urls import patterns, url
from .views import home, requests, upd_requests, edit_info
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns(
    '',
    url(r'^$', home, name='home'),
    url(r'^requests$', requests, name='requests'),
    url(r'^upd_requests$', upd_requests, name='upd_requests'),
    url(r'^edit$', edit_info, name='edit_info'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

