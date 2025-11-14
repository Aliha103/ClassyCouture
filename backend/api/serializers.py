"""
Serializers for ClassyCouture API.
"""
from rest_framework import serializers
from .models import Product, Category, Review, Newsletter


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model with hierarchical support."""
    subcategories = serializers.SerializerMethodField()
    parent_name = serializers.CharField(source='parent.name', read_only=True, allow_null=True)
    product_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            'id', 'name', 'slug', 'description', 'image_url',
            'parent', 'parent_name', 'is_collection', 'display_order',
            'subcategories', 'product_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['slug', 'created_at', 'updated_at']
        extra_kwargs = {
            'parent': {'required': False, 'allow_null': True}
        }

    def get_subcategories(self, obj):
        """Get subcategories if any."""
        if obj.subcategories.exists():
            return CategorySerializer(obj.subcategories.all(), many=True, context=self.context).data
        return []

    def get_product_count(self, obj):
        """Get total product count including subcategories."""
        return obj.product_count


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
    discounted_price = serializers.SerializerMethodField()
    is_in_stock = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'price', 'discounted_price',
            'image_url', 'rating', 'review_count', 'featured', 'new_arrival',
            'inventory', 'sku', 'on_sale', 'discount_percent',
            'is_in_stock', 'category_name', 'created_at', 'updated_at'
        ]

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

    def get_discounted_price(self, obj):
        """Return discounted price."""
        return float(obj.discounted_price)

    def get_is_in_stock(self, obj):
        """Return stock status."""
        return obj.is_in_stock

    def get_category_name(self, obj):
        """Return category name."""
        return obj.category.name if obj.category else None


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
