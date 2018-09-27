from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse as api_reverse
from rest_framework import status


from .models import UserManager


class AuthenticationTest(APITestCase):
    def setUp(self):
        self.url = api_reverse('authentication:user-registration')
        self.user =  { 
            'user' : { 
                'username': 'Jane Doe', 
                'email': 'jane@doe.com', 
                'password': 'janedoe123', 
            }
        }

    def test_user_can_signup(self):
        response = self.client.post(self.url, self.user, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn(b'jane@doe.com', response.content)
    
    def test_user_cannot_signup_without_email(self):
        del self.user['user']['email']
        response = self.client.post(self.url, self.user, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(b'Email is required', response.content)

    def test_user_cannot_signup_with_invalid_email(self):
        self.user['user']['email'] = 'NOT-AN-EMAIL'
        response = self.client.post(self.url, self.user, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(b'Enter a valid email address', response.content)

    def test_user_cannot_signup_without_password(self):
        del self.user['user']['password']
        response = self.client.post(self.url, self.user, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(b'Password is required', response.content)

    def test_user_cannot_signup_with_short_password(self):
        self.user['user']['password'] = 'abc'
        response = self.client.post(self.url, self.user, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(b'Password must have at least 8 characters', 
                response.content)

    def test_user_cannot_signup_without_alphanumeric_password(self):
        self.user['user']['password'] = 'abcdefghijk'
        response = self.client.post(self.url, self.user, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(b'Password must have a number and a letter', 
                response.content)

    def test_user_cannot_signup_without_username(self):
        del self.user['user']['username']
        response = self.client.post(self.url, self.user, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(b'Username is required', response.content)

    def test_user_cannot_signup_with_short_username(self):
        self.user['user']['username'] = 'abc'
        response = self.client.post(self.url, self.user, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(b'Username must have at least 4 characters', 
                response.content)

