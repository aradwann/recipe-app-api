from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """test creating a new user with email is successful"""
        email = "testemai@email.com"
        password = "testpassword"
        user = get_user_model().objects.create_user(
            email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """test the email for a new user is normalised"""
        email = "testemail@EMAIL.COM"
        user = get_user_model().objects.create_user(
            email=email, password="testpassword")

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email=None, password="testpassword")

    def test_create_new_superuser(self):
        """test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            email="testemail@email.com", password="testpassword")

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
