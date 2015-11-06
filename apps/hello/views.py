from django.shortcuts import render
from .models import Info


def home(request):
    try:
        info = Info.objects.get(pk=1)
    except:
        info = "Unfortunately there are no records in database"

    context = {'info': info}
    return render(request, 'home.html', context)
