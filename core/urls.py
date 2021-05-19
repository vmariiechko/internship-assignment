"""core URL Configuration

The `urlpatterns` list routes URLs to views.
"""
from django.contrib import admin
from django.urls import path, include
from api.views import redirect_view, APIRoot

urlpatterns = [
    path('', redirect_view),
    path('api/', APIRoot.as_view()),
    path('api/smses/', include('api.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('admin/', admin.site.urls),
]
