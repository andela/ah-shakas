from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from authors.apps.authentication.models import User
from django.core import mail
from django.urls import reverse
from authors.apps.authentication.token import generate_token


class AccountVerification(TestCase):
    """
    Test for account verification
    """

    def setUp(self):
        """
        Define globals.
        """
        self.client = APIClient()
        self.registration_url = reverse('authentication:sign-up')
        self.user_data = {
            "user": {
                "username": "shaka",
                "email": "shaka@domain.com",
                "password": "0@secure"
            }
        }

    def test_confirmation_mail(self):
        """
        Test for sending of confirmation mail
        """
        # More on Outbox objects can be found in the following link
        # https://docs.djangoproject.com/en/dev/topics/email/#django.core.mail.EmailMessage

        self.client.post(self.registration_url, self.user_data, format='json')
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("You will need to confirm your email to start using Author heaven", mail.outbox[0].body)

    def test_account_verification(self):
        """
        Test for successful account verification
        """
        self.client.post(self.registration_url, self.user_data, format='json')
        user = self.user_data['user']
        token = generate_token(user['username'])
        response = self.client.get(reverse("authentication:verify", args=[token]))
        user = User.objects.get(username=user['username'])
        self.assertTrue(user.is_active)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
