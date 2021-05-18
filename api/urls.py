from django.urls import path, include
from .views import APIOverview, InitialView

app_name = 'api'

urlpatterns = [
    path('', APIOverview.as_view(), name="api-overview"),
    path('initial/', InitialView.as_view(), name="initial"),
]
