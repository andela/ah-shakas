
from rest_framework import status
from rest_framework.reverse import reverse as API_Reverse
from rest_framework.test import APITestCase, APIClient

from authors.apps.articles.tests.base_tests import BaseTest


class CommentsTests(BaseTest):
    article_url = '/api/articles/gloria-2/comments'
    
    def create_comment(self):
        slug = self.create_article()
        url = API_Reverse('articles:comments', {slug: 'slug'})
        response = self.client.post(url, self.comment, format='json')
        return response, url

    def test_can_create_comment(self):
        response, url  = self.create_comment()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_unauthenticated_user_cant_comment(self):
        # use a valid user to create article
        slug = self.create_article()
        url = API_Reverse('articles:comments', {slug: 'slug'})
        response = self.unauthorised_client.post(url, self.comment, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_can_view_comments(self):
        response, url = self.create_comment()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_unauthorised_can_view_comments(self):
        response, url = self.create_comment()
        response = self.unauthorised_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_can_view_single_comment(self):
        slug = self.create_article()
        url = API_Reverse('articles:comments', {slug: 'slug'})
        response = self.client.post(url, self.comment, format='json')
        id = response.data['id']
        url = API_Reverse('articles:comment-details', {slug: 'slug', id: 'id'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


