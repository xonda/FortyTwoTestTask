from django.shortcuts import render
from .models import Info


def home(request):
    info = Info.objects.get()
    context = {'info': info,
               'title': 'Xonda'
               }
    return render(request, 'base.html', context)
