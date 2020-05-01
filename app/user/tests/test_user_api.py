from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the public users API"""

    def setUp(self):
        self.client = APIClient()

    def create_valid_user_success(self):
        """creating a user with a valid payload is successful"""
        payload = {
            'email': 'test@email.com',
            'password': 'testpassword',
        }
        response = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**response.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', response.data)

    def test_user_exists(self):
        """ test creating a user that already exists fails"""
        payload = {
            'email': 'test@email.com',
            'password': 'testpassword',
        }
        create_user(**payload)
        response = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """ test the password must be more than 5 characters"""
        payload = {
            'email': 'test@email.com',
            'password': 'rd',
        }
        response = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        user_exits = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exits)

    def test_create_token_for_user(self):
        """ Test that token created for the user """
        payload = {
            'email': 'test@email.com',
            'password': 'password',
        }
        create_user(**payload)
        response = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """ test that token is not created
        if invalid credentials is provided"""
        payload1 = {
            'email': 'test@email.com',
            'password': 'password',
        }
        create_user(**payload1)
        payload2 = {
            'email': 'tedsadst@email.com',
            'password': 'pasfadsword',
        }
        response = self.client.post(TOKEN_URL, payload2)
        self.assertNotIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_no_token(self):
        """ test that token is not created if user doesn't exist"""
        payload = {
            'email': 'test@email.com',
            'password': 'password',
        }
        response = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """ test that email and password is required for creating a token"""
        payload1 = {
            'email': 'test@email.com',
            'password': 'password',
        }
        create_user(**payload1)
        payload2 = {
            'email': 'test@email.com',
            'password': '',
        }
        response = self.client.post(TOKEN_URL, payload2)
        self.assertNotIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """ test that authentication is required for users"""
        response = self.client.get(ME_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """ test requests that require authentication """

    def setUp(self):
        payload = {
            'email': 'test@email.com',
            'password': 'password',
        }
        self.user = create_user(**payload, name='name')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """ test retrieving profile for loggedin user"""
        response = self.client.get(ME_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data,
                         {
                             'email': self.user.email,
                             'name': self.user.name,
                         })

    def test_post_not_allowed(self):
        """ test that post is not allowed in the Me url"""
        response = self.client.post(ME_URL, {})

        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """ test updating a profile for an authenticated user """

        payload = {
            'name': 'newname',
            'email': 'test@email.com',
            'password': 'newpassword'
        }

        response = self.client.patch(ME_URL, payload)
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
