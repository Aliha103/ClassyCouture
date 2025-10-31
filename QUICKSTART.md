# ClassyCouture - Quick Start Guide

Get the ClassyCouture e-commerce platform running in minutes!

## One-Time Setup (First Time Only)

### Backend Setup

```bash
# Navigate to backend
cd ClassyCouture/backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Seed sample data
python manage.py seed_data

# (Optional) Create admin user
python manage.py createsuperuser
```

### Frontend Setup

```bash
# Navigate to frontend
cd ClassyCouture/frontend

# Install dependencies
npm install
```

## Running the Application (Every Time)

You need **two terminal windows/tabs** - one for backend, one for frontend.

### Terminal 1: Backend (Django)

```bash
cd ClassyCouture/backend

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Start Django server
python manage.py runserver 0.0.0.0:8000
```

Output should show:
```
Starting development server at http://127.0.0.1:8000/
```

### Terminal 2: Frontend (Next.js)

```bash
cd ClassyCouture/frontend

# Start Next.js dev server
npm run dev
```

Output should show:
```
> next dev
  ▲ Next.js 14.x.x
  - Local: http://localhost:3000
```

## Access the Application

Open your browser:

- **Frontend**: http://localhost:3000
  - View the main page with products, categories, reviews, newsletter signup

- **API**: http://localhost:8000/api/
  - View API documentation

- **Admin Panel**: http://localhost:8000/admin/
  - Manage products, categories, reviews
  - Username/password: Use credentials from `createsuperuser`

## What You'll See

### Frontend (localhost:3000)

1. **Hero Section** - Fashion banner with "Shop Now" button
2. **Featured Products** - 8-12 products with:
   - Product images
   - Prices (formatted as $XX.XX)
   - Star ratings
   - Review counts
3. **Categories** - 4 category cards (Women, Men, Accessories, Shoes)
4. **Customer Reviews** - 6 recent reviews with:
   - Customer names
   - 5-star ratings
   - Review text
   - Relative dates ("2 weeks ago")
5. **Newsletter Signup** - Email subscription form with validation
6. **Footer** - Links and copyright

### Backend API Endpoints

All responses return data wrapped in a `data` object:

```bash
# Featured products
curl http://localhost:8000/api/products/?featured=true

# All categories
curl http://localhost:8000/api/categories/

# Recent reviews (limit 6)
curl http://localhost:8000/api/reviews/?limit=6

# Subscribe to newsletter
curl -X POST http://localhost:8000/api/newsletter/subscribe/ \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com"}'
```

## Test the Integration

1. Open http://localhost:3000 in your browser
2. Check DevTools Network tab (F12)
3. Verify API calls are successful (200 status):
   - `products/?featured=true`
   - `categories/`
   - `reviews/?limit=6`
4. Try subscribing to newsletter at bottom of page
5. Visit http://localhost:8000/admin to see data in database

## Common Issues & Solutions

### "Cannot GET /api/products"
- Ensure backend is running: `python manage.py runserver`
- Check frontend `.env.local` has `NEXT_PUBLIC_API_URL=http://localhost:8000`

### "Failed to fetch products"
- Backend not running
- Check browser console for CORS errors
- Verify both servers are on correct ports (8000 for backend, 3000 for frontend)

### "Port 8000 already in use"
```bash
# Use different port
python manage.py runserver 0.0.0.0:8001

# Update frontend .env.local
NEXT_PUBLIC_API_URL=http://localhost:8001
```

### "No products available"
```bash
# Seed sample data
python manage.py seed_data
```

### Admin login not working
```bash
# Create new superuser
python manage.py createsuperuser
```

## File Locations

```
ClassyCouture/
├── frontend/
│   ├── app/page.tsx              (Main page)
│   ├── components/               (All page sections)
│   ├── .env.example              (Copy to .env.local)
│   └── package.json
├── backend/
│   ├── api/                      (Django app)
│   │   ├── models.py             (Database models)
│   │   ├── views.py              (API endpoints)
│   │   └── admin.py              (Admin panel config)
│   ├── config/
│   │   ├── settings.py           (CORS & DB config)
│   │   └── urls.py               (URL routing)
│   ├── manage.py
│   ├── requirements.txt
│   └── .env.example              (Optional config)
└── SETUP_GUIDE.md                (Detailed setup)
```

## Next Steps

1. **Customize Products**: Go to http://localhost:8000/admin/api/product and add/edit products
2. **Add Categories**: Create new categories in admin panel
3. **Moderate Reviews**: Manage customer reviews in admin
4. **View Subscribers**: Check newsletter subscriptions in admin

## Environment Variables

### Frontend (`.env.local`)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Backend (`.env` - optional, defaults work for dev)
```
DEBUG=True
SECRET_KEY=dev-key-change-in-production
ALLOWED_HOSTS=localhost,127.0.0.1
```

## Production Deployment

When ready for production, see `SETUP_GUIDE.md` for:
- Security configuration
- Database setup (PostgreSQL)
- Environment variables
- Deployment instructions

## Support

- Django docs: https://docs.djangoproject.com/
- DRF docs: https://www.django-rest-framework.org/
- Next.js docs: https://nextjs.org/docs
- See `SETUP_GUIDE.md` for detailed troubleshooting
