from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework import status
from .models import Profile


from authors.apps.authentication.models import UserManager


class ProfileTest(APITestCase):
    """
    User authentication test cases
    """
    def setUp(self):
        """
        Method for setting up user
        """
        self.user =  { 
            "user":{
                    'username': 'janeDoe', 
                    'email': 'jane@doe.com', 
                    'password': 'janedoe123', 
            }
        }

        self.user_2 =  { 
            "user":{
                    'username': 'jane1Doe', 
                    'email': 'jane3@doe.com', 
                    'password': 'jane3doe123', 
            }
        }

        self.url_register = reverse('authentication:user-registration')
        reg_res=self.client.post(self.url_register,self.user_2,format='json')
        
    
    def registration(self):
        response = self.client.post(self.url_register, self.user, format='json')
        token=response.data['token']
        return token

    def test_get_followers_without_auth(self):
        data={}
        url=reverse("profiles:followers", kwargs={"username": self.user_2['user']['username']})
        response = self.client.get(url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)

    def test_get_following_without_auth(self):
        data={}
        url=reverse("profiles:following", kwargs={"username": self.user['user']['username']})
        response = self.client.get(url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)

    def test_get_following_with_auth(self):
        token=self.registration()
        data={}
        self.client.credentials(HTTP_AUTHORIZATION=token)
        url=reverse("profiles:following", kwargs={"username": self.user['user']['username']})
        response = self.client.get(url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_get_followers_with_auth(self):
        token=self.registration()
        data={}
        self.client.credentials(HTTP_AUTHORIZATION=token)
        url=reverse("profiles:followers", kwargs={"username": self.user['user']['username']})
        response = self.client.get(url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_follow_with_auth(self):
        token=self.registration()
        data={}
        self.client.credentials(HTTP_AUTHORIZATION=token)
        url=reverse("profiles:follow", kwargs={"username": self.user_2['user']['username']})
        response = self.client.post(url,data,format='json')
        self.assertEqual(response.status_code,201)

    

    def test_follow_without_auth(self):
        data={}
        url=reverse("profiles:follow", kwargs={"username": self.user_2['user']['username']})
        response = self.client.post(url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)

    def test_unfollow_with_auth(self):
        token=self.registration()
        data={}
        self.client.credentials(HTTP_AUTHORIZATION=token)
        url=reverse("profiles:follow", kwargs={"username": self.user_2['user']['username']})
        response = self.client.delete(url,data,format='json')
        self.assertEqual(response.status_code,200)

    def test_unfollow_without_auth(self):
        data={}
        url=reverse("profiles:follow", kwargs={"username": self.user_2['user']['username']})
        response = self.client.delete(url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)