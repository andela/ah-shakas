import copy
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse as api_reverse
from rest_framework import status

from authors import settings


class RatingsTest(APITestCase):
    """
    Tests rating of an article
    """
    def setUp(self):
        """
        Setup the user, rating and article for the tests
        """
        self.rating =  {'rating' :{'rating': 4}}
        self.user = {
            'user': {
                'username': 'janeDoe',
                'email': 'jane@doe.com', 
                'password': 'secret123'
            }
        }
        self.article = {
            "article": {
                "title": "test article",
                "description": "This is test description",
                "body": "This is a test body"
            }
        }

    def create_user(self, user=None):
        """Creates a user and return their authenticated token"""
        if not user:
            user = self.user
        url = api_reverse('authentication:user-registration')
        resp = self.client.post(url, user, format='json')
        token = resp.data['token']

        return token

    def create_article(self, token):
        """Creates an article and returns its slug"""
        url = api_reverse('articles:articles')
        resp = self.client.post(url, self.article, format='json', HTTP_AUTHORIZATION=token)
        slug = resp.data['slug']

        return slug

    def article_rating_url(self, article_slug):
        """Returns the url endpoint for rating an article given its slug"""
        return api_reverse('articles:ratings', {article_slug: 'slug'})

    def test_user_can_rate_article(self):
        """A user can rate another user's article"""
        author_token = self.create_user()
        slug = self.create_article(author_token)
        url = self.article_rating_url(slug)

        rater = copy.deepcopy(self.user)
        rater['user'].update({
            'email': 'john@doe.com',
            'username': 'johnDoe'
        })

        rater_token = self.create_user(rater)
        resp = self.client.post(url, self.rating, 'json', HTTP_AUTHORIZATION=rater_token)

        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertIn(b'rating', resp.content)
        
    def test_user_cannot_create_rating_without_value(self):
        """Rating value is required while rating"""
        author_token = self.create_user()
        slug = self.create_article(author_token)
        url = self.article_rating_url(slug)

        rater = copy.deepcopy(self.user)
        rater['user'].update({
            'email': 'john@doe.com',
            'username': 'johnDoe'
        })

        rater_token = self.create_user(rater)
        del self.rating['rating']
        resp = self.client.post(url, self.rating, 'json', HTTP_AUTHORIZATION=rater_token)

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(b'The rating is required', resp.content)
        
    def test_user_cannot_create_rating_with_invalid_value(self):
        """Rating must be within a specified range"""
        author_token = self.create_user()
        slug = self.create_article(author_token)
        url = self.article_rating_url(slug)

        rater = copy.deepcopy(self.user)
        rater['user'].update({
            'email': 'john@doe.com',
            'username': 'johnDoe'
        })

        rater_token = self.create_user(rater)
        self.rating['rating'].update({'rating': settings.RATING_MIN - 1})
        resp = self.client.post(url, self.rating, 'json', HTTP_AUTHORIZATION=rater_token)

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(b'Rating cannot be less than', resp.content)

        self.rating['rating'].update({'rating': settings.RATING_MAX + 1})
        resp = self.client.post(url, self.rating, 'json', HTTP_AUTHORIZATION=rater_token)

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(b'Rating cannot be more than', resp.content)
        
    def test_user_can_update_their_rating(self):
        """User can update their rating on an article"""
        author_token = self.create_user()
        slug = self.create_article(author_token)
        url = self.article_rating_url(slug)

        rater = copy.deepcopy(self.user)
        rater['user'].update({
            'email': 'john@doe.com',
            'username': 'johnDoe'
        })

        rater_token = self.create_user(rater)
        resp = self.client.post(url, self.rating, 'json', HTTP_AUTHORIZATION=rater_token)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertIn(b'rating', resp.content)
        self.assertIn(b'4', resp.content)

        self.rating['rating'].update({'rating': 5})
        resp = self.client.put(url, self.rating, 'json', HTTP_AUTHORIZATION=rater_token)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn(b'rating', resp.content)
        self.assertIn(b'5', resp.content)
        
    def test_user_cannot_update_nonexistant_rating(self):
        """Ensure a rating exists for it to be updated"""
        author_token = self.create_user()
        slug = self.create_article(author_token)
        url = self.article_rating_url(slug)

        rater = copy.deepcopy(self.user)
        rater['user'].update({
            'email': 'john@doe.com',
            'username': 'johnDoe'
        })

        rater_token = self.create_user(rater)
        self.rating['rating'].update({'rating': 5})
        resp = self.client.put(url, self.rating, 'json', HTTP_AUTHORIZATION=rater_token)
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn(b'rating', resp.content)
        self.assertIn(b'Rating not found', resp.content)

    def test_user_cannot_update_rating_with_invalid_values(self):
        """An update on a rating must be within specified range"""
        author_token = self.create_user()
        slug = self.create_article(author_token)
        url = self.article_rating_url(slug)

        rater = copy.deepcopy(self.user)
        rater['user'].update({
            'email': 'john@doe.com',
            'username': 'johnDoe'
        })

        rater_token = self.create_user(rater)
        resp = self.client.post(url, self.rating, 'json', HTTP_AUTHORIZATION=rater_token)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertIn(b'rating', resp.content)
        self.assertIn(b'4', resp.content)

        self.rating['rating'].update({'rating': settings.RATING_MAX + 1})
        resp = self.client.put(url, self.rating, 'json', HTTP_AUTHORIZATION=rater_token)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(b'Rating cannot be more than', resp.content)

        self.rating['rating'].update({'rating': settings.RATING_MIN - 1})
        resp = self.client.put(url, self.rating, 'json', HTTP_AUTHORIZATION=rater_token)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(b'Rating cannot be less than', resp.content)

    def test_posting_to_existing_rating_updates_it(self):
        """Attempt to create an existing rating updates it instead"""
        author_token = self.create_user()
        slug = self.create_article(author_token)
        url = self.article_rating_url(slug)

        rater = copy.deepcopy(self.user)
        rater['user'].update({
            'email': 'john@doe.com',
            'username': 'johnDoe'
        })

        rater_token = self.create_user(rater)
        resp = self.client.post(url, self.rating, 'json', HTTP_AUTHORIZATION=rater_token)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertIn(b'rating', resp.content)
        self.assertIn(b'4', resp.content)

        self.rating['rating'].update({'rating': 5})
        resp = self.client.post(url, self.rating, 'json', HTTP_AUTHORIZATION=rater_token)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertIn(b'rating', resp.content)
        self.assertIn(b'5', resp.content)
        
