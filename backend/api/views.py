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
    - GET /api/products/{id}/ - Retrieve specific product
    """
    serializer_class = ProductSerializer

    def get_queryset(self):
        """Filter products based on query parameters."""
        queryset = Product.objects.all()
        featured = self.request.query_params.get('featured')
        if featured and featured.lower() == 'true':
            queryset = queryset.filter(featured=True)
        return queryset

    def list(self, request, *args, **kwargs):
        """Override list to return data in expected format."""
        response = super().list(request, *args, **kwargs)
        return Response({'data': response.data})

    def retrieve(self, request, *args, **kwargs):
        """Override retrieve to return data in expected format."""
        response = super().retrieve(request, *args, **kwargs)
        return Response({'data': response.data})


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Category model.

    Endpoints:
    - GET /api/categories/ - List all categories
    - GET /api/categories/{id}/ - Retrieve specific category
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

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
