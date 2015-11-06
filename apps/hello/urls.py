from django.conf.urls import patterns, url

from django.contrib import admin
admin.autodiscover()

from hello.views import home

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'fortytwo_test_task.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', home, name='home'),

)