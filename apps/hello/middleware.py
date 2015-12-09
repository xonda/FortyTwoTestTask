import json
from models import WebRequest


class SaveRequest(object):
    def process_request(self, request):
        """
        Saves each request to db
        """
        if not request.path == '/upd_requests':
            WebRequest(
                host=request.get_host(),
                path=request.path,
                method=request.method,
                user_agent=request.META.pop('HTTP_USER_AGENT', None),
                get=None if not request.GET else json.dumps(request.GET),
                post=json.dumps(request.POST),
                is_secure=request.is_secure(),
                is_ajax=request.is_ajax(),
                user=request.user
            ).save()

        return None
