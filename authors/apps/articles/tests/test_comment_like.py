import copy
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse as api_reverse
from rest_framework import status

from authors import settings
from .base_tests import BaseTest

class LikesDislikesTests(BaseTest):
    """
    Likes test cases
    """

    def setUp(self):
        """
        Setup the user, rating and article for the tests
        """
        super().setUp()
        self.like =  {
            "comment_likes":True
        }


        self.second_user = {
            "user": {
                "username": "seconduser",
                "password": "password134",
                "email": "pass@g.com"
            }
        }
        
        self.author_token = self.create_and_login_user()
        # self.article_slug = self.create_article(token=self.author_token)
        self.slug = self.create_article()
        self.id = self.create_comment()

        self.article_url = api_reverse('articles:comment-details', {self.slug:'slug' ,self.id: 'id'})
        self.like_url = api_reverse('articles:comment-like', {self.slug:'slug' ,self.id: 'id'})

    def create_like(self, like=None):
        if not like:
            like = self.like
        response = self.client.post(
            self.like_url, 
            like, 
            'json', 
            HTTP_AUTHORIZATION=self.create_and_login_user(self.second_user)
        )

        return response


    def test_user_cant_like_own_article(self):
        """
        Test a user liking their own article
        """
        response = self.client.post(self.like_url, self.like, format='json', HTTP_AUTHORIZATION=self.author_token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_can_create_like(self):
        """
        Test if authenticated users can create comments
        """      
        response = self.create_like()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_article_does_not_exist(self):
        """
        Test liking an article that does not exist
        """
        response = self.client.post('/api/articles/slug/like/',
            self.like,
            HTTP_AUTHORIZATION=self.create_and_login_user(self.second_user),
            format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_cant_like_article_twice(self):
        """
        Test a user cant like an article twice
        """
        self.create_like()
        response = self.create_like()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_like_invalid_payload(self):
        """
        Test validity of the passed payload
        """
        response = self.client.post(self.like_url,
            {"likes":"hjvajkv"},
            HTTP_AUTHORIZATION=self.create_and_login_user(self.second_user),
            format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) 

    def test_unauthenticated_user_cannot_like_article(self):
        """
        Test unauthenticated user cannot like an article
        """
        self.client.credentials(HTTP_AUTHORIZATION='')
        response = self.client.post(self.like_url,
            {"likes":"hjvajkv"},
            format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_like(self):
        """
        Test deletion of a like
        """
        self.create_like()
        response = self.client.delete(self.like_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_non_existent_like(self):
        """
        Test deletion of a non-existant like
        """
        response = self.client.delete(self.like_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_delete_like_unauthenticated_user(self):
        """
        Test unauthenticated user cannot delete like
        """
        self.client.credentials(HTTP_AUTHORIZATION='')
        self.client.post(self.like_url, self.like, format='json', HTTP_AUTHORIZATION=self.author_token)
        response = self.client.delete(self.like_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
