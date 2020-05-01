from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')


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
            'name': 'test name'
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
            'name': 'test name'
        }
        create_user(**payload)
        response = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """ test the password must be more than 5 characters"""
        payload = {
            'email': 'test@email.com',
            'password': 'rd',
            'name': 'test name'
        }

        response = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        user_exits = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exits)
