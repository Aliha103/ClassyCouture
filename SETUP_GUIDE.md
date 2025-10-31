# ClassyCouture - Complete Setup Guide

This guide walks you through setting up the complete ClassyCouture e-commerce platform with Next.js frontend and Django backend.

## Project Structure

```
ClassyCouture/
├── frontend/           # Next.js frontend application
├── backend/            # Django REST API backend
└── .git/              # Git repository
```

## Prerequisites

- Python 3.8+ (for Django backend)
- Node.js 18+ (for Next.js frontend)
- npm or yarn (for package management)

## Setup Instructions

### Part 1: Backend Setup (Django)

#### 1.1 Navigate to Backend Directory

```bash
cd ClassyCouture/backend
```

#### 1.2 Create Virtual Environment

```bash
# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

#### 1.3 Install Dependencies

```bash
pip install -r requirements.txt
```

#### 1.4 Environment Configuration (Optional)

Copy and customize environment variables:

```bash
cp .env.example .env
```

Default settings work for local development without modifications.

#### 1.5 Database Setup

Run migrations to create database tables:

```bash
python manage.py migrate
```

Seed sample data into database:

```bash
python manage.py seed_data
```

Output should show:
```
✓ Created category: Women
✓ Created category: Men
✓ Created category: Accessories
✓ Created category: Shoes
✓ Created product: Classic Black Blazer
... (more products and reviews)
✓ Database seeded successfully!
```

#### 1.6 Create Admin User (Optional)

```bash
python manage.py createsuperuser
```

Follow prompts to create superuser account for admin panel access.

#### 1.7 Start Backend Server

```bash
python manage.py runserver 0.0.0.0:8000
```

Backend will be available at: `http://localhost:8000`

Access admin panel at: `http://localhost:8000/admin/`

**Keep this terminal open** and proceed to frontend setup.

### Part 2: Frontend Setup (Next.js)

#### 2.1 Open New Terminal and Navigate to Frontend

```bash
cd ClassyCouture/frontend
```

#### 2.2 Install Dependencies

```bash
npm install
```

#### 2.3 Environment Configuration

Copy environment variables:

```bash
cp .env.example .env.local
```

Verify that `.env.local` contains:

```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

This tells the frontend where to find the API.

#### 2.4 Start Frontend Development Server

```bash
npm run dev
```

Frontend will be available at: `http://localhost:3000`

**Keep this terminal open**.

### Part 3: Verify Integration

#### 3.1 Check Frontend

Open your browser and navigate to: `http://localhost:3000`

You should see:
- Hero section with "ClassyCouture" banner
- Featured Products section loading products from API
- Categories section showing 4 categories
- Customer Reviews section with reviews
- Newsletter signup form
- Footer

#### 3.2 Verify API Calls

Open browser DevTools (F12) and check Network tab:

1. Refresh the page
2. Look for these API calls:
   - `products?featured=true` - should return 200
   - `categories/` - should return 200
   - `reviews?limit=6` - should return 200

3. Click each call and check Response tab
4. Response should have `data` object with proper structure

#### 3.3 Test Newsletter Signup

1. Scroll to "Join Our Newsletter" section
2. Enter your email: `test@example.com`
3. Click "Subscribe"
4. You should see success message: "Thank you! Check your email for confirmation."

#### 3.4 Test Admin Panel

1. Go to: `http://localhost:8000/admin/`
2. Login with superuser credentials created earlier
3. You should see:
   - Categories (4 items)
   - Products (10 items)
   - Reviews (6 items)
   - Newsletter subscriptions (if you tested signup)

## API Endpoints Reference

### Products

**List all featured products:**
```
GET http://localhost:8000/api/products/?featured=true
```

Response:
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

### Categories

**List all categories:**
```
GET http://localhost:8000/api/categories/
```

Response:
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

### Reviews

**List recent reviews:**
```
GET http://localhost:8000/api/reviews/?limit=6
```

Response:
```json
{
  "data": [
    {
      "id": 1,
      "customer_name": "Sarah Johnson",
      "review_text": "Excellent quality!",
      "rating": 5,
      "date": "2025-01-15T10:30:00Z"
    }
  ]
}
```

### Newsletter

**Subscribe to newsletter:**
```
POST http://localhost:8000/api/newsletter/subscribe/

Body:
{
  "email": "user@example.com"
}
```

Response:
```json
{
  "success": true,
  "message": "Successfully subscribed to newsletter",
  "email": "user@example.com"
}
```

## Frontend Features

### Responsive Design

The frontend is fully responsive:

- **Mobile (320px)**: 2-column product grid, single column reviews
- **Tablet (768px)**: 4-column product grid, 3-column categories, 2-column reviews
- **Desktop (1024px+)**: Optimized layouts with centered container

