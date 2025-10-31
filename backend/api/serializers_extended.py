"""
Extended serializers for ClassyCouture API - Admin, Auth, Orders, User Features.
"""
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    UserProfile, Banner, Voucher, SalesAnalytics,
    Order, OrderItem, OrderTracking, Refund,
    Watchlist, ProductReview, Complaint, Referral, Product
)


# ============================================================================
# USER & AUTH SERIALIZERS
# ============================================================================

class UserSerializer(serializers.ModelSerializer):
    """Basic user serializer."""

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class UserProfileSerializer(serializers.ModelSerializer):
    """User profile serializer."""
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = [
            'id', 'user', 'phone', 'address', 'city', 'country', 'postal_code',
            'referral_code', 'referral_points', 'total_referrals', 'is_admin'
        ]


class UserRegistrationSerializer(serializers.ModelSerializer):
    """User registration serializer."""
    password = serializers.CharField(write_only=True, min_length=6)
    password_confirm = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 'first_name', 'last_name']

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        # Create user profile
        UserProfile.objects.create(
            user=user,
            referral_code=f"REF{user.id}{user.username[:3].upper()}"
        )
        return user


class UserLoginSerializer(serializers.Serializer):
    """User login serializer."""
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


# ============================================================================
# ADMIN SERIALIZERS
# ============================================================================

class BannerSerializer(serializers.ModelSerializer):
    """Banner serializer."""

    class Meta:
        model = Banner
        fields = ['id', 'title', 'description', 'image_url', 'cta_text', 'cta_link', 'is_active', 'order']


class VoucherSerializer(serializers.ModelSerializer):
    """Voucher serializer."""
    can_use = serializers.SerializerMethodField()
    is_expired = serializers.SerializerMethodField()

    class Meta:
        model = Voucher
        fields = [
            'id', 'code', 'description', 'discount_type', 'discount_value',
            'min_purchase', 'max_uses', 'current_uses', 'is_active',
            'start_date', 'end_date', 'can_use', 'is_expired'
        ]

    def get_can_use(self, obj):
        return obj.can_use

    def get_is_expired(self, obj):
        return obj.is_expired


class SalesAnalyticsSerializer(serializers.ModelSerializer):
    """Sales analytics serializer."""

    class Meta:
        model = SalesAnalytics
        fields = [
            'id', 'date', 'total_orders', 'total_revenue', 'total_items_sold',
            'avg_order_value', 'total_profit', 'unique_customers'
        ]


# ============================================================================
# ORDER SERIALIZERS
# ============================================================================

class OrderItemSerializer(serializers.ModelSerializer):
    """Order item serializer."""
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_image = serializers.CharField(source='product.image_url', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'product_image', 'quantity', 'price_at_purchase', 'total']


class OrderTrackingSerializer(serializers.ModelSerializer):
    """Order tracking serializer."""

    class Meta:
        model = OrderTracking
        fields = ['id', 'current_location', 'estimated_delivery', 'carrier', 'tracking_number', 'last_updated']


class RefundSerializer(serializers.ModelSerializer):
    """Refund serializer."""
    processed_by_username = serializers.CharField(source='processed_by.username', read_only=True)

    class Meta:
        model = Refund
        fields = [
            'id', 'order', 'reason', 'requested_at', 'amount', 'status',
            'admin_notes', 'processed_at', 'processed_by', 'processed_by_username'
        ]


class OrderSerializer(serializers.ModelSerializer):
    """Order serializer."""
    items = OrderItemSerializer(many=True, read_only=True)
    tracking = OrderTrackingSerializer(read_only=True)
    refund = RefundSerializer(read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'order_id', 'user', 'username', 'total_price', 'discount_amount',
            'final_price', 'voucher_code', 'status', 'shipping_address', 'phone',
            'payment_method', 'payment_status', 'notes', 'items', 'tracking', 'refund',
            'created_at', 'updated_at'
        ]


class OrderCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating orders."""

    class Meta:
        model = Order
        fields = [
            'total_price', 'discount_amount', 'final_price', 'voucher_code',
            'shipping_address', 'phone', 'payment_method', 'notes'
        ]


# ============================================================================
# USER FEATURE SERIALIZERS
# ============================================================================

class WatchlistSerializer(serializers.ModelSerializer):
    """Watchlist serializer."""
    products = serializers.SerializerMethodField()

    class Meta:
        model = Watchlist
        fields = ['id', 'user', 'products', 'created_at', 'updated_at']

    def get_products(self, obj):
        from .serializers import ProductSerializer
        return ProductSerializer(obj.products.all(), many=True).data


class ProductReviewSerializer(serializers.ModelSerializer):
    """Product review serializer."""
    username = serializers.CharField(source='user.username', read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = ProductReview
        fields = [
            'id', 'product', 'product_name', 'user', 'username', 'rating', 'title',
            'review_text', 'is_verified_purchase', 'helpful_count', 'created_at', 'updated_at'
        ]


class ComplaintSerializer(serializers.ModelSerializer):
    """Complaint serializer."""
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Complaint
        fields = [
            'id', 'order_item', 'user', 'username', 'title', 'description',
            'status', 'resolution', 'created_at', 'updated_at', 'resolved_at'
        ]


class ReferralSerializer(serializers.ModelSerializer):
    """Referral serializer."""
    referrer_username = serializers.CharField(source='referrer.username', read_only=True)
    referred_username = serializers.CharField(source='referred_user.username', read_only=True)

    class Meta:
        model = Referral
        fields = [
            'id', 'referrer', 'referrer_username', 'referred_user', 'referred_username',
            'referral_code', 'is_active', 'points_earned', 'created_at'
        ]
