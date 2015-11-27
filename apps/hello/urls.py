from django.conf.urls import patterns, url
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from .views import home, requests, upd_requests, edit_info

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns(
    '',
    url(r'^$', home, name='home'),
    url(r'^requests$', requests, name='requests'),
    url(r'^upd_requests$', upd_requests, name='upd_requests'),
    url(r'^edit$', edit_info, name='edit_info'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
