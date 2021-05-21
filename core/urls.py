"""core URL Configuration

The `urlpatterns` list routes URLs to views.
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from api.views import redirect_view, APIRoot

urlpatterns = [
    path('', redirect_view),
    path('api/', APIRoot.as_view()),
    path('api/smses/', include('api.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('accounts/profile/', redirect_view),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('admin/', admin.site.urls),
]
