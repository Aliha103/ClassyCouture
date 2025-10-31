"""
Serializers for ClassyCouture API.
"""
from rest_framework import serializers
from .models import Product, Category, Review, Newsletter


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model."""

    class Meta:
        model = Category
        fields = ['id', 'name', 'image_url']


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for Review model."""
    date = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ['id', 'customer_name', 'review_text', 'rating', 'date']

    def get_date(self, obj):
        """Return ISO format date."""
        return obj.created_at.isoformat()


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for Product model."""
    rating = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'image_url', 'rating', 'review_count']

    def get_rating(self, obj):
        """Calculate and return average rating."""
        reviews = obj.reviews.all()
        if not reviews.exists():
            return 0
        total_rating = sum(review.rating for review in reviews)
        return round(total_rating / reviews.count(), 1)

    def get_review_count(self, obj):
        """Return count of reviews."""
        return obj.reviews.count()


class NewsletterSerializer(serializers.ModelSerializer):
    """Serializer for Newsletter subscription."""

    class Meta:
        model = Newsletter
        fields = ['email']

    def validate_email(self, value):
        """Check if email already exists."""
        if Newsletter.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already subscribed.")
        return value

    def create(self, validated_data):
        """Create newsletter subscription."""
        newsletter, created = Newsletter.objects.get_or_create(
            email=validated_data['email'],
            defaults={'is_active': True}
        )
        if not created and not newsletter.is_active:
            newsletter.is_active = True
            newsletter.save()
        return newsletter
