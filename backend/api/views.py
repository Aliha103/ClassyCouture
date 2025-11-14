"""
API Views for ClassyCouture.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import Product, Category, Review, Newsletter
from .serializers import (
    ProductSerializer,
    CategorySerializer,
    ReviewSerializer,
    NewsletterSerializer
)


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Product model.

    Endpoints:
    - GET /api/products/ - List all products
    - GET /api/products/?featured=true - List featured products
    - GET /api/products/?new_arrivals=true - List new arrival products
    - GET /api/products/?limit=8 - Limit number of products returned
    - GET /api/products/{id}/ - Retrieve specific product
    """
    serializer_class = ProductSerializer

    def get_queryset(self):
        """Filter products based on query parameters."""
        queryset = Product.objects.select_related('category').prefetch_related('reviews')

        # Filter by featured
        featured = self.request.query_params.get('featured')
        if featured and featured.lower() == 'true':
            queryset = queryset.filter(featured=True)

        # Filter by new arrivals
        new_arrivals = self.request.query_params.get('new_arrivals')
        if new_arrivals and new_arrivals.lower() == 'true':
            queryset = queryset.filter(new_arrival=True)

        # Limit results
        limit = self.request.query_params.get('limit')
        if limit:
            try:
                limit = int(limit)
                queryset = queryset[:limit]
            except ValueError:
                pass

        return queryset

    def list(self, request, *args, **kwargs):
        """Override list to return data in expected format."""
        response = super().list(request, *args, **kwargs)
        return Response({'data': response.data})

    def retrieve(self, request, *args, **kwargs):
        """Override retrieve to return data in expected format."""
        response = super().retrieve(request, *args, **kwargs)
        return Response({'data': response.data})


class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Category model with collection support.

    Endpoints:
    - GET /api/categories/ - List all categories
    - GET /api/categories/?collections_only=true - List top-level collections only
    - GET /api/categories/?parent=<id> - List subcategories of parent
    - GET /api/categories/{id}/ - Retrieve specific category
    - POST /api/categories/ - Create new category/collection
    - PUT/PATCH /api/categories/{id}/ - Update category/collection
    - DELETE /api/categories/{id}/ - Delete category/collection
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_queryset(self):
        """Filter categories based on query parameters."""
        queryset = Category.objects.all().prefetch_related('subcategories', 'products')

        # Filter for collections only (top-level)
        collections_only = self.request.query_params.get('collections_only')
        if collections_only and collections_only.lower() == 'true':
            queryset = queryset.filter(parent__isnull=True, is_collection=True)

        # Filter for sub-collections of a specific parent
        parent_id = self.request.query_params.get('parent')
        if parent_id:
            queryset = queryset.filter(parent_id=parent_id)

        # Filter for top-level categories/collections only
        top_level = self.request.query_params.get('top_level')
        if top_level and top_level.lower() == 'true':
            queryset = queryset.filter(parent__isnull=True)

        return queryset

    def list(self, request, *args, **kwargs):
        """Override list to return data in expected format."""
        response = super().list(request, *args, **kwargs)
        return Response({'data': response.data})

    def retrieve(self, request, *args, **kwargs):
        """Override retrieve to return data in expected format."""
        response = super().retrieve(request, *args, **kwargs)
        return Response({'data': response.data})


class ReviewViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Review model.

    Endpoints:
    - GET /api/reviews/ - List all reviews
    - GET /api/reviews/?limit=6 - List recent reviews with limit
    """
    serializer_class = ReviewSerializer

    def get_queryset(self):
        """Get reviews ordered by recency."""
        return Review.objects.all().order_by('-created_at')

    def list(self, request, *args, **kwargs):
        """Override list with limit parameter support."""
        limit = request.query_params.get('limit')
        queryset = self.get_queryset()

        if limit:
            try:
                limit = int(limit)
                queryset = queryset[:limit]
            except ValueError:
                pass

        serializer = self.get_serializer(queryset, many=True)
        return Response({'data': serializer.data})

    def retrieve(self, request, *args, **kwargs):
        """Override retrieve to return data in expected format."""
        response = super().retrieve(request, *args, **kwargs)
        return Response({'data': response.data})


class NewsletterViewSet(viewsets.ViewSet):
    """
    ViewSet for Newsletter subscription.

    Endpoints:
    - POST /api/newsletter/subscribe/ - Subscribe to newsletter
    """

    @action(detail=False, methods=['post'])
    def subscribe(self, request):
        """
        Subscribe email to newsletter.

        Expected POST data:
        {
            "email": "user@example.com"
        }
        """
        serializer = NewsletterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    'success': True,
                    'message': 'Successfully subscribed to newsletter',
                    'email': serializer.validated_data['email']
                },
                status=status.HTTP_201_CREATED
            )

        # Return validation errors
        errors = serializer.errors
        if 'email' in errors:
            error_message = errors['email'][0]
            if 'already subscribed' in str(error_message):
                return Response(
                    {
                        'success': False,
                        'error': 'Email already subscribed'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        return Response(
            {
                'success': False,
                'error': errors.get('email', ['Invalid email'])[0]
            },
            status=status.HTTP_400_BAD_REQUEST
        )


# ===========================
# Recommendation API Views
# ===========================

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from .recommendation_engine import RecommendationEngine


@api_view(['GET'])
@permission_classes([AllowAny])
def similar_products(request, product_id):
    """
    Get products similar to the specified product.

    GET /api/recommendations/similar/<product_id>/
    Query params:
    - limit: Number of products to return (default: 6)
    """
    limit = int(request.query_params.get('limit', 6))
    products = RecommendationEngine.get_similar_products(product_id, limit)
    serializer = ProductSerializer(products, many=True)
    return Response({'data': serializer.data})


@api_view(['GET'])
@permission_classes([AllowAny])
def frequently_bought_together(request, product_id):
    """
    Get products frequently bought with the specified product.

    GET /api/recommendations/frequently-bought/<product_id>/
    Query params:
    - limit: Number of products to return (default: 4)
    """
    limit = int(request.query_params.get('limit', 4))
    products = RecommendationEngine.get_frequently_bought_together(product_id, limit)
    serializer = ProductSerializer(products, many=True)
    return Response({'data': serializer.data})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def personalized_recommendations(request):
    """
    Get personalized product recommendations for the authenticated user.

    GET /api/recommendations/personalized/
    Query params:
    - limit: Number of products to return (default: 8)
    """
    limit = int(request.query_params.get('limit', 8))
    products = RecommendationEngine.get_personalized_recommendations(request.user.id, limit)
    serializer = ProductSerializer(products, many=True)
    return Response({'data': serializer.data})


@api_view(['GET'])
@permission_classes([AllowAny])
def trending_products(request):
    """
    Get trending products based on recent sales.

    GET /api/recommendations/trending/
    Query params:
    - limit: Number of products to return (default: 8)
    """
    limit = int(request.query_params.get('limit', 8))
    products = RecommendationEngine.get_trending_products(limit)
    serializer = ProductSerializer(products, many=True)
    return Response({'data': serializer.data})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def you_may_also_like(request, product_id):
    """
    Get hybrid recommendations combining similar products and personalized suggestions.

    GET /api/recommendations/you-may-also-like/<product_id>/
    Query params:
    - limit: Number of products to return (default: 6)
    """
    limit = int(request.query_params.get('limit', 6))
    products = RecommendationEngine.get_you_may_also_like(request.user.id, product_id, limit)
    serializer = ProductSerializer(products, many=True)
    return Response({'data': serializer.data})


@api_view(['GET'])
@permission_classes([AllowAny])
def bundle_suggestions(request, product_id):
    """
    Get bundle discount suggestions for the specified product.

    GET /api/recommendations/bundles/<product_id>/
    Query params:
    - limit: Number of bundle suggestions (default: 3)
    """
    limit = int(request.query_params.get('limit', 3))
    bundles = RecommendationEngine.get_bundle_discount_suggestions(product_id, limit)
    return Response({'data': bundles})


@api_view(['GET'])
@permission_classes([AllowAny])
def new_arrivals(request):
    """
    Get newest products added to the store.

    GET /api/recommendations/new-arrivals/
    Query params:
    - limit: Number of products to return (default: 8)
    """
    limit = int(request.query_params.get('limit', 8))
    products = RecommendationEngine.get_new_arrivals(limit)
    serializer = ProductSerializer(products, many=True)
    return Response({'data': serializer.data})


@api_view(['GET'])
@permission_classes([AllowAny])
def best_sellers(request):
    """
    Get best-selling products of all time.

    GET /api/recommendations/best-sellers/
    Query params:
    - limit: Number of products to return (default: 8)
    """
    limit = int(request.query_params.get('limit', 8))
    products = RecommendationEngine.get_best_sellers(limit)
    serializer = ProductSerializer(products, many=True)
    return Response({'data': serializer.data})
