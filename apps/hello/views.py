from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from .models import Info, WebRequest


# def home(request):
#     try:
#         info = Info.objects.all()[0]
#     except:
#         info = "Unfortunately there are no records in database"
#
#     context = {'info': info}
#     return render(request, 'home.html', context)

def home(request):
    info = Info.objects.first() or None

    context = {'info': info}
    return render(request, 'home.html', context)


def requests(request):
    return render(request, 'requests.html')


def upd_requests(request):
    if not request.is_ajax():
        return HttpResponse('Not ajax request')

    last_10_reqs = WebRequest.objects.all().order_by('-id')[:10]
    if last_10_reqs:
        data = serializers.serialize("json", last_10_reqs)
        return HttpResponse(data, content_type='application/json')

    return HttpResponse('No records in database')
