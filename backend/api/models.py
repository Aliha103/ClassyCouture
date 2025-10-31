"""
Models for ClassyCouture API.
"""
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
import uuid


class Category(models.Model):
    """Product category model."""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    image_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "categories"
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    """Product model."""
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    image_url = models.URLField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    featured = models.BooleanField(default=False, db_index=True)
    inventory = models.IntegerField(default=0, validators=[MinValueValidator(0)])  # Stock quantity
    sku = models.CharField(max_length=50, unique=True, null=True, blank=True)  # Stock Keeping Unit
    on_sale = models.BooleanField(default=False)
    discount_percent = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['featured', '-created_at']),
        ]

    def __str__(self):
        return self.name

    @property
    def rating(self):
        """Calculate average rating from reviews."""
        reviews = self.reviews.all()
        if not reviews.exists():
            return 0
        return round(sum([r.rating for r in reviews]) / reviews.count(), 1)

    @property
    def review_count(self):
        """Get count of reviews."""
        return self.reviews.count()

    @property
    def discounted_price(self):
        """Calculate discounted price."""
        if self.on_sale and self.discount_percent > 0:
            discount_amount = self.price * (self.discount_percent / 100)
            return round(self.price - discount_amount, 2)
        return self.price

    @property
    def is_in_stock(self):
        """Check if product is in stock."""
        return self.inventory > 0


class Review(models.Model):
    """Customer review model."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    customer_name = models.CharField(max_length=100)
    review_text = models.TextField()
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    email = models.EmailField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return f"{self.customer_name} - {self.product.name}"


class Newsletter(models.Model):
    """Newsletter subscription model."""
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-subscribed_at']

    def __str__(self):
        return self.email
