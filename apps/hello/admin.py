from django.contrib import admin
from .models import Info, WebRequest, DatabaseLog


admin.site.register(Info)
admin.site.register(WebRequest)
admin.site.register(DatabaseLog)
