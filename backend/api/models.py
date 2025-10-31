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


# ============================================================================
# USER MANAGEMENT & PROFILE
# ============================================================================

class UserProfile(models.Model):
    """Extended user profile."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    referral_code = models.CharField(max_length=20, unique=True)
    referral_points = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    total_referrals = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} Profile"


# ============================================================================
# ADMIN FEATURES
# ============================================================================

class Banner(models.Model):
    """Homepage banner control."""
    title = models.CharField(max_length=200)
    description = models.TextField()
    image_url = models.URLField()
    cta_text = models.CharField(max_length=100, default="Shop Now")
    cta_link = models.CharField(max_length=200, default="/shop")
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class Voucher(models.Model):
    """Discount voucher/coupon model."""
    DISCOUNT_TYPES = [
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed Amount'),
    ]

    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPES, default='percentage')
    discount_value = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    min_purchase = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    max_uses = models.IntegerField(null=True, blank=True)
    current_uses = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    is_active = models.BooleanField(default=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.code} - {self.discount_value}{('%' if self.discount_type == 'percentage' else '$')}"

    @property
    def is_expired(self):
        """Check if voucher is expired."""
        return timezone.now() > self.end_date

    @property
    def can_use(self):
        """Check if voucher can be used."""
        if not self.is_active or self.is_expired:
            return False
        if self.max_uses and self.current_uses >= self.max_uses:
            return False
        return True


class SalesAnalytics(models.Model):
    """Track sales and analytics."""
    date = models.DateField(auto_now_add=True)
    total_orders = models.IntegerField(default=0)
    total_revenue = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_items_sold = models.IntegerField(default=0)
    avg_order_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_profit = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    unique_customers = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
        verbose_name_plural = "Sales Analytics"

    def __str__(self):
        return f"Sales - {self.date}"


# ============================================================================
# ORDER MANAGEMENT
# ============================================================================

class Order(models.Model):
    """Customer order model."""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    order_id = models.CharField(max_length=50, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    total_price = models.DecimalField(max_digits=15, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    final_price = models.DecimalField(max_digits=15, decimal_places=2)
    voucher_code = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', db_index=True)
    shipping_address = models.TextField()
    phone = models.CharField(max_length=20)
    payment_method = models.CharField(max_length=50)
    payment_status = models.CharField(max_length=20, default='pending')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"Order {self.order_id}"

    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = f"ORD-{uuid.uuid4().hex[:10].upper()}"
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    """Items in an order."""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    def save(self, *args, **kwargs):
        self.total = self.price_at_purchase * self.quantity
        super().save(*args, **kwargs)


class OrderTracking(models.Model):
    """Track order status updates."""
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='tracking')
    current_location = models.CharField(max_length=200, blank=True)
    estimated_delivery = models.DateTimeField(null=True, blank=True)
    carrier = models.CharField(max_length=100, blank=True)
    tracking_number = models.CharField(max_length=100, blank=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Tracking - {self.order.order_id}"


class Refund(models.Model):
    """Refund/Return requests."""
    STATUS_CHOICES = [
        ('requested', 'Requested'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('refunded', 'Refunded'),
    ]

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='refund')
    reason = models.TextField()
    requested_at = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='requested')
    admin_notes = models.TextField(blank=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    processed_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='refunds_processed')

    def __str__(self):
        return f"Refund - {self.order.order_id}"


# ============================================================================
# USER FEATURES
# ============================================================================

class Watchlist(models.Model):
    """User watchlist for products."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='watchlist')
    products = models.ManyToManyField(Product, related_name='in_watchlists')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Watchlist - {self.user.username}"


class ProductReview(models.Model):
    """User product reviews."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='user_reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_reviews')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    title = models.CharField(max_length=200)
    review_text = models.TextField()
    is_verified_purchase = models.BooleanField(default=False)
    helpful_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['product', 'user']

    def __str__(self):
        return f"Review - {self.user.username} for {self.product.name}"


class Complaint(models.Model):
    """Product complaints/issues."""
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]

    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name='complaints')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='complaints')
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    resolution = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Complaint - {self.user.username}"


class Referral(models.Model):
    """Referral tracking."""
    referrer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referrals_given')
    referred_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referral_source')
    referral_code = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    points_earned = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['referrer', 'referred_user']

    def __str__(self):
        return f"Referral - {self.referrer.username} → {self.referred_user.username}"
