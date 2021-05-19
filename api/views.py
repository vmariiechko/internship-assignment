from django.shortcuts import redirect
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .models import SMS
from .serializers import SMSListSerializer, SMSDetailSerializer


def redirect_view(request):
    """Redirects user from main page '/' to '/api/'."""

    response = redirect('/api/')
    return response


class APIOverview(APIView):
    """General overview of all available endpoints."""

    api_urls = {
        'SMS List': '/smses/',
        'SMS Detail': '/smses/{id}/',
    }

    def get(self, request):
        return Response(self.api_urls)


class SMSList(generics.ListAPIView):
    """List API view for all SMSes."""

    queryset = SMS.objects.all()
    serializer_class = SMSListSerializer
    permission_classes = [AllowAny]


class SMSDetail(generics.RetrieveAPIView):
    """Detail API view for single SMS."""

    queryset = SMS.objects.all()
    serializer_class = SMSDetailSerializer
    permission_classes = [AllowAny]
