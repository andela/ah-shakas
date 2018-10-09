from rest_framework import status
from rest_framework.reverse import reverse as API_Reverse
from rest_framework.test import APITestCase, APIClient

from authors.apps.articles.tests.base_tests import BaseTest


class CommentsTests(BaseTest):
    """
    Comments test cases
    """
    
    def create_comment(self):
        slug = self.create_article()
        url = API_Reverse('articles:comments', {slug: 'slug'})
        response = self.client.post(url, self.comment, format='json')
        return response, url

    def test_can_create_comment(self):
        """
        Test if authenticated users can create comments
        """
        response, url  = self.create_comment()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_unauthenticated_user_cannot_comment(self):
        """
        Test unauthenticated users cannot create comments
        """
        # use a valid user to create article
        slug = self.create_article()
        url = API_Reverse('articles:comments', {slug: 'slug'})
        response = self.unauthorised_client.post(url, self.comment, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_users_can_view_comments(self):
        """
        Test users can view all comments
        """
        response, url = self.create_comment()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_unauthorised_users_can_view_comments(self):
        """
        Test any user can view somments
        """
        response, url = self.create_comment()
        response = self.unauthorised_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_can_view_single_comment(self):
        """
        Test users can view a single comment
        """
        slug = self.create_article()
        url = API_Reverse('articles:comments', {slug: 'slug'})
        response = self.client.post(url, self.comment, format='json')
        id = response.data['id']
        url = API_Reverse('articles:comment-details', {slug: 'slug', id: 'id'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_can_delete_comment(self):
        """
        Test authenticated users can delete their comments
        """
        slug = self.create_article()
        url = API_Reverse('articles:comments', {slug: 'slug'})
        response = self.client.post(url, self.comment, format='json')
        id = response.data['id']
        url = API_Reverse('articles:comment-details', {slug: 'slug', id: 'id'})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_unauthenticated_user_cannot_delete_comment(self):
        """
        Test non-owners of comments cannot delete comments
        """
        slug = self.create_article()
        url = API_Reverse('articles:comments', {slug: 'slug'})
        response = self.client.post(url, self.comment, format='json')
        id = response.data['id']
        url = API_Reverse('articles:comment-details', {slug: 'slug', id: 'id'})
        response = self.unauthorised_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_update_comment(self):
        """
        Test authenticated users can update their comments
        """
        slug = self.create_article()
        url = API_Reverse('articles:comments', {slug: 'slug'})
        response = self.client.post(url, self.comment, format='json')
        id = response.data['id']
        url = API_Reverse('articles:comment-details', {slug: 'slug', id: 'id'})
        response = self.client.put(url, data={'comment': {'body': 'New comment'}}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_unauthenticated_user_cannot_update_comment(self):
        """
        Test non-owners of comments cannot update comments
        """
        slug = self.create_article()
        url = API_Reverse('articles:comments', {slug: 'slug'})
        response = self.client.post(url, self.comment, format='json')
        id = response.data['id']
        url = API_Reverse('articles:comment-details', {slug: 'slug', id: 'id'})
        response = self.unauthorised_client.put(url, data={'comment': {'body': 'New comment'}}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
