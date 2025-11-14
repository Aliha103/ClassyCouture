"""
URL configuration for API endpoints.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProductViewSet, CategoryViewSet, ReviewViewSet, NewsletterViewSet,
    similar_products, frequently_bought_together, personalized_recommendations,
    trending_products, you_may_also_like, bundle_suggestions,
    new_arrivals, best_sellers
)
from .views_extended import (
    AuthViewSet, BannerViewSet, VoucherViewSet, SalesAnalyticsViewSet,
    OrderViewSet, RefundViewSet, UserProfileViewSet, WatchlistViewSet,
    ComplaintViewSet, ReferralViewSet
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
router.register(r'complaints', ComplaintViewSet, basename='complaint')
router.register(r'referrals', ReferralViewSet, basename='referral')

# URL patterns
urlpatterns = [
    path('', include(router.urls)),

    # Recommendation endpoints
    path('recommendations/similar/<int:product_id>/', similar_products, name='similar-products'),
    path('recommendations/frequently-bought/<int:product_id>/', frequently_bought_together, name='frequently-bought'),
    path('recommendations/personalized/', personalized_recommendations, name='personalized-recommendations'),
    path('recommendations/trending/', trending_products, name='trending-products'),
    path('recommendations/you-may-also-like/<int:product_id>/', you_may_also_like, name='you-may-also-like'),
    path('recommendations/bundles/<int:product_id>/', bundle_suggestions, name='bundle-suggestions'),
    path('recommendations/new-arrivals/', new_arrivals, name='new-arrivals'),
    path('recommendations/best-sellers/', best_sellers, name='best-sellers'),
]
