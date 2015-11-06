from django.conf.urls import patterns, url

from django.contrib import admin
admin.autodiscover()

from hello.views import home, requests

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'fortytwo_test_task.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', home, name='home'),
    url(r'^requests$', requests, name='requests'),
)