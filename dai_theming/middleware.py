from django.shortcuts import redirect

class CheckUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if '/groups/' in request.path and not request.user.is_authenticated:
            return redirect('/account/login/')
        response = self.get_response(request)
        return response