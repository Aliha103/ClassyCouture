"""
Extended views for ClassyCouture API - Admin, Auth, Orders, User Features.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models import Sum
from .models import (
    UserProfile, Banner, Voucher, SalesAnalytics,
    Order, OrderItem, OrderTracking, Refund,
    Watchlist, ProductReview, Complaint, Referral, Product
)
from .serializers_extended import (
    UserSerializer, UserProfileSerializer, UserRegistrationSerializer, UserLoginSerializer,
    BannerSerializer, VoucherSerializer, SalesAnalyticsSerializer,
    OrderSerializer, OrderItemSerializer, OrderTrackingSerializer, RefundSerializer, OrderCreateSerializer,
    WatchlistSerializer, ProductReviewSerializer, ComplaintSerializer, ReferralSerializer
)


# ============================================================================
# AUTHENTICATION VIEWS
# ============================================================================

class AuthViewSet(viewsets.ViewSet):
    """Authentication endpoints."""
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'])
    def register(self, request):
        """Register new user."""
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    'success': True,
                    'message': 'User registered successfully',
                    'user': UserSerializer(user).data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(
            {
                'success': False,
                'errors': serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=False, methods=['post'])
    def login(self, request):
        """Login user."""
        serializer = UserLoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'success': False, 'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )

        if user is None:
            return Response(
                {'success': False, 'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        profile = user.profile
        return Response(
            {
                'success': True,
                'message': 'Login successful',
                'user': UserSerializer(user).data,
                'profile': UserProfileSerializer(profile).data
            },
            status=status.HTTP_200_OK
        )


# ============================================================================
# ADMIN VIEWS
# ============================================================================

class BannerViewSet(viewsets.ModelViewSet):
    """Banner management viewset."""
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUser()]

    def list(self, request, *args, **kwargs):
        """Get all active banners."""
        queryset = Banner.objects.filter(is_active=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response({'data': serializer.data})


class VoucherViewSet(viewsets.ModelViewSet):
    """Voucher management viewset."""
    queryset = Voucher.objects.all()
    serializer_class = VoucherSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action == 'retrieve':
            return [AllowAny()]
        return [IsAdminUser()]

    @action(detail=False, methods=['post'])
    def validate_code(self, request):
        """Validate voucher code."""
        code = request.data.get('code')
        if not code:
            return Response({'valid': False, 'error': 'Code required'})

        try:
            voucher = Voucher.objects.get(code=code)
            if voucher.can_use:
                return Response({
                    'valid': True,
                    'voucher': VoucherSerializer(voucher).data
                })
            return Response({'valid': False, 'error': 'Voucher expired or max uses reached'})
        except Voucher.DoesNotExist:
            return Response({'valid': False, 'error': 'Voucher not found'})


class SalesAnalyticsViewSet(viewsets.ReadOnlyModelViewSet):
    """Sales analytics viewset."""
    queryset = SalesAnalytics.objects.all()
    serializer_class = SalesAnalyticsSerializer
    permission_classes = [IsAdminUser]


# ============================================================================
# ORDER VIEWS
# ============================================================================

class OrderViewSet(viewsets.ModelViewSet):
    """Order management viewset."""
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Users see only their orders, admins see all."""
        if self.request.user.profile.is_admin:
            return Order.objects.all()
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Create order for current user."""
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['get'])
    def tracking(self, request, pk=None):
        """Get order tracking info."""
        order = self.get_object()
        try:
            tracking = order.tracking
            serializer = OrderTrackingSerializer(tracking)
            return Response({'data': serializer.data})
        except OrderTracking.DoesNotExist:
            return Response({'data': None, 'message': 'No tracking info yet'})

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel order if possible."""
        order = self.get_object()
        if order.status == 'pending':
            order.status = 'cancelled'
            order.save()
            return Response({'success': True, 'message': 'Order cancelled'})
        return Response({'success': False, 'error': 'Order cannot be cancelled'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def my_orders(self, request):
        """Get current user's orders."""
        orders = self.get_queryset()
        serializer = self.get_serializer(orders, many=True)
        return Response({'data': serializer.data})


class RefundViewSet(viewsets.ModelViewSet):
    """Refund management viewset."""
    serializer_class = RefundSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Users see only their refunds, admins see all."""
        if self.request.user.profile.is_admin:
            return Refund.objects.all()
        return Refund.objects.filter(order__user=self.request.user)

    @action(detail=False, methods=['post'])
    def request_refund(self, request):
        """Request refund for an order."""
        order_id = request.data.get('order_id')
        reason = request.data.get('reason')

        try:
            order = Order.objects.get(id=order_id, user=request.user)
            if Refund.objects.filter(order=order).exists():
                return Response(
                    {'error': 'Refund already requested for this order'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            refund = Refund.objects.create(
                order=order,
                reason=reason,
                amount=order.final_price
            )
            return Response(
                RefundSerializer(refund).data,
                status=status.HTTP_201_CREATED
            )
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)


# ============================================================================
# USER FEATURE VIEWS
# ============================================================================

class UserProfileViewSet(viewsets.ViewSet):
    """User profile views."""
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def my_profile(self, request):
        """Get current user's profile."""
        serializer = UserProfileSerializer(request.user.profile)
        return Response({'data': serializer.data})

    @action(detail=False, methods=['put'])
    def update_profile(self, request):
        """Update user profile."""
        profile = request.user.profile
        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True, 'data': serializer.data})
        return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class WatchlistViewSet(viewsets.ViewSet):
    """Watchlist views."""
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def my_watchlist(self, request):
        """Get user's watchlist."""
        watchlist, created = Watchlist.objects.get_or_create(user=request.user)
        serializer = WatchlistSerializer(watchlist)
        return Response({'data': serializer.data})

    @action(detail=False, methods=['post'])
    def add_product(self, request):
        """Add product to watchlist."""
        product_id = request.data.get('product_id')
        try:
            product = Product.objects.get(id=product_id)
            watchlist, created = Watchlist.objects.get_or_create(user=request.user)
            watchlist.products.add(product)
            return Response({'success': True, 'message': 'Product added to watchlist'})
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['post'])
    def remove_product(self, request):
        """Remove product from watchlist."""
        product_id = request.data.get('product_id')
        try:
            watchlist = Watchlist.objects.get(user=request.user)
            watchlist.products.remove(product_id)
            return Response({'success': True, 'message': 'Product removed from watchlist'})
        except Watchlist.DoesNotExist:
            return Response({'error': 'Watchlist not found'}, status=status.HTTP_404_NOT_FOUND)


