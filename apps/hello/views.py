import json
import time
import os
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest
from django.core import serializers
from .models import Info, WebRequest
from .forms import InfoForm


def home(request):
    info = Info.objects.first()
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


@login_required()
def edit_info(request):
    try:
        info = Info.objects.first()
        if not info:
            return HttpResponse('No records in database')
        form = InfoForm(request.POST or None, request.FILES or None, instance=info)
        previous_photo = info.photo.path

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

        elif form.errors:
            errors_dict = {}
            for error in form.errors:
                e = form.errors[error]
                errors_dict[error] = unicode(e)
            return HttpResponseBadRequest(json.dumps(errors_dict))

        else:
            context = {
                'form': form,
            }
            return render(request, 'edit_info.html', context)
    except Exception, e:
                print str(e)
