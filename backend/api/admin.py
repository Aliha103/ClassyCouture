"""
Django admin configuration for API models.
"""
from django.contrib import admin
from .models import (
    Category, Product, Review, Newsletter, UserProfile, Banner, Voucher,
    SalesAnalytics, Order, OrderItem, OrderTracking, Refund,
    Watchlist, Complaint, Referral
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'inventory', 'category', 'featured', 'on_sale', 'discount_percent', 'created_at']
    list_filter = ['featured', 'on_sale', 'category', 'created_at']
    search_fields = ['name', 'description', 'sku']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'price', 'sku')
        }),
        ('Media & Category', {
            'fields': ('image_url', 'category')
        }),
        ('Inventory', {
            'fields': ('inventory',)
        }),
        ('Sales & Discounts', {
            'fields': ('featured', 'on_sale', 'discount_percent')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'product', 'rating', 'created_at']
    list_filter = ['rating', 'created_at', 'product']
    search_fields = ['customer_name', 'review_text', 'product__name']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Review Information', {
            'fields': ('product', 'customer_name', 'email', 'rating')
        }),
        ('Content', {
            'fields': ('review_text',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['email', 'is_active', 'subscribed_at']
    list_filter = ['is_active', 'subscribed_at']
    search_fields = ['email']
    readonly_fields = ['subscribed_at']
    actions = ['mark_active', 'mark_inactive']

    def mark_active(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, "Selected emails marked as active.")
    mark_active.short_description = "Mark selected as active"

    def mark_inactive(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, "Selected emails marked as inactive.")
    mark_inactive.short_description = "Mark selected as inactive"


# ============================================================================
# NEW ADMIN CLASSES
# ============================================================================

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'referral_code', 'referral_points', 'total_referrals', 'is_admin']
    list_filter = ['is_admin', 'created_at']
    search_fields = ['user__username', 'referral_code', 'phone']
    readonly_fields = ['referral_code', 'created_at', 'updated_at']


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'order', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Content', {
            'fields': ('title', 'description', 'image_url')
        }),
        ('CTA', {
            'fields': ('cta_text', 'cta_link')
        }),
        ('Settings', {
            'fields': ('is_active', 'order')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Voucher)
class VoucherAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount_value', 'discount_type', 'is_active', 'current_uses', 'max_uses']
    list_filter = ['discount_type', 'is_active', 'start_date', 'end_date']
    search_fields = ['code', 'description']
    readonly_fields = ['current_uses', 'created_at', 'updated_at']
    fieldsets = (
        ('Voucher Code', {
            'fields': ('code', 'description')
        }),
        ('Discount', {
            'fields': ('discount_type', 'discount_value', 'min_purchase')
        }),
        ('Usage', {
            'fields': ('max_uses', 'current_uses', 'is_active')
        }),
        ('Validity', {
            'fields': ('start_date', 'end_date')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(SalesAnalytics)
class SalesAnalyticsAdmin(admin.ModelAdmin):
    list_display = ['date', 'total_orders', 'total_revenue', 'total_profit', 'unique_customers']
    list_filter = ['date']
    readonly_fields = ['date', 'created_at']


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product', 'quantity', 'price_at_purchase', 'total']


class OrderTrackingInline(admin.StackedInline):
    model = OrderTracking
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'user', 'final_price', 'status', 'payment_status', 'created_at']
    list_filter = ['status', 'payment_status', 'created_at']
    search_fields = ['order_id', 'user__username', 'user__email']
    readonly_fields = ['order_id', 'created_at', 'updated_at']
    inlines = [OrderItemInline, OrderTrackingInline]
    fieldsets = (
        ('Order Information', {
            'fields': ('order_id', 'user', 'status', 'created_at', 'updated_at')
        }),
        ('Pricing', {
            'fields': ('total_price', 'discount_amount', 'final_price', 'voucher_code')
        }),
        ('Shipping', {
            'fields': ('shipping_address', 'phone')
        }),
        ('Payment', {
            'fields': ('payment_method', 'payment_status')
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
    )


@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
    list_display = ['order', 'status', 'amount', 'requested_at', 'processed_at']
    list_filter = ['status', 'requested_at', 'processed_at']
    search_fields = ['order__order_id', 'reason']
    readonly_fields = ['requested_at', 'processed_at']
    fieldsets = (
        ('Refund Request', {
            'fields': ('order', 'reason', 'amount', 'requested_at')
        }),
        ('Processing', {
            'fields': ('status', 'processed_by', 'processed_at', 'admin_notes')
        }),
    )


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'status', 'created_at', 'resolved_at']
    list_filter = ['status', 'created_at', 'resolved_at']
    search_fields = ['user__username', 'title', 'description']
    readonly_fields = ['created_at', 'updated_at', 'resolved_at']


@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    list_display = ['referrer', 'referred_user', 'points_earned', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['referrer__username', 'referred_user__username', 'referral_code']
    readonly_fields = ['created_at']