Test by:
1. Opening DevTools (F12)
2. Clicking device toggle button
3. Selecting different device sizes

### Error Handling

- **Loading States**: Shows skeleton loaders while data fetches
- **Error States**: Displays error messages with retry buttons
- **Missing Data**: Shows appropriate placeholders for missing images/data
- **Form Validation**: Newsletter email validation with error messages

### Components

```
page.tsx (Main page)
├── Hero.tsx (Hero banner)
├── FeaturedProducts.tsx (Product grid - fetches from /api/products?featured=true)
├── CategoriesSection.tsx (Category grid - fetches from /api/categories)
├── ReviewsSection.tsx (Review grid - fetches from /api/reviews?limit=6)
├── NewsletterSection.tsx (Email signup - POSTs to /api/newsletter/subscribe)
└── Footer.tsx (Footer links)
```

## Backend Structure

```
backend/
├── config/
│   ├── settings.py (Django configuration, CORS setup)
│   ├── urls.py (Main URL router)
│   └── wsgi.py (WSGI application)
├── api/
│   ├── models.py (Category, Product, Review, Newsletter)
│   ├── serializers.py (DRF serializers)
│   ├── views.py (API views/viewsets)
│   ├── urls.py (API URL routing)
│   ├── admin.py (Django admin configuration)
│   └── management/commands/
│       └── seed_data.py (Sample data generator)
├── manage.py (Django CLI)
└── requirements.txt (Python dependencies)
```

## Database Models

### Category
- `id` - Primary key
- `name` - Category name (unique)
- `image_url` - Category image URL

### Product
- `id` - Primary key
- `name` - Product name
- `price` - Product price
- `image_url` - Product image URL
- `category` - Foreign key to Category
- `featured` - Boolean (true/false)

### Review
- `id` - Primary key
- `product` - Foreign key to Product
- `customer_name` - Reviewer name
- `review_text` - Review content
- `rating` - Rating (1-5)
- `date` - Created timestamp (ISO format)

### Newsletter
- `email` - Subscriber email
- `subscribed_at` - Subscription date

## Troubleshooting

### Issue: Frontend shows "No products available"

**Solution:**
1. Verify backend is running: `http://localhost:8000/api/products/?featured=true`
2. Check browser console for errors
3. Verify `.env.local` has correct API URL
4. Run seed_data command in backend

### Issue: CORS errors in browser console

**Solution:**
1. Check backend server is running on port 8000
2. Verify frontend URL in backend `config/settings.py` CORS_ALLOWED_ORIGINS
3. Restart both servers

### Issue: "Email already subscribed" error

**Solution:**
Clear the newsletter table and re-seed:
```bash
python manage.py flush --no-input
python manage.py migrate
python manage.py seed_data
```

### Issue: Port 8000 already in use

**Solution:**
```bash
# Use different port
python manage.py runserver 0.0.0.0:8001

# Update frontend .env.local
NEXT_PUBLIC_API_URL=http://localhost:8001
```

### Issue: Python module not found error

**Solution:**
1. Make sure virtual environment is activated
2. Reinstall requirements: `pip install -r requirements.txt`

## Development Commands

### Backend

```bash
# Run migrations
python manage.py migrate

# Create migration for model changes
python manage.py makemigrations

# Seed data
python manage.py seed_data

# Create admin user
python manage.py createsuperuser

# Run tests
python manage.py test

# Run server on custom port
python manage.py runserver 0.0.0.0:8001
```

### Frontend

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Check for TypeScript errors
npm run typecheck
```

## Production Deployment

### Backend (Django)

1. Set `DEBUG=False` in `.env`
2. Use PostgreSQL instead of SQLite
3. Generate secure `SECRET_KEY`
4. Update `ALLOWED_HOSTS` with your domain
5. Configure CORS for production domain
6. Use production email backend
7. Deploy with Gunicorn or uWSGI
8. Use environment variables for all secrets

### Frontend (Next.js)

1. Build: `npm run build`
2. Update `.env.production` with production API URL
3. Deploy to Vercel, Netlify, or your own server
4. Ensure API URL is accessible from production domain

## Next Steps

1. **Customize Content**: Edit products, categories, and reviews in admin panel
2. **Add More Features**: Implement product detail pages, shopping cart, checkout
3. **Style Customization**: Modify Tailwind config and colors
4. **Backend Enhancements**: Add user authentication, orders, payments
5. **Testing**: Run test suite: `python manage.py test`

## Support

For issues or questions:
1. Check troubleshooting section above
2. Review Django documentation: https://docs.djangoproject.com/
3. Review DRF documentation: https://www.django-rest-framework.org/
4. Review Next.js documentation: https://nextjs.org/docs

---

**You're all set!** The ClassyCouture platform is now running with a fully integrated frontend and backend.
