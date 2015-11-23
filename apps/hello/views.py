from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from .models import Info, WebRequest


def home(request):
    try:
        info = Info.objects.all()[0]
    except:
        info = "Unfortunately there are no records in database"

    context = {'info': info}
    return render(request, 'home.html', context)


def requests(request):
    return render(request, 'requests.html')


def upd_requests(request):
    if request.is_ajax():
        last_10_reqs = WebRequest.objects.all().order_by('-id')[:10]
        if last_10_reqs:
            data = serializers.serialize("json", last_10_reqs)
            return HttpResponse(data, content_type='application/json')
        else:
            return HttpResponse('No records in database')
    return HttpResponse('Not ajax request')


def edit(request):
    return render(request, 'edit_info.html')