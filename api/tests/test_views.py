from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from ..models import SMS
from ..serializers import SMSListSerializer, SMSDetailSerializer


class GetSMSTestCaseSetUp(APITestCase):
    """
    Set up module for retreiveng SMS test cases.
    """

    def setUp(self):
        """Create 4 SMSes and users."""

        for i in range(1, 5):
            user = User.objects.create_user(
                username=f'user{i}', password='123456789')
            SMS.objects.create(
                author_id=i, message=f'The {i}th message', views_count=i)


class ModifySMSTestCaseSetUp(APITestCase):
    """
    Set up module for modifying SMS test cases.
    """

    def setUp(self):
        """Create single SMS and authenticated user."""

        self.user = User.objects.create_user(
            username='user', password='123456789')
        self.client.login(username='user', password='123456789')
        self.sms = SMS.objects.create(
            author_id=1, message=f'Mesage wih incrrect speling', views_count=5)


class GetAllSMSesTestCase(GetSMSTestCaseSetUp):
    """
    Test module for GET all SMSes API.
    """

    def test_get_all_smses(self):
        # Request all SMSes
        url = reverse('smses:sms-list')
        response = self.client.get(url)

        # Get data from db
        smses = SMS.objects.all()
        serializer = SMSListSerializer(smses, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetSingleSMSTestCase(GetSMSTestCaseSetUp):
    """
    Test module for GET single SMS API.
    """

    def test_get_valid_single_sms(self):
        # Request existed SMS
        sms_id = 2
        url = reverse('smses:sms-detail', kwargs={'sms_id': sms_id})
        response = self.client.get(url)

        # Test received SMS
        sms = SMS.objects.get(pk=sms_id)
        serializer = SMSDetailSerializer(sms)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_sms(self):
        # Get not existed SMS
        url = reverse('smses:sms-detail', kwargs={'sms_id': 15})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_sms_view_count(self):
        # View first SMS 5 times
        url = reverse('smses:sms-detail', kwargs={'sms_id': 1})
        for i in range(4):
            self.client.get(url)
        response = self.client.get(url)

        # Check the number of views
        self.assertEqual(response.data, {'message': 'The 1th message', 'views_count': 6})
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CreateSMSTestCase(APITestCase):
    """
    Test module for POST SMS API.
    """

    url = reverse('smses:sms-list')

    def setUp(self):
        # Create and authenticate the user
        self.user = User.objects.create_user(
            username=f'user', password='123456789')
        self.client.login(username='user', password='123456789')

    def test_create_sms_authenticated(self):
        # Create valid SMS as an authenticated user
        data = {'message': "That's awesome!"}
        response = self.client.post(self.url, data)
        self.assertIsNotNone(SMS.objects.get(id=1))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_sms_views_count(self):
        # Create valid SMS as an authenticated user but with a defined number of views
        data = {
            'message': "That's awesome!",
            'views_count': 50,              # New SMS must have 0 views
        }
        response = self.client.post(self.url, data)
        serializer = SMSDetailSerializer(SMS.objects.get(id=1))
        self.assertEqual(serializer.data['views_count'], 0)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_sms_un_authenticated(self):
        # Try to authenticate not existed user
        self.client.force_authenticate(user=None)

        # Try to create SMS
        data = {'message': 'Hacked!!'}
        response = self.client.post(self.url, data)
        self.assertFalse(SMS.objects.all())
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_sms_bad_request(self):
        # Create and test bad request
        data = {'incorrect_data': "That's 400 status"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateSingleSMSTestCase(ModifySMSTestCaseSetUp):
    """
    Test module for PUT SMS API.
    """

    url = reverse('smses:sms-detail', kwargs={"sms_id": 1})

    def test_update_sms_authenticated_owner(self):
        # Update and test SMS
        data = {'message': "Message with correct spelling"}
        response = self.client.put(self.url, data)
        serializer = SMSDetailSerializer(SMS.objects.get(pk=1))
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_sms_views_count(self):
        # Try to change the number of views
        data = {
            'message': "Message with correct spelling",
            'views_count': 100,             # Updated SMS must have 0 views
        }
        response = self.client.put(self.url, data)
        serializer = SMSDetailSerializer(SMS.objects.get(pk=1))
        self.assertEqual(response.data['views_count'], 0)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_sms_authenticated_not_owner(self):
        # Authenticate another user
        not_author = User.objects.create_user(
            username='not_author', password='123456789')
        self.client.force_authenticate(user=not_author)

        # Try to update SMS as not author
        data = {'message': "Guest modified the SMS of the owner!"}
        response = self.client.put(self.url, data)
        self.assertEqual(response.data['detail'], 'Modifying SMSes is allowed to the author only')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_sms_un_authenticated(self):
        # Try to authenticate not existed user
        self.client.force_authenticate(user=None)

        # Try to update SMS
        data = {'message': "Hacked!!"}
        response = self.client.put(self.url, data)
        # Test SMS before and after request
        serializer1 = SMSDetailSerializer(SMS.objects.get(pk=1))
        serializer2 = SMSDetailSerializer(self.sms)
        self.assertEqual(serializer1.data, serializer2.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_sms_bad_request(self):
        # Try to update and test bad request
        data = {'incorrect_data': "That's 400 status"}
        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteSingleSMSTestCase(ModifySMSTestCaseSetUp):
    """
    Test module for DELETE SMS API.
    """

    url = reverse('smses:sms-detail', kwargs={"sms_id": 1})

    def test_delete_sms_authenticated_owner(self):
        # Delete and test SMS
        response = self.client.delete(self.url)
        self.assertFalse(SMS.objects.all())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_sms_authenticated_not_owner(self):
        # Authenticate another user
        not_author = User.objects.create_user(
            username='not_author', password='123456789')
        self.client.force_authenticate(user=not_author)

        # Try to delete SMS as not author
        response = self.client.delete(self.url)
        self.assertEqual(response.data['detail'], 'Modifying SMSes is allowed to the author only')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_sms_un_authenticated(self):
        # Try to authenticate not existed user
        self.client.force_authenticate(user=None)

        # Try to delete SMS
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class JWTAuthenticationTest(APITestCase):
    """
    Test module for JWT authentication API.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username=f'user', password='123456789')
        # Request JWT tokens
        url = '/api/token/'
        data = {
            'username': 'user',
            'password': '123456789',
        }
        self.response = self.client.post(url, data)

    def test_valid_jwt_authentication(self):
        self.assertIsNotNone(self.response.data)
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)
        self.create_sms_using_access_token_test(self.response.data['access'])

    def test_refresh_token_usage(self):
        url = '/api/token/refresh/'
        data = {
            'refresh': self.response.data['refresh']
        }
        response = self.client.post(url, data)
        self.assertIsNotNone(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.create_sms_using_access_token_test(response.data['access'])

    def create_sms_using_access_token_test(self, access_token):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + access_token)
        url = reverse('smses:sms-list')
        data = {'message': "Authorized using JWT!"}
        response = self.client.post(url, data)
        self.assertIsNotNone(SMS.objects.get(id=1))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_jwt_authentication(self):
        # Send invalid user data
        url = '/api/token/'
        data = {
            'username': 'non-existing',
            'password': 'incorrect_psw',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.data['detail'], 'No active account found with the given credentials')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class GetAPIRootTest(APITestCase):
    """
    Test module for GET APIRoot API.
    """

    api_urls = {
        'SMS List': 'GET /smses/',
        'SMS Create': 'POST /smses/',
        'SMS Detail': 'GET /smses/{id}/',
        'SMS Update': 'PUT /smses/{id}/',
        'SMS Delete': 'DELETE /smses/{id}/',
    }

    def test_get_api_root(self):
        # Get API URLs
        response = self.client.get('/api/')
        self.assertEqual(response.data, self.api_urls)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_redirect_to_api_root(self):
        # Get redirection from '/' to the root API page
        response = self.client.get('/')
        self.assertEqual(response.url, '/api/')
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
