from django.shortcuts import redirect, get_object_or_404

from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import SMS
from .permissions import IsAuthenticatedOrViewOnly
from .serializers import SMSListSerializer, SMSDetailSerializer


def redirect_view(request):
    """
    Redirects user to API root page.
    """

    response = redirect('/api/')
    return response


class APIRoot(APIView):
    """
    General overview of API endpoints.
    """

    api_urls = {
        'SMS List': 'GET /smses/',
        'SMS Create': 'POST /smses/',
        'SMS Detail': 'GET /smses/{id}/',
        'SMS Update': 'PUT /smses/{id}/',
        'SMS Delete': 'DELETE /smses/{id}/',
    }

    def get(self, request):
        return Response(self.api_urls)


class SMSViewSet(viewsets.ViewSet):
    """
    A viewset for listing all SMSes and creating a new SMS.
    """

    permission_classes = [IsAuthenticatedOrViewOnly]
    http_method_names = ['get', 'post']

    def list(self, request):
        """Lists SMSes with all data."""

        queryset = SMS.objects.all()
        serializer = SMSListSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        """Creates a new SMS."""

        self.check_permissions(request)
        serializer = SMSDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['author'] = request.user
            serializer.validated_data['views_count'] = 0
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SMSDetailViewSet(viewsets.ViewSet):
    """
    A viewset for interacting with single SMS.
    """

    permission_classes = [IsAuthenticatedOrViewOnly]
    http_method_names = ['get', 'put', 'delete']
    lookup_field = 'sms_id'

    def get_object(self, sms_id):
        """Gets SMS object by id."""

        queryset = SMS.objects.all()
        return get_object_or_404(queryset, pk=sms_id)

    def retrieve(self, request, sms_id=None, *args, **kwargs):
        """Retrieves SMS by id and increments the number of views."""

        sms = self.get_object(sms_id)
        self.check_object_permissions(request, sms)
        data = {
            "views_count": sms.views_count + 1
        }
        serializer = SMSDetailSerializer(instance=sms, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, sms_id=None, *args, **kwargs):
        """Updates SMS by id and sets the number of views to zero."""

        sms = self.get_object(sms_id)
        self.check_object_permissions(request, sms)
        data = {
            'message': request.data.get('message'),
            'views_count': 0,
        }
        serializer = SMSDetailSerializer(instance=sms, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, sms_id=None, *args, **kwargs):
        """Deletes SMS by id."""

        sms = self.get_object(sms_id)
        self.check_object_permissions(request, sms)
        sms.delete()
        return Response(status=status.HTTP_200_OK)
