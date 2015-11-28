import time
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core import serializers
from .models import Info, WebRequest
from .forms import InfoForm


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


@login_required()
def edit_info(request):
    try:
        info = Info.objects.all()[0]
    except:
        return HttpResponse('No records in database')
    form = InfoForm(request.POST or None, request.FILES or None, instance=info)
    if form.is_valid():
        form.save()
        if request.is_ajax():
            time.sleep(3)
            return HttpResponse('Changes have been saved')
        else:
            return redirect('home')
    context = {
        'form': form,
    }
    return render(request, 'edit_info.html', context)
