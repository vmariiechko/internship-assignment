from django.urls import path
from .views import SMSList, SMSDetail

app_name = 'smses'

urlpatterns = [
    path('', SMSList.as_view(), name="sms-list"),
    path('<str:pk>/', SMSDetail.as_view(), name="sms-detail"),
]
