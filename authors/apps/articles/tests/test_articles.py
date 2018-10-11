from rest_framework.reverse import reverse as API_Reverse
from rest_framework import status
import json

from authors.apps.articles.tests.base_tests import ArticlesBaseTest


class ArticleTests(ArticlesBaseTest):
  
    def test_anyone_can_get_articles(self):
        """This method tests is anyone can access articles endpoint"""
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logged_in_user_view_articles(self):
        """This method tests if a logged in user can access articles"""
        token = self.create_user()
        response = self.client.get(
            self.url, format='json', headers={'Authorization': token})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_can_create_article(self):
        """This method tests if a user can create an article"""
        token = self.create_user()
        response = self.client.post(self.url, self.article, format='json', HTTP_AUTHORIZATION=token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_create_articles_unauthorized_user(self):
        """This method checks if an unauthorized user cannot create an article"""
        response = self.client.post(self.url, self.article, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_access_single_article(self):
        """This method checks if a user can access a single article"""
        url = self.single_article_details()
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cannot_create_without_title(self):
        """This method tests if a user can post without a title"""
        self.article['article'].pop('title')
        token = self.create_user()
        response = self.client.post(self.url, self.article, format='json', HTTP_AUTHORIZATION=token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_can_update(self):
        """This method checks if a user can update an existing articles"""
        token = self.create_user()
        response = self.client.post(self.url, self.article, format='json', HTTP_AUTHORIZATION=token)
        slug = response.data['slug']
        url = API_Reverse('articles:article-details', {slug: 'slug'})
        r = self.client.put(url, data={"article": {"title": "Updated Title", "body": "Updated body"}}, format='json', HTTP_AUTHORIZATION=token)
        self.assertIn("Updated Title", json.dumps(r.data))
        self.assertEqual(r.status_code, status.HTTP_200_OK)

    def test_unauthorised_user_update(self):
        """This method tests if unauthorized user can update existing articles"""
        url = self.single_article_details()
        r = self.client.put(url, data={"article": {"title": "Updated Title", "body": "Updated body"}}, format='json')
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_delete(self):
        """This method tests if a user can delete articles"""
        token = self.create_user()
        response = self.client.post(self.url, self.article, format='json', HTTP_AUTHORIZATION=token)
        slug = response.data['slug']
        url = API_Reverse('articles:article-details', {slug: 'slug'})
        r = self.client.delete(url, format='json', HTTP_AUTHORIZATION=token)
        self.assertEqual(r.status_code, status.HTTP_204_NO_CONTENT)

    def test_unauthorised_user_delete(self):
        """This method tests if a non owner can delete an article"""
        url = self.single_article_details()
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    