class ProductReviewViewSet(viewsets.ModelViewSet):
    """Product review viewset."""
    serializer_class = ProductReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter by product if provided."""
        product_id = self.request.query_params.get('product_id')
        if product_id:
            return ProductReview.objects.filter(product_id=product_id)
        return ProductReview.objects.all()

    def perform_create(self, serializer):
        """Create review for current user."""
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def my_reviews(self, request):
        """Get current user's reviews."""
        reviews = ProductReview.objects.filter(user=request.user)
        serializer = self.get_serializer(reviews, many=True)
        return Response({'data': serializer.data})


class ComplaintViewSet(viewsets.ModelViewSet):
    """Complaint viewset."""
    serializer_class = ComplaintSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Users see only their complaints, admins see all."""
        if self.request.user.profile.is_admin:
            return Complaint.objects.all()
        return Complaint.objects.filter(user=request.user)

    def perform_create(self, serializer):
        """Create complaint for current user."""
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def my_complaints(self, request):
        """Get current user's complaints."""
        complaints = Complaint.objects.filter(user=request.user)
        serializer = self.get_serializer(complaints, many=True)
        return Response({'data': serializer.data})


class ReferralViewSet(viewsets.ReadOnlyModelViewSet):
    """Referral viewset."""
    serializer_class = ReferralSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Users see their referrals."""
        return Referral.objects.filter(referrer=self.request.user)

    @action(detail=False, methods=['get'])
    def my_referrals(self, request):
        """Get user's referrals."""
        referrals = Referral.objects.filter(referrer=request.user)
        serializer = self.get_serializer(referrals, many=True)
        total_points = referrals.aggregate(total=models.Sum('points_earned'))['total'] or 0
        return Response({
            'data': serializer.data,
            'total_points': total_points,
            'total_referrals': referrals.count()
        })

    @action(detail=False, methods=['get'])
    def referral_info(self, request):
        """Get user's referral info."""
        profile = request.user.profile
        return Response({
            'referral_code': profile.referral_code,
            'referral_points': profile.referral_points,
            'total_referrals': profile.total_referrals
        })
