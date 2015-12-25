import json
from django.core.urlresolvers import reverse
from models import WebRequest


class SaveRequest(object):
    def process_request(self, request):
        """
        Saves each request to db
        """
        if not request.path == reverse('upd_requests'):
            priority_mark = '1' if request.method == 'POST' else '0'
            WebRequest(
                host=request.get_host(),
                path=request.path,
                method=request.method,
                user_agent=request.META.pop('HTTP_USER_AGENT', None),
                get=None if not request.GET else json.dumps(request.GET),
                post=json.dumps(request.POST),
                is_secure=request.is_secure(),
                is_ajax=request.is_ajax(),
                user=request.user,
                priority=priority_mark
            ).save()
