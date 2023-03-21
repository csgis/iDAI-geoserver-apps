from django.shortcuts import redirect
from django.http import Http404

class CheckUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if ('/groups/' in request.path or '/people/' in request.path) \
                and not request.user.is_authenticated:
            return redirect('/account/login/?next=/groups')
        response = self.get_response(request)
        return response


class BlockSignupMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'POST' and request.path == '/account/signup/':
            raise Http404("Page not found")

        response = self.get_response(request)
        return response
