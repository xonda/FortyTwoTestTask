from django.conf.urls import patterns, url
from .views import home, requests, upd_requests

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'fortytwo_test_task.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', home, name='home'),
    url(r'^requests$', requests, name='requests'),
    url(r'^upd_requests$', upd_requests, name='upd_requests'),

)
