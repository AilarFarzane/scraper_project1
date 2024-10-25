from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Article
from django.contrib.auth.models import User

class ArticleAPITests(APITestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='user', password='ailar1234')
        self.client.login(username='user', password='ailar1234')  # Log in the user

        # Create an article instance for testing
        self.article = Article.objects.create(
            title='Test Article',
            date_published='2024-10-25',
            content='This is a test article content.'
        )
        self.article_list_url = reverse('ArticleList')
        self.article_detail_url = reverse('ArticleDetail', args=[self.article.id])

    def test_article_list_get(self):
        response = self.client.get(self.article_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Check if the list contains 1 article

    def test_article_list_post(self):
        new_article_data = {
            'title': 'New Test Article',
            'date_published': '2024-10-26',
            'content': 'This is another test article content.'
        }
        response = self.client.post(self.article_list_url, new_article_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Article.objects.count(), 2)  # Check if the article count has increased

    def test_article_detail_get(self):
        response = self.client.get(self.article_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.article.title)

    def test_article_detail_patch(self):
        updated_data = {
            'title': 'Updated Test Article'
        }
        response = self.client.patch(self.article_detail_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.article.refresh_from_db()  # Refresh the instance from the database
        self.assertEqual(self.article.title, 'Updated Test Article')

    def test_article_detail_delete(self):
        response = self.client.delete(self.article_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Article.objects.filter(id=self.article.id).exists())  # Check if the article was deleted

    def test_article_list_filter_by_date(self):
        response = self.client.get(self.article_list_url, {'date_published': '2024-10-25'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Only the original article should be returned
