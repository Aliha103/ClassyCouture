"""
URL configuration for API endpoints.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, CategoryViewSet, ReviewViewSet, NewsletterViewSet
from .views_extended import (
    AuthViewSet, BannerViewSet, VoucherViewSet, SalesAnalyticsViewSet,
    OrderViewSet, RefundViewSet, UserProfileViewSet, WatchlistViewSet,
    ProductReviewViewSet, ComplaintViewSet, ReferralViewSet
)

# Create router for viewsets
router = DefaultRouter()

# Original endpoints
router.register(r'products', ProductViewSet, basename='product')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'reviews', ReviewViewSet, basename='review')
router.register(r'newsletter', NewsletterViewSet, basename='newsletter')

# Authentication
router.register(r'auth', AuthViewSet, basename='auth')

# Admin features
router.register(r'banners', BannerViewSet, basename='banner')
router.register(r'vouchers', VoucherViewSet, basename='voucher')
router.register(r'analytics', SalesAnalyticsViewSet, basename='analytics')

# Orders & Refunds
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'refunds', RefundViewSet, basename='refund')

# User features
router.register(r'profile', UserProfileViewSet, basename='profile')
router.register(r'watchlist', WatchlistViewSet, basename='watchlist')
router.register(r'product-reviews', ProductReviewViewSet, basename='product-review')
router.register(r'complaints', ComplaintViewSet, basename='complaint')
router.register(r'referrals', ReferralViewSet, basename='referral')

# URL patterns
urlpatterns = [
    path('', include(router.urls)),
]
