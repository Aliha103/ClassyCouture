"""
Management command to seed sample data into the database.

Usage: python manage.py seed_data
"""
from django.core.management.base import BaseCommand
from api.models import Category, Product, Review
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = 'Seed the database with sample data'

    def handle(self, *args, **options):
        # Clear existing data
        Category.objects.all().delete()
        Product.objects.all().delete()
        Review.objects.all().delete()

        self.stdout.write(self.style.SUCCESS('Cleared existing data'))

        # Create categories
        categories_data = [
            {
                'name': 'Women',
                'image_url': 'https://images.unsplash.com/photo-1567777869896-9c5b0d22c3fe?w=400&h=400&fit=crop',
            },
            {
                'name': 'Men',
                'image_url': 'https://images.unsplash.com/photo-1614707267537-b85faf00021b?w=400&h=400&fit=crop',
            },
            {
                'name': 'Accessories',
                'image_url': 'https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?w=400&h=400&fit=crop',
            },
            {
                'name': 'Shoes',
                'image_url': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&h=400&fit=crop',
            },
        ]

        categories = {}
        for cat_data in categories_data:
            cat = Category.objects.create(**cat_data)
            categories[cat.name] = cat
            self.stdout.write(self.style.SUCCESS(f'✓ Created category: {cat.name}'))

        # Create products
        products_data = [
            {
                'name': 'Classic Black Blazer',
                'description': 'Elegant and timeless black blazer perfect for any occasion',
                'price': '129.99',
                'image_url': 'https://images.unsplash.com/photo-1591047990973-2c43eb69fcee?w=400&h=500&fit=crop',
                'category': categories['Women'],
                'featured': True,
            },
            {
                'name': 'White Silk Blouse',
                'description': 'Luxurious white silk blouse with premium finish',
                'price': '89.99',
                'image_url': 'https://images.unsplash.com/photo-1551028719-00167b16ebc5?w=400&h=500&fit=crop',
                'category': categories['Women'],
                'featured': True,
            },
            {
                'name': 'Navy Blue Dress',
                'description': 'Sophisticated navy blue dress for elegant evenings',
                'price': '149.99',
                'image_url': 'https://images.unsplash.com/photo-1595777707802-c2265d4c6596?w=400&h=500&fit=crop',
                'category': categories['Women'],
                'featured': True,
            },
            {
                'name': 'Premium Denim Jeans',
                'description': 'High-quality denim jeans with comfortable fit',
                'price': '79.99',
                'image_url': 'https://images.unsplash.com/photo-1542272604-787c62d465d1?w=400&h=500&fit=crop',
                'category': categories['Women'],
                'featured': True,
            },
            {
                'name': 'Charcoal Suit',
                'description': 'Professional charcoal suit perfect for business',
                'price': '299.99',
                'image_url': 'https://images.unsplash.com/photo-1591047990973-2c43eb69fcee?w=400&h=500&fit=crop',
                'category': categories['Men'],
                'featured': True,
            },
            {
                'name': 'Oxford Button-Down Shirt',
                'description': 'Classic oxford button-down shirt in white',
                'price': '59.99',
                'image_url': 'https://images.unsplash.com/photo-1596455160519-b21d5bb269fe?w=400&h=500&fit=crop',
                'category': categories['Men'],
                'featured': True,
            },
            {
                'name': 'Leather Dress Shoes',
                'description': 'Premium leather dress shoes for formal occasions',
                'price': '159.99',
                'image_url': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&h=500&fit=crop',
                'category': categories['Shoes'],
                'featured': True,
            },
            {
                'name': 'Sneaker Collection',
                'description': 'Modern and comfortable sneakers for everyday wear',
                'price': '99.99',
                'image_url': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&h=500&fit=crop',
                'category': categories['Shoes'],
                'featured': True,
            },
            {
                'name': 'Silk Scarf',
                'description': 'Elegant silk scarf with beautiful patterns',
                'price': '49.99',
                'image_url': 'https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?w=400&h=500&fit=crop',
                'category': categories['Accessories'],
                'featured': False,
            },
            {
                'name': 'Designer Handbag',
                'description': 'Sophisticated leather handbag for daily use',
                'price': '189.99',
                'image_url': 'https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=400&h=500&fit=crop',
                'category': categories['Accessories'],
                'featured': True,
            },
        ]

        products = {}
        for prod_data in products_data:
            prod = Product.objects.create(**prod_data)
            products[prod.name] = prod
            self.stdout.write(self.style.SUCCESS(f'✓ Created product: {prod.name}'))

        # Create reviews
        sample_reviews = [
            {
                'product': products['Classic Black Blazer'],
                'customer_name': 'Sarah Johnson',
                'review_text': 'Excellent quality blazer! Fits perfectly and looks very professional. Highly recommended!',
                'rating': 5,
                'email': 'sarah@example.com',
            },
            {
                'product': products['Classic Black Blazer'],
                'customer_name': 'Emma Wilson',
                'review_text': 'Great blazer, very versatile. Perfect for work and casual outings.',
                'rating': 4,
                'email': 'emma@example.com',
            },
            {
                'product': products['White Silk Blouse'],
                'customer_name': 'Michael Chen',
                'review_text': 'Premium quality silk. The material feels luxurious and the fit is impeccable.',
                'rating': 5,
                'email': 'michael@example.com',
            },
            {
                'product': products['Navy Blue Dress'],
                'customer_name': 'Jessica Brown',
                'review_text': 'Absolutely stunning dress! Wore it to an evening event and received many compliments.',
                'rating': 5,
                'email': 'jessica@example.com',
            },
            {
                'product': products['Charcoal Suit'],
                'customer_name': 'David Martinez',
                'review_text': 'Professional suit with perfect tailoring. Great value for money.',
                'rating': 4,
                'email': 'david@example.com',
            },
            {
                'product': products['Leather Dress Shoes'],
                'customer_name': 'Robert Taylor',
                'review_text': 'Comfortable and stylish. These shoes are perfect for business meetings.',
                'rating': 4,
                'email': 'robert@example.com',
            },
        ]

        for review_data in sample_reviews:
            review = Review.objects.create(**review_data)
            self.stdout.write(self.style.SUCCESS(
                f'✓ Created review: {review.customer_name} for {review.product.name}'
            ))

        self.stdout.write(self.style.SUCCESS('\n✓ Database seeded successfully!'))
