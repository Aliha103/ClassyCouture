"""
Tests for ClassyCouture API.
"""
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from .models import Category, Product, Review, Newsletter
from datetime import datetime


class ProductAPITestCase(TestCase):
    """Test Product API endpoints."""

    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.category = Category.objects.create(
            name='Test Category',
            image_url='https://example.com/image.jpg'
        )
        self.product = Product.objects.create(
            name='Test Product',
            price=99.99,
            image_url='https://example.com/product.jpg',
            category=self.category,
            featured=True
        )
        self.review = Review.objects.create(
            product=self.product,
            customer_name='Test Customer',
            review_text='Great product!',
            rating=5
        )

    def test_list_products(self):
        """Test listing all products."""
        response = self.client.get('/api/products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('data', response.json())
        self.assertEqual(len(response.json()['data']), 1)

    def test_list_featured_products(self):
        """Test listing featured products."""
        response = self.client.get('/api/products/?featured=true')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()['data']
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['name'], 'Test Product')

    def test_product_response_format(self):
        """Test product response has correct fields."""
        response = self.client.get('/api/products/')
        data = response.json()['data'][0]
        self.assertIn('id', data)
        self.assertIn('name', data)
        self.assertIn('price', data)
        self.assertIn('image_url', data)
        self.assertIn('rating', data)
        self.assertIn('review_count', data)

    def test_retrieve_product(self):
        """Test retrieving a specific product."""
        response = self.client.get(f'/api/products/{self.product.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()['data']
        self.assertEqual(data['name'], 'Test Product')
        self.assertEqual(data['review_count'], 1)


class CategoryAPITestCase(TestCase):
    """Test Category API endpoints."""

    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.category = Category.objects.create(
            name='Test Category',
            image_url='https://example.com/image.jpg'
        )

    def test_list_categories(self):
        """Test listing all categories."""
        response = self.client.get('/api/categories/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('data', response.json())
        self.assertEqual(len(response.json()['data']), 1)

    def test_category_response_format(self):
        """Test category response has correct fields."""
        response = self.client.get('/api/categories/')
        data = response.json()['data'][0]
        self.assertIn('id', data)
        self.assertIn('name', data)
        self.assertIn('image_url', data)


class ReviewAPITestCase(TestCase):
    """Test Review API endpoints."""

    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.category = Category.objects.create(
            name='Test Category',
            image_url='https://example.com/image.jpg'
        )
        self.product = Product.objects.create(
            name='Test Product',
            price=99.99,
            image_url='https://example.com/product.jpg',
            category=self.category
        )
        self.review = Review.objects.create(
            product=self.product,
            customer_name='Test Customer',
            review_text='Great product!',
            rating=5
        )

    def test_list_reviews(self):
        """Test listing all reviews."""
        response = self.client.get('/api/reviews/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('data', response.json())
        self.assertEqual(len(response.json()['data']), 1)

    def test_reviews_with_limit(self):
        """Test listing reviews with limit parameter."""
        # Create additional reviews
        for i in range(5):
            Review.objects.create(
                product=self.product,
                customer_name=f'Customer {i}',
                review_text='Good product',
                rating=4
            )

        response = self.client.get('/api/reviews/?limit=3')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()['data']
        self.assertEqual(len(data), 3)

    def test_review_response_format(self):
        """Test review response has correct fields."""
        response = self.client.get('/api/reviews/')
        data = response.json()['data'][0]
        self.assertIn('id', data)
        self.assertIn('customer_name', data)
        self.assertIn('review_text', data)
        self.assertIn('rating', data)
        self.assertIn('date', data)


class NewsletterAPITestCase(TestCase):
    """Test Newsletter API endpoints."""

    def setUp(self):
        """Set up test client."""
        self.client = Client()

    def test_subscribe_newsletter(self):
        """Test newsletter subscription."""
        response = self.client.post(
            '/api/newsletter/subscribe/',
            {'email': 'test@example.com'},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertEqual(data['email'], 'test@example.com')

    def test_duplicate_subscription(self):
        """Test duplicate subscription fails."""
        Newsletter.objects.create(email='test@example.com')
        response = self.client.post(
            '/api/newsletter/subscribe/',
            {'email': 'test@example.com'},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = response.json()
        self.assertFalse(data['success'])

    def test_invalid_email(self):
        """Test invalid email format."""
        response = self.client.post(
            '/api/newsletter/subscribe/',
            {'email': 'invalid-email'},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
