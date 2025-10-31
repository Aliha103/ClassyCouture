# ClassyCouture Backend - Django REST API

A complete Django REST API backend for ClassyCouture e-commerce platform. Fully integrated with the Next.js frontend with proper CORS configuration and responsive API design.

## Features

- **Django REST Framework** - Modern RESTful API architecture
- **CORS Configuration** - Seamless frontend-backend communication
- **Product Management** - Featured products with ratings and reviews
- **Category Management** - Organize products by categories
- **Review System** - Customer testimonials with ratings
- **Newsletter Subscription** - Email collection with validation
- **Admin Interface** - Complete Django admin panel for content management

## Tech Stack

- **Framework**: Django 4.2
- **API**: Django REST Framework 3.14
- **Database**: SQLite (development), PostgreSQL (production recommended)
- **CORS**: django-cors-headers 4.3
- **Python**: 3.8+

## Quick Start

### 1. Installation

Clone the repository and navigate to the backend directory:

```bash
cd ClassyCouture/backend
```

Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### 2. Configuration

Copy environment variables:

```bash
cp .env.example .env
```

Update `.env` with your settings (optional for development):

```
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 3. Database Setup

Run migrations:

```bash
python manage.py migrate
```

Seed sample data:

```bash
python manage.py seed_data
```

### 4. Create Admin User

```bash
python manage.py createsuperuser
```

### 5. Run Development Server

```bash
python manage.py runserver 0.0.0.0:8000
```

The API will be available at: `http://localhost:8000/api/`

## API Endpoints

### Products
- `GET /api/products/` - List all products
- `GET /api/products/?featured=true` - List featured products
- `GET /api/products/{id}/` - Retrieve specific product

### Categories
- `GET /api/categories/` - List all categories
- `GET /api/categories/{id}/` - Retrieve specific category

### Reviews
- `GET /api/reviews/` - List all reviews
- `GET /api/reviews/?limit=6` - List recent reviews with limit

### Newsletter
- `POST /api/newsletter/subscribe/` - Subscribe to newsletter

## Response Format

All endpoints return data in a consistent format:

```json
{
  "data": [
    {
      "id": 1,
      "name": "Product Name",
      "price": 99.99,
      ...
    }
  ]
}
```

### Product Response

```json
{
  "data": [
    {
      "id": 1,
      "name": "Classic Black Blazer",
      "price": "129.99",
      "image_url": "https://...",
      "rating": 4.5,
      "review_count": 2
    }
  ]
}
```

### Category Response

```json
{
  "data": [
    {
      "id": 1,
      "name": "Women",
      "image_url": "https://..."
    }
  ]
}
```

### Review Response

```json
{
  "data": [
    {
      "id": 1,
      "customer_name": "John Doe",
      "review_text": "Great product!",
      "rating": 5,
      "date": "2025-01-15T10:30:00Z"
    }
  ]
}
```

### Newsletter Response

```json
{
  "success": true,
  "message": "Successfully subscribed to newsletter",
  "email": "user@example.com"
}
```

## Admin Interface

Access the Django admin panel at: `http://localhost:8000/admin/`

**Default credentials**: Use the superuser account created with `createsuperuser`

### Admin Features

- **Categories**: Create, edit, and delete product categories
- **Products**: Manage products with featured flag
- **Reviews**: View and moderate customer reviews
- **Newsletter**: Manage email subscriptions

## CORS Configuration

The backend is pre-configured to accept requests from the frontend at:

- `http://localhost:3000` (Next.js dev server)
- `http://127.0.0.1:3000`

To add more allowed origins, edit `config/settings.py`:

```python
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://your-domain.com',
    'https://your-domain.com',
]
```

## Frontend Integration

The frontend expects the API at a specific base URL. Configure it in your `.env.local`:

```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Make sure both servers are running:

```bash
# Terminal 1 - Backend
cd ClassyCouture/backend
python manage.py runserver

# Terminal 2 - Frontend
cd ClassyCouture/frontend
npm run dev
```

## Database Models

### Category
- `id` - Primary key
- `name` - Category name (unique)
- `description` - Optional description
- `image_url` - Category image URL
- `created_at`, `updated_at` - Timestamps

### Product
- `id` - Primary key
- `name` - Product name
- `description` - Product description
- `price` - Product price (decimal)
- `image_url` - Product image URL
- `category` - Foreign key to Category
- `featured` - Boolean flag for featured products
- `created_at`, `updated_at` - Timestamps

### Review
- `id` - Primary key
- `product` - Foreign key to Product
- `customer_name` - Reviewer name
- `review_text` - Review content
- `rating` - Rating (1-5)
- `email` - Optional reviewer email
- `created_at`, `updated_at` - Timestamps

### Newsletter
- `id` - Primary key
- `email` - Subscriber email (unique)
- `is_active` - Subscription status
- `subscribed_at` - Subscription timestamp

## Development

### Create New Endpoint

1. Add model to `api/models.py`
2. Create serializer in `api/serializers.py`
3. Create viewset in `api/views.py`
4. Register in `api/urls.py`
5. Add to admin panel in `api/admin.py`

### Seed Custom Data

Edit `api/management/commands/seed_data.py` and run:

```bash
python manage.py seed_data
```

## Production Deployment

For production:

1. Set `DEBUG=False` in `.env`
2. Use a production database (PostgreSQL recommended)
3. Set `SECRET_KEY` to a secure random value
4. Update `ALLOWED_HOSTS` with your domain
5. Configure CORS for your production domain
6. Use environment variables for sensitive data
7. Use a production WSGI server (Gunicorn, uWSGI)

## Common Issues

### CORS Errors

If you see CORS errors:
1. Verify frontend URL in `CORS_ALLOWED_ORIGINS`
2. Check frontend `.env` has correct `NEXT_PUBLIC_API_URL`
3. Restart both servers

### Database Errors

If you see database errors:
1. Delete `db.sqlite3` to start fresh
2. Run migrations: `python manage.py migrate`
3. Seed data: `python manage.py seed_data`

### Port Already in Use

If port 8000 is already in use:

```bash
python manage.py runserver 0.0.0.0:8001
# Then update frontend NEXT_PUBLIC_API_URL=http://localhost:8001
```

## Testing

Run tests:

```bash
python manage.py test
```

## Documentation

For more information:

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework Documentation](https://www.django-rest-framework.org/)
- [django-cors-headers Documentation](https://github.com/adamchainz/django-cors-headers)

## License

Proprietary - ClassyCouture
