from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework. response import Response


def redirect_view(request):
    """Redirects user from main page '/' to '/api/'."""

    response = redirect('/api/')
    return response


class APIOverview(APIView):
    api_urls = {
        'Initial url': '/initial/',
    }

    def get(self, request):
        return Response(self.api_urls)


class InitialView(APIView):

    def get(self, request):
        return Response("Initial view")
