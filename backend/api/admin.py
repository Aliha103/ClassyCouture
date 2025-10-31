"""
Django admin configuration for API models.
"""
from django.contrib import admin
from .models import (
    Category, Product, Review, Newsletter, UserProfile, Banner, Voucher,
    SalesAnalytics, Order, OrderItem, OrderTracking, Refund,
    Watchlist, ProductReview, Complaint, Referral
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category', 'featured', 'created_at']
    list_filter = ['featured', 'category', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'price')
        }),
        ('Media & Category', {
            'fields': ('image_url', 'category')
        }),
        ('Visibility', {
            'fields': ('featured',)
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
