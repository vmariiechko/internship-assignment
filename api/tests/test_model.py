from django.test import TestCase
from django.contrib.auth.models import User
from ..models import SMS


class SMSCreateTest(TestCase):
    """
    Test module for SMS model.
    """

    def setUp(self):
        """Create a single SMS."""

        user = User.objects.create_user(
            username='user', password='123456789')
        SMS.objects.create(
            author_id=1, message='Can I use your laptop?', views_count=1)

    def test_sms_content(self):
        """Test all the SMS content."""

        sms = SMS.objects.get(id=1)
        author = f'{sms.author}'
        message = sms.message
        views_count = sms.views_count

        self.assertEqual(author, 'user')
        self.assertEqual(message, 'Can I use your laptop?')
        self.assertEqual(views_count, 1)
