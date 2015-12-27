import json
import os
import time
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest
from django.core import serializers
from .models import Info, WebRequest
from .forms import InfoForm
import signals


def home(request):
    info = Info.objects.first()
    context = {'info': info}
    return render(request, 'home.html', context)


def requests(request):
    return render(request, 'requests.html')


def upd_requests(request):
    if not request.is_ajax():
        return HttpResponse('Not ajax request')

    sort_flag = int(request.GET.get('sort_flag'))
    print type(sort_flag)
    if sort_flag >= 0:
        last_10_reqs = WebRequest.objects.filter(priority=sort_flag).order_by('-id')[:10]
    else:
        last_10_reqs = WebRequest.objects.all().order_by('-id')[:10]


    if last_10_reqs:
        data = serializers.serialize("json", last_10_reqs)
        return HttpResponse(data, content_type='application/json')

    return HttpResponse('No records in database')


@login_required()
def edit_info(request):
    info = Info.objects.first()
    if not info:
        return HttpResponse('No records in database')
    form = InfoForm(request.POST or None, request.FILES or None, instance=info)
    previous_photo = info.photo.path

    if not form.is_valid() and not form.errors:
        context = {
            'form': form,
        }
        return render(request, 'edit_info.html', context)

    if form.is_valid():
        form.save()
        try:
            if previous_photo != info.photo.path:
                os.remove(previous_photo)
        except Exception, e:
            print str(e)
        if request.is_ajax():
            time.sleep(3)
            return HttpResponse('Changes have been saved')
        else:
            return redirect('home')

    errors_dict = {}
    for error in form.errors:
        e = form.errors[error]
        errors_dict[error] = unicode(e)
    return HttpResponseBadRequest(json.dumps(errors_dict))
