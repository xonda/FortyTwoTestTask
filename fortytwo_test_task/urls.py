from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from apps.hello import urls

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include(urls)),
)
