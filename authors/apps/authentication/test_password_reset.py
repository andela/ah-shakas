from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse as api_reverse
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .models import User

class TestEmailSent(APITestCase):
    """
    test for class to send password reset link to email
    """
    def setUp(self):
        """
        set up method to test email to be sent endpoint
        """
        self.url = api_reverse('authentication:email_password')
        self.register_url = api_reverse('authentication:user-registration')
        self.user =  {
            'user' : {
                'username': 'kevin',
                'email': 'koechkevin92@gmail.com',
                'password': 'Kev12345'
            }
        }
        self.client.post(self.register_url, self.user, format="json")

    def test_unregistered_email(self):
        """
        case where unregistered user tries to request a password
        """
        response = self.client.post(self.url, data={"email":"koechkevin@gmail.com"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.content, b'{"user": {"message": "The Email provided is not registered"}}')

    def test_email_field_missing(self):
        """
        case where a user provides no parameters on request body
        """
        response = self.client.post(self.url, data={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.content, b'{"user": {"message": "email field should be provided"}}')

    def test_empty_email(self):
        """
        case where a user provides empty email field
        """
        response = self.client.post(self.url, data={"email":""})
        self.assertEqual(response.content, b'{"user": {"message": "email field cannot be empty"}}')
        self.assertEqual(response.status_code, 400)

    def test_successful_email(self):
        """
        case where a user provides valid credentials
        """
        response = self.client.post(self.url, data={"email":"koechkevin92@gmail.com"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, b'{"user": {"message": "We\'ve sent a password reset link to your email"}}')

class TestPasswordReset(APITestCase):
    """
    test link to reset password
    """
    def setUp(self):
        """
        set up method to test password reset endpoint
        """
        self.user =  {
            'user' : {
                'username': 'kevin',
                'email': 'koechkevin92@gmail.com',
                'password': 'Kev12345'
            }
        }
        self.register_url = api_reverse('authentication:user-registration')
        self.client.post(self.register_url, self.user, format="json")
        token_generator = PasswordResetTokenGenerator()
        user_object = User.objects.filter(email='koechkevin92@gmail.com').first()
        token = token_generator.make_token(user_object)
        self.url = api_reverse('authentication:password_reset')+'?token='+token
        #self.url = 'http://127.0.0.1:8000/api/users/password_reset?token='+token

    def test_invalid_token(self):
        """
        test a case where an invalid token is provided or token has been tampered with
        """
        response = self.client.put(self.url+'r', data={"email":"koechkevin92@gmail.com"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.content, b'{"user": {"message": "invalid token"}}')

    def test_valid_token_password(self):
        """
        test a case where valid token is provided
        """
        data = {
            "email":"koechkevin92@gmail.com",
            "password":"Kev12345"
        }
        response = self.client.put(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, b'{"user": {"message": "password successfully changed"}}')

    def test_used_token(self):
        """
        a case where user tries to reuse a token
        """
        data = {
            "email":"koechkevin92@gmail.com",
            "password":"Kev12345"
        }
        data2 = {
            "email":"koechkevin92@gmail.com",
            "password":"Kevinkoech"
        }
        response1 = self.client.put(self.url, data=data)
        response2 = self.client.put(self.url, data=data2)
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(response1.content, b'{"user": {"message": "password successfully changed"}}')
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response2.content, b'{"user": {"message": "invalid token"}}')

    def test_short_password(self):
        """
        a case where user provides a short password on reset
        """
        data = {
            "email":"koechkevin92@gmail.com",
            "password":"Kev123"
            }
        response = self.client.put(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.content, b'{"user": {"password": ["Password must have at least 8 characters", "Password must have a number and a letter"]}}')