from rest_framework.routers import SimpleRouter
from .views import SMSViewSet, SMSDetailViewSet

app_name = 'smses'

# Generate all URL endpoints for SMSes
router = SimpleRouter()
router.register('', SMSViewSet, basename="sms")
router.register('', SMSDetailViewSet, basename="sms")
urlpatterns = router.urls
