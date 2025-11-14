"""
AI-Powered Recommendation Engine for ClassyCouture
Provides personalized product recommendations based on user behavior and purchase patterns.
"""

from django.db.models import Count, Q, F, Avg
from django.utils import timezone
from datetime import timedelta
from .models import Product, Order, OrderItem, Review
from typing import List


class RecommendationEngine:
    """AI-powered product recommendation system."""

    @staticmethod
    def get_similar_products(product_id: int, limit: int = 6) -> List[Product]:
        """
        Get products similar to the given product.
        Based on: category, price range, and rating.

        Args:
            product_id: ID of the product to find similar items for
            limit: Maximum number of recommendations to return

        Returns:
            List of similar Product objects
        """
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return []

        # Calculate price range (±30%)
        price_min = float(product.price) * 0.7
        price_max = float(product.price) * 1.3

        # Find similar products
        similar = Product.objects.filter(
            category=product.category,
            price__gte=price_min,
            price__lte=price_max,
            inventory__gt=0
        ).exclude(
            id=product_id
        ).order_by(
            '-featured',
            '-rating',
            '-created_at'
        )[:limit]

        return list(similar)

    @staticmethod
    def get_frequently_bought_together(product_id: int, limit: int = 4) -> List[Product]:
        """
        Get products frequently bought with this product.
        Analyzes order history to find co-purchase patterns.

        Args:
            product_id: ID of the product to find companions for
            limit: Maximum number of recommendations to return

        Returns:
            List of frequently co-purchased Product objects
        """
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return []

        # Find all orders containing this product
        orders_with_product = OrderItem.objects.filter(
            product_id=product_id
        ).values_list('order_id', flat=True)

        if not orders_with_product:
            # Fallback to similar products
            return RecommendationEngine.get_similar_products(product_id, limit)

        # Find products that appear in the same orders
        co_purchased = OrderItem.objects.filter(
            order_id__in=orders_with_product
        ).exclude(
            product_id=product_id
        ).values('product_id').annotate(
            frequency=Count('product_id')
        ).order_by('-frequency')[:limit]

        # Get the actual product objects
        product_ids = [item['product_id'] for item in co_purchased]
        products = Product.objects.filter(
            id__in=product_ids,
            inventory__gt=0
        )

        # Sort by frequency
        product_dict = {p.id: p for p in products}
        sorted_products = [
            product_dict[item['product_id']]
            for item in co_purchased
            if item['product_id'] in product_dict
        ]

        return sorted_products

    @staticmethod
    def get_personalized_recommendations(user_id: int, limit: int = 8) -> List[Product]:
        """
        Get personalized recommendations based on user's purchase history and browsing.
        Uses collaborative filtering approach.

        Args:
            user_id: ID of the user to generate recommendations for
            limit: Maximum number of recommendations to return

        Returns:
            List of recommended Product objects
        """
        from django.contrib.auth.models import User

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return RecommendationEngine.get_trending_products(limit)

        # Get user's order history
        user_orders = Order.objects.filter(user=user)
        purchased_product_ids = OrderItem.objects.filter(
            order__in=user_orders
        ).values_list('product_id', flat=True)

        if not purchased_product_ids:
            # New user - show trending products
            return RecommendationEngine.get_trending_products(limit)

        # Find categories user has purchased from
        purchased_products = Product.objects.filter(id__in=purchased_product_ids)
        favorite_categories = purchased_products.values('category').annotate(
            count=Count('category')
        ).order_by('-count')[:3]

        favorite_category_ids = [cat['category'] for cat in favorite_categories]

        # Recommend products from favorite categories that user hasn't purchased
        recommendations = Product.objects.filter(
            category_id__in=favorite_category_ids,
            inventory__gt=0
        ).exclude(
            id__in=purchased_product_ids
        ).order_by(
            '-featured',
            '-rating',
            '-created_at'
        )[:limit]

        recommendations_list = list(recommendations)

        # If we don't have enough recommendations, add trending products
        if len(recommendations_list) < limit:
            trending = RecommendationEngine.get_trending_products(
                limit - len(recommendations_list)
            )
            recommendations_list.extend([
                p for p in trending
                if p.id not in purchased_product_ids and p not in recommendations_list
            ])

        return recommendations_list

    @staticmethod
    def get_trending_products(limit: int = 8) -> List[Product]:
        """
        Get trending products based on recent sales and popularity.

        Args:
            limit: Maximum number of trending products to return

        Returns:
            List of trending Product objects
        """
        # Get orders from last 30 days
        thirty_days_ago = timezone.now() - timedelta(days=30)

        # Find products with most sales in last 30 days
        trending_ids = OrderItem.objects.filter(
            order__order_date__gte=thirty_days_ago,
            order__status__in=['processing', 'shipped', 'delivered']
        ).values('product_id').annotate(
            sales_count=Count('product_id')
        ).order_by('-sales_count')[:limit]

        product_ids = [item['product_id'] for item in trending_ids]

        # Get the actual products
        trending_products = Product.objects.filter(
            id__in=product_ids,
            inventory__gt=0
        )

        # Sort by the sales count
        product_dict = {p.id: p for p in trending_products}
        sorted_trending = [
            product_dict[item['product_id']]
            for item in trending_ids
            if item['product_id'] in product_dict
        ]

        # If we don't have enough, add featured products
        if len(sorted_trending) < limit:
            featured = list(Product.objects.filter(
                featured=True,
                inventory__gt=0
            ).exclude(
                id__in=product_ids
            ).order_by('-rating', '-created_at')[:limit - len(sorted_trending)])
            sorted_trending.extend(featured)

        return sorted_trending

    @staticmethod
    def get_you_may_also_like(user_id: int, current_product_id: int, limit: int = 6) -> List[Product]:
        """
        Hybrid recommendations combining similar products and personalized suggestions.

        Args:
            user_id: ID of the user
            current_product_id: ID of the product user is viewing
            limit: Maximum number of recommendations to return

        Returns:
            List of recommended Product objects
        """
        # Get half from similar products
        similar = RecommendationEngine.get_similar_products(
            current_product_id,
            limit=limit // 2
        )

        # Get half from personalized recommendations
        personalized = RecommendationEngine.get_personalized_recommendations(
            user_id,
            limit=limit // 2
        )

        # Combine and deduplicate
        recommendations = []
        seen_ids = set()

        # Alternate between similar and personalized
        for i in range(max(len(similar), len(personalized))):
            if i < len(similar) and similar[i].id not in seen_ids:
                recommendations.append(similar[i])
                seen_ids.add(similar[i].id)

            if i < len(personalized) and personalized[i].id not in seen_ids:
                recommendations.append(personalized[i])
                seen_ids.add(personalized[i].id)

            if len(recommendations) >= limit:
                break

        return recommendations[:limit]

    @staticmethod
    def get_bundle_discount_suggestions(product_id: int, limit: int = 3) -> List[dict]:
        """
        Suggest product bundles with potential discounts.

        Args:
            product_id: ID of the product to create bundles for
            limit: Maximum number of bundle suggestions

        Returns:
            List of bundle dictionaries with products and suggested discount
        """
        frequently_bought = RecommendationEngine.get_frequently_bought_together(
            product_id,
            limit=limit
        )

        try:
            main_product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return []

        bundles = []
        for companion in frequently_bought:
            bundle_price = float(main_product.price) + float(companion.price)
            discount_percent = 10  # 10% bundle discount
            discounted_price = bundle_price * (1 - discount_percent / 100)
            savings = bundle_price - discounted_price

            bundles.append({
                'main_product': {
                    'id': main_product.id,
                    'name': main_product.name,
                    'price': float(main_product.price),
                    'image': main_product.image_url
                },
                'companion_product': {
                    'id': companion.id,
                    'name': companion.name,
                    'price': float(companion.price),
                    'image': companion.image_url
                },
                'bundle_price': bundle_price,
                'discounted_price': round(discounted_price, 2),
                'savings': round(savings, 2),
                'discount_percent': discount_percent
            })

        return bundles

    @staticmethod
    def get_new_arrivals(limit: int = 8) -> List[Product]:
        """
        Get newest products added to the store.

        Args:
            limit: Maximum number of products to return

        Returns:
            List of newest Product objects
        """
        return list(Product.objects.filter(
            inventory__gt=0
        ).order_by('-created_at')[:limit])

    @staticmethod
    def get_best_sellers(limit: int = 8) -> List[Product]:
        """
        Get best-selling products of all time.

        Args:
            limit: Maximum number of products to return

        Returns:
            List of best-selling Product objects
        """
        best_sellers_ids = OrderItem.objects.filter(
            order__status__in=['processing', 'shipped', 'delivered']
        ).values('product_id').annotate(
            total_sales=Count('product_id')
        ).order_by('-total_sales')[:limit]

        product_ids = [item['product_id'] for item in best_sellers_ids]

        best_sellers = Product.objects.filter(
            id__in=product_ids,
            inventory__gt=0
        )

        # Sort by sales count
        product_dict = {p.id: p for p in best_sellers}
        sorted_best_sellers = [
            product_dict[item['product_id']]
            for item in best_sellers_ids
            if item['product_id'] in product_dict
        ]

        return sorted_best_sellers
