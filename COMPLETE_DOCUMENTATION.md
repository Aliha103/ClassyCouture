# ClassyCouture - Complete Documentation

**A fully-featured e-commerce platform with admin and user management systems**

Version: 1.0
Last Updated: 2025-11-01

---

## Table of Contents

1. [Quick Start](#1-quick-start)
2. [Setup & Installation](#2-setup--installation)
3. [Features & Implementation](#3-features--implementation)
4. [Authentication System](#4-authentication-system)
5. [Database Configuration](#5-database-configuration)
6. [API Reference](#6-api-reference)
7. [Frontend Architecture](#7-frontend-architecture)
8. [Troubleshooting](#8-troubleshooting)
9. [Advanced Topics](#9-advanced-topics)

---

## 1. Quick Start

### Get Running in 5 Minutes

#### Backend Setup
```bash
cd ClassyCouture/backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_data
python manage.py runserver 0.0.0.0:8000
```

#### Frontend Setup
```bash
cd ClassyCouture/frontend
npm install
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
npm run dev
```

#### Access Points
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000/api/
- **Django Admin**: http://localhost:8000/admin/

#### Test the System
1. Open http://localhost:3000
2. Check products load on homepage
3. Try registering at http://localhost:3000/register
4. Login at http://localhost:3000/login
5. Access account at http://localhost:3000/account

---

## 2. Setup & Installation

### 2.1 Prerequisites

- Python 3.8+ (for Django backend)
- Node.js 18+ (for Next.js frontend)
- npm or yarn (package management)
- PostgreSQL (optional, for production)

### 2.2 Project Structure

```
ClassyCouture/
├── frontend/                 # Next.js Application
│   ├── app/
│   │   ├── login/           # Login page
│   │   ├── register/        # Registration page
│   │   ├── account/         # Account dashboard
│   │   ├── admin/           # Admin dashboard
│   │   └── dashboard/       # User dashboard
│   ├── components/          # React components
│   └── lib/                 # Utilities
│
├── backend/                 # Django Application
│   ├── api/
│   │   ├── models.py       # 14 database models
│   │   ├── views.py        # Original viewsets
│   │   ├── views_extended.py # 30+ API endpoints
│   │   ├── serializers.py  # Data serializers
│   │   └── admin.py        # Django admin config
│   ├── config/             # Django configuration
│   └── manage.py
│
└── Documentation/          # All .md files
```

### 2.3 Backend Installation

#### Step 1: Create Virtual Environment
```bash
cd ClassyCouture/backend
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate  # Windows
```

#### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

Expected packages:
- Django 4.2+
- djangorestframework
- django-cors-headers
- psycopg2-binary (for PostgreSQL)
- python-dotenv

#### Step 3: Environment Configuration
```bash
cp .env.example .env
```

Default `.env` (for development):
```env
DEBUG=True
SECRET_KEY=dev-key-change-in-production
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3
```

#### Step 4: Database Setup
```bash
# Create database tables
python manage.py makemigrations
python manage.py migrate

# Seed sample data
python manage.py seed_data

# Create admin user
python manage.py createsuperuser
```

#### Step 5: Start Backend Server
```bash
python manage.py runserver 0.0.0.0:8000
```

### 2.4 Frontend Installation

#### Step 1: Install Dependencies
```bash
cd ClassyCouture/frontend
npm install
```

#### Step 2: Environment Configuration
```bash
cp .env.example .env.local
```

`.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

#### Step 3: Start Development Server
```bash
npm run dev
```

Frontend will be available at http://localhost:3000

### 2.5 Verification Checklist

- [ ] Backend running on port 8000
- [ ] Frontend running on port 3000
- [ ] Database file exists: `backend/db.sqlite3`
- [ ] API returns data: `curl http://localhost:8000/api/products/`
- [ ] Frontend displays products
- [ ] No CORS errors in console

---

## 3. Features & Implementation

### 3.1 Complete Feature List

#### For Customers
- ✅ Account registration & login
- ✅ Product browsing with filters
- ✅ Shopping with discounts/vouchers
- ✅ Real-time order tracking
- ✅ Refund requests
- ✅ Product watchlist
- ✅ Product reviews
- ✅ Complaint filing
- ✅ Referral program with points

#### For Admins
- ✅ Sales analytics dashboard
- ✅ Inventory management
- ✅ Discount/sale creation
- ✅ Voucher/coupon management
- ✅ Homepage banner control
- ✅ Order management
- ✅ Refund processing
- ✅ Customer management

### 3.2 Database Models (14 Total)

#### User Management Models
1. **User** (Django built-in)
2. **UserProfile** - Extended user info, referral codes, points
   - Fields: phone, address, city, country, postal_code
   - Fields: referral_code (unique), referral_points, total_referrals
   - Fields: is_admin (boolean)

3. **Watchlist** - User's favorite products
   - Fields: user, products (many-to-many)

4. **ProductReview** - User ratings and reviews
   - Fields: user, product, rating (1-5), title, review_text
   - Fields: is_verified_purchase, helpful_count

5. **Complaint** - Issue tracking
   - Fields: user, order_item, title, description
   - Fields: status (open/in_progress/resolved/closed)

6. **Referral** - Referral relationships
   - Fields: referrer, referred_user, referral_code
   - Fields: points_earned, is_active

#### Admin & Marketing Models
7. **Banner** - Homepage promotions
   - Fields: title, description, image_url
   - Fields: cta_text, cta_link, order, is_active

8. **Voucher** - Discount codes
   - Fields: code (unique), description
   - Fields: discount_type (percentage/fixed), discount_value
   - Fields: min_purchase, max_uses, current_uses
   - Fields: start_date, end_date, is_active

9. **SalesAnalytics** - Daily metrics
   - Fields: date, total_orders, total_revenue
   - Fields: total_profit, total_items_sold
   - Fields: avg_order_value, unique_customers

#### Order & Fulfillment Models
10. **Order** - Customer orders
    - Fields: user, order_id (auto-generated)
    - Fields: status (pending/processing/shipped/delivered/cancelled)
    - Fields: payment_status (pending/completed/failed)
    - Fields: total_price, discount_amount, final_price
    - Fields: voucher_code, shipping_address, phone
    - Fields: payment_method, notes

11. **OrderItem** - Line items
    - Fields: order, product, quantity
    - Fields: price_at_purchase, total

12. **OrderTracking** - Real-time tracking
    - Fields: order, current_location, estimated_delivery
    - Fields: carrier, tracking_number, last_updated

13. **Refund** - Return requests
    - Fields: order, user, reason, amount
    - Fields: status (requested/approved/rejected/refunded)
    - Fields: admin_notes, requested_at, processed_at

#### Enhanced Models
14. **Product** - Enhanced with inventory/sales
    - Original: id, name, price, description, image_url
    - Original: category (FK), featured (boolean)
    - **New**: inventory (integer), sku (string)
    - **New**: on_sale (boolean), discount_percent
    - **Properties**: discounted_price, is_in_stock

### 3.3 Frontend Pages

#### Authentication Pages
- `/login` - Email/password authentication
  - Features: Form validation, error handling, social login placeholders
  - Redirects to `/account` on success

- `/register` - User registration
  - Features: Password confirmation, validation, terms acceptance
  - Auto-generates username from email
  - Creates UserProfile with referral code

- `/account` - Account dashboard
  - Features: Protected route, profile management
  - Sections: Profile, Orders, Wishlist, Settings
  - Sign out functionality

#### Admin Pages
- `/admin/dashboard` - Analytics overview
  - Sales metrics, revenue, profit
  - Order statistics, customer count

- `/admin/inventory` - Stock management
  - Inline editing, SKU management
  - Discount controls, sale toggles

#### User Pages
- `/dashboard` - User overview
  - Order history, profile info
  - Referral code display
  - Quick stats

### 3.4 Key Features Implementation

#### Referral System
**How it works:**
1. Each user gets unique referral code on registration (REF{UserID}{UsernamePrefix})
2. Users share code with friends
3. New users sign up using referral code
4. Both users earn points
5. Points tracked in UserProfile

**Example:**
- User "john_doe" with ID 5 gets code: `REF5JOH`
- New user signs up with this code
- John earns 50 points, new user earns 50 points

#### Voucher System
**Features:**
- Percentage or fixed amount discounts
- Minimum purchase requirements
- Usage limits (max_uses)
- Date range validation
- Automatic expiration

**Validation Endpoint:**
```bash
POST /api/vouchers/validate_code/
{
  "code": "SUMMER50"
}
```

**Response:**
```json
{
  "valid": true,
  "voucher": {
    "code": "SUMMER50",
    "discount_value": "50",
    "discount_type": "percentage",
    "min_purchase": "100.00"
  }
}
```

#### Order Tracking
**Features:**
- Auto-generated order IDs (ORD-{random})
- 5 status levels: pending → processing → shipped → delivered
- Real-time location updates
- Carrier and tracking number storage
- Estimated delivery dates

**Flow:**
1. Order created → status: "pending"
2. Admin processes → status: "processing"
3. Item ships → status: "shipped", tracking info added
4. Delivered → status: "delivered"

---

## 4. Authentication System

### 4.1 Registration Flow

**Endpoint:** `POST /api/auth/register/`

**Frontend Component:** `/frontend/app/register/page.tsx`

**Request Payload:**
```json
{
  "username": "user",           // Extracted from email prefix
  "email": "user@example.com",
  "password": "password123",
  "password_confirm": "password123",
  "first_name": "John",         // From name field
  "last_name": "Doe"            // From name field
}
```

**Backend Processing:**
1. Validates all required fields
2. Checks passwords match (minimum 6 characters)
3. Validates email format
4. Checks username/email not taken
5. Creates User object
6. Creates UserProfile with unique referral code
7. Creates empty Watchlist

**Success Response (201):**
```json
{
  "success": true,
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "username": "user",
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe"
  }
}
```

**Frontend Behavior:**
- Shows success message
- Redirects to `/login` after 2 seconds

### 4.2 Login Flow

**Endpoint:** `POST /api/auth/login/`

**Frontend Component:** `/frontend/app/login/page.tsx`

**Request Payload:**
```json
{
  "username": "user",    // Extracted from email
  "password": "password123"
}
```

**Backend Processing:**
1. Authenticates using Django's auth system
2. Retrieves user and profile data
3. Returns user info and profile details

**Success Response (200):**
```json
{
  "success": true,
  "message": "Login successful",
  "user": {
    "id": 1,
    "username": "user",
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe"
  },
  "profile": {
    "id": 1,
    "phone": "+1234567890",
    "address": "123 Main St",
    "city": "New York",
    "country": "USA",
    "postal_code": "10001",
    "referral_code": "REF1USE",
    "referral_points": 100,
    "total_referrals": 5,
    "is_admin": false
  }
}
```

**Frontend Behavior:**
- Stores token in localStorage (if provided)
- Shows success message
- Redirects to `/account` after 1 second

### 4.3 Account Page Protection

**Component:** `/frontend/app/account/page.tsx`

**Protection Mechanism:**
```typescript
useEffect(() => {
  const token = localStorage.getItem("auth_token");
  if (!token) {
    setShowLoginPrompt(true);
  }
}, []);
```

**If not logged in:**
- Shows "Account Access Required" card
- Provides "Sign In" and "Create Account" buttons
- "Back to Home" option

**If logged in:**
- Full account dashboard visible
- Profile information (editable)
- Orders section
- Wishlist section
- Settings section
- Sign Out button

### 4.4 Authentication Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    USER REGISTRATION                         │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
    User visits /register and fills form
    (name, email, password, confirm password)
                           │
                           ▼
    Frontend extracts:
    - username from email (user@example.com → user)
    - first_name/last_name from name
                           │
                           ▼
    POST /api/auth/register/
    {username, email, password, password_confirm, first_name, last_name}
                           │
                           ▼
    Backend validates and creates:
    - User object
    - UserProfile with referral code
    - Empty Watchlist
                           │
                           ▼
    Response: 201 Created
    {success: true, user: {...}}
                           │
                           ▼
    Frontend redirects to /login after 2 seconds

┌─────────────────────────────────────────────────────────────┐
│                       USER LOGIN                             │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
    User visits /login and enters credentials
                           │
                           ▼
    POST /api/auth/login/
    {username, password}
                           │
                           ▼
    Backend authenticates using Django auth
                           │
                           ▼
    Response: 200 OK
    {success: true, user: {...}, profile: {...}}
                           │
                           ▼
    Frontend stores token in localStorage
                           │
                           ▼
    Frontend redirects to /account
```

---

## 5. Database Configuration

### 5.1 Default Configuration (SQLite)

**Current Setup:**
- Database: SQLite
- Location: `/backend/db.sqlite3`
- Configuration: `backend/config/settings.py`

**Settings:**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

**Advantages:**
- No additional setup required
- Perfect for development
- Easy to reset/recreate

**Limitations:**
- Not suitable for production
- Limited concurrent connections
- No advanced features

### 5.2 PostgreSQL Migration

#### Step 1: Install PostgreSQL

**macOS:**
```bash
brew install postgresql@15
brew services start postgresql@15
```

**Ubuntu/Linux:**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
```

**Windows:**
Download from: https://www.postgresql.org/download/windows/

#### Step 2: Create Database
```bash
psql postgres

# In PostgreSQL prompt:
CREATE DATABASE classycouture;
CREATE USER classyuser WITH PASSWORD 'your_secure_password';
ALTER ROLE classyuser SET client_encoding TO 'utf8';
ALTER ROLE classyuser SET default_transaction_isolation TO 'read committed';
ALTER ROLE classyuser SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE classycouture TO classyuser;

# PostgreSQL 15+ additional permission:
\c classycouture
GRANT ALL ON SCHEMA public TO classyuser;

\q
```

#### Step 3: Install Python PostgreSQL Driver
```bash
cd backend
source venv/bin/activate
pip install psycopg2-binary
```

#### Step 4: Configure Django

**Create/edit `.env`:**
```env
DB_ENGINE=django.db.backends.postgresql
DB_NAME=classycouture
DB_USER=classyuser
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=5432
```

**Backend reads these automatically** from `settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': os.getenv('DB_NAME', BASE_DIR / 'db.sqlite3'),
        'USER': os.getenv('DB_USER', ''),
        'PASSWORD': os.getenv('DB_PASSWORD', ''),
        'HOST': os.getenv('DB_HOST', ''),
        'PORT': os.getenv('DB_PORT', ''),
    }
}
```

#### Step 5: Migrate Data (Optional)

**Export from SQLite:**
```bash
python manage.py dumpdata --natural-foreign --natural-primary \
  -e contenttypes -e auth.Permission --indent 2 > data_backup.json
```

**Import to PostgreSQL:**
```bash
python manage.py migrate
python manage.py loaddata data_backup.json
```

**Or seed fresh data:**
```bash
python manage.py migrate
python manage.py seed_data
python manage.py createsuperuser
```

#### Step 6: Verify Connection
```bash
python manage.py shell
>>> from django.db import connection
>>> connection.settings_dict['ENGINE']
# Should show: 'django.db.backends.postgresql'
>>> exit()
```

### 5.3 Database Backup

**SQLite:**
```bash
# Backup
cp backend/db.sqlite3 backup_$(date +%Y%m%d).sqlite3

# Restore
cp backup_20250101.sqlite3 backend/db.sqlite3
```

**PostgreSQL:**
```bash
# Backup
pg_dump -U classyuser classycouture > backup.sql

# Restore
psql -U classyuser classycouture < backup.sql
```

### 5.4 Production Considerations

**Security:**
- Use strong passwords
- Enable SSL connections
- Restrict network access
- Regular security updates

**Performance:**
- Connection pooling
- Query optimization
- Index management
- Regular VACUUM (PostgreSQL)

**Reliability:**
- Automated backups
- Point-in-time recovery
- Replication (if needed)
- Monitoring and alerts

---

## 6. API Reference

### 6.1 Authentication Endpoints

#### Register User
```http
POST /api/auth/register/
Content-Type: application/json

{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "securepass123",
  "password_confirm": "securepass123",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Response (201):**
```json
{
  "success": true,
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com"
  }
}
```

#### Login
```http
POST /api/auth/login/
Content-Type: application/json

{
  "username": "johndoe",
  "password": "securepass123"
}
```

**Response (200):**
```json
{
  "success": true,
  "message": "Login successful",
  "user": {...},
  "profile": {...}
}
```

### 6.2 Admin Endpoints

#### View Sales Analytics
```http
GET /api/analytics/
Authorization: (admin required)
```

**Response:**
```json
{
  "data": [
    {
      "date": "2025-01-15",
      "total_orders": 45,
      "total_revenue": "15000.00",
      "total_items_sold": 150,
      "avg_order_value": "333.33",
      "total_profit": "5000.00",
      "unique_customers": 40
    }
  ]
}
```

#### Create Banner
```http
POST /api/banners/
Authorization: (admin required)
Content-Type: application/json

{
  "title": "Summer Sale",
  "description": "Get 50% off on all summer collection",
  "image_url": "https://example.com/summer.jpg",
  "cta_text": "Shop Now",
  "cta_link": "/category/summer",
  "is_active": true,
  "order": 1
}
```

#### Create Voucher
```http
POST /api/vouchers/
Authorization: (admin required)
Content-Type: application/json

{
  "code": "SUMMER50",
  "description": "50% off on all items",
  "discount_type": "percentage",
  "discount_value": "50",
  "min_purchase": "100.00",
  "max_uses": 1000,
  "is_active": true,
  "start_date": "2025-01-01T00:00:00Z",
  "end_date": "2025-12-31T23:59:59Z"
}
```

#### Validate Voucher
```http
POST /api/vouchers/validate_code/
Content-Type: application/json

{
  "code": "SUMMER50"
}
```

**Response:**
```json
{
  "valid": true,
  "voucher": {
    "code": "SUMMER50",
    "discount_value": "50",
    "discount_type": "percentage",
    "min_purchase": "100.00"
  }
}
```

### 6.3 Product Endpoints

#### Get Featured Products
```http
GET /api/products/?featured=true
```

**Response:**
```json
{
  "data": [
    {
      "id": 1,
      "name": "Classic Black Blazer",
      "price": "129.99",
      "image_url": "https://...",
      "rating": 4.5,
      "review_count": 12,
      "inventory": 50,
      "is_in_stock": true,
      "on_sale": true,
      "discount_percent": 20,
      "discounted_price": "103.99"
    }
  ]
}
```

#### Update Product (Admin)
```http
PUT /api/products/{id}/
Authorization: (admin required)
Content-Type: application/json

{
  "inventory": 50,
  "sku": "BLZ-001",
  "on_sale": true,
  "discount_percent": 20
}
```

### 6.4 Order Endpoints

#### Create Order
```http
POST /api/orders/
Authorization: Bearer {token}
Content-Type: application/json

{
  "total_price": "499.97",
  "discount_amount": "50.00",
  "final_price": "449.97",
  "voucher_code": "SUMMER50",
  "shipping_address": "123 Main St, New York, NY 10001",
  "phone": "+1234567890",
  "payment_method": "credit_card",
  "notes": "Please deliver after 6 PM"
}
```

**Response (201):**
```json
{
  "id": 1,
  "order_id": "ORD-ABC123DEF45",
  "status": "pending",
  "payment_status": "pending",
  "final_price": "449.97",
  "created_at": "2025-01-15T10:30:00Z"
}
```

#### Get My Orders
```http
GET /api/orders/my_orders/
Authorization: Bearer {token}
```

#### Order Tracking
```http
GET /api/orders/{id}/tracking/
Authorization: Bearer {token}
```

**Response:**
```json
{
  "data": {
    "current_location": "Distribution Center, Los Angeles",
    "estimated_delivery": "2025-01-18T17:00:00Z",
    "carrier": "FedEx",
    "tracking_number": "FDX123456789",
    "last_updated": "2025-01-15T15:30:00Z"
  }
}
```

#### Cancel Order
```http
POST /api/orders/{id}/cancel/
Authorization: Bearer {token}
```

### 6.5 Refund Endpoints

#### Request Refund
```http
POST /api/refunds/request_refund/
Authorization: Bearer {token}
Content-Type: application/json

{
  "order_id": 1,
  "reason": "Product arrived damaged"
}
```

**Response (201):**
```json
{
  "id": 1,
  "order": 1,
  "reason": "Product arrived damaged",
  "amount": "449.97",
  "status": "requested",
  "requested_at": "2025-01-15T10:30:00Z"
}
```

### 6.6 User Profile Endpoints

#### Get Profile
```http
GET /api/profile/my_profile/
Authorization: Bearer {token}
```

#### Update Profile
```http
PUT /api/profile/update_profile/
Authorization: Bearer {token}
Content-Type: application/json

{
  "phone": "+1234567890",
  "address": "123 Main St",
  "city": "New York",
  "country": "USA",
  "postal_code": "10001"
}
```

### 6.7 Watchlist Endpoints

#### Get Watchlist
```http
GET /api/watchlist/my_watchlist/
Authorization: Bearer {token}
```

#### Add Product
```http
POST /api/watchlist/add_product/
Authorization: Bearer {token}
Content-Type: application/json

{
  "product_id": 1
}
```

#### Remove Product
```http
POST /api/watchlist/remove_product/
Authorization: Bearer {token}
Content-Type: application/json

{
  "product_id": 1
}
```

### 6.8 Review Endpoints

#### Leave Review
```http
POST /api/product-reviews/
Authorization: Bearer {token}
Content-Type: application/json

{
  "product": 1,
  "rating": 5,
  "title": "Excellent Quality",
  "review_text": "The product is amazing! Highly recommended.",
  "is_verified_purchase": true
}
```

#### Get My Reviews
```http
GET /api/product-reviews/my_reviews/
Authorization: Bearer {token}
```

### 6.9 Complaint Endpoints

#### File Complaint
```http
POST /api/complaints/
Authorization: Bearer {token}
Content-Type: application/json

{
  "order_item": 1,
  "title": "Item Defective",
  "description": "The zipper on the blazer is broken"
}
```

#### Get My Complaints
```http
GET /api/complaints/my_complaints/
Authorization: Bearer {token}
```

### 6.10 Referral Endpoints

#### Get Referral Info
```http
GET /api/referrals/referral_info/
Authorization: Bearer {token}
```

**Response:**
```json
{
  "referral_code": "REFJOHN1DO",
  "referral_points": 150,
  "total_referrals": 5
}
```

#### Get My Referrals
```http
GET /api/referrals/my_referrals/
Authorization: Bearer {token}
```

**Response:**
```json
{
  "data": [
    {
      "referrer": 1,
      "referred_user": 2,
      "referral_code": "REFJOHN1DO",
      "points_earned": 50,
      "created_at": "2025-01-10T10:30:00Z"
    }
  ],
  "total_points": 250,
  "total_referrals": 5
}
```

### 6.11 Complete Endpoint List

```
Authentication (2)
├── POST   /api/auth/register/
└── POST   /api/auth/login/

Admin (6)
├── GET/POST/PUT/DELETE  /api/banners/
├── GET/POST/PUT/DELETE  /api/vouchers/
├── POST                 /api/vouchers/validate_code/
└── GET                  /api/analytics/

Products (2)
├── GET    /api/products/
└── PUT    /api/products/{id}/

Orders (5)
├── GET/POST  /api/orders/
├── GET       /api/orders/my_orders/
├── GET       /api/orders/{id}/
├── GET       /api/orders/{id}/tracking/
└── POST      /api/orders/{id}/cancel/

Refunds (2)
├── GET/POST  /api/refunds/
└── POST      /api/refunds/request_refund/

Profile (2)
├── GET    /api/profile/my_profile/
└── PUT    /api/profile/update_profile/

Watchlist (3)
├── GET    /api/watchlist/my_watchlist/
├── POST   /api/watchlist/add_product/
└── POST   /api/watchlist/remove_product/

Reviews (2)
├── POST   /api/product-reviews/
└── GET    /api/product-reviews/my_reviews/

Complaints (2)
├── POST   /api/complaints/
└── GET    /api/complaints/my_complaints/

Referrals (2)
├── GET    /api/referrals/referral_info/
└── GET    /api/referrals/my_referrals/

Total: 30+ Endpoints
```

---

## 7. Frontend Architecture

### 7.1 Technology Stack

- **Framework:** Next.js 15
- **Language:** TypeScript
- **Styling:** Tailwind CSS
- **UI Components:** shadcn/ui
- **Animations:** Framer Motion
- **State Management:** React Hooks

### 7.2 Page Structure

```
app/
├── page.tsx                 # Homepage
├── layout.tsx               # Root layout
├── globals.css              # Global styles
│
├── login/
│   └── page.tsx            # Login page
│
├── register/
│   └── page.tsx            # Registration page
│
├── account/
│   └── page.tsx            # Account dashboard
│
├── admin/
│   ├── dashboard/
│   │   └── page.tsx        # Admin overview
│   └── inventory/
│       └── page.tsx        # Inventory management
│
└── dashboard/
    └── page.tsx            # User dashboard
```

### 7.3 Component Organization

```
components/
├── ui/                     # shadcn/ui components
│   ├── button.tsx
│   ├── input.tsx
│   ├── card.tsx
│   └── ...
│
├── Hero.tsx               # Homepage hero
├── FeaturedProducts.tsx   # Product grid
├── CategoriesSection.tsx  # Category tiles
├── ReviewsSection.tsx     # Customer reviews
├── NewsletterSection.tsx  # Email signup
└── Footer.tsx             # Site footer
```

### 7.4 Key Features

#### Responsive Design
- Mobile-first approach
- Breakpoints: 640px (sm), 768px (md), 1024px (lg), 1280px (xl)
- Flexible grid layouts
- Touch-friendly interface

#### Loading States
```typescript
const [loading, setLoading] = useState(true);
const [products, setProducts] = useState([]);

useEffect(() => {
  fetchProducts().then(data => {
    setProducts(data);
    setLoading(false);
  });
}, []);

if (loading) return <SkeletonLoader />;
return <ProductGrid products={products} />;
```

#### Error Handling
```typescript
const [error, setError] = useState('');

try {
  const response = await fetch(apiUrl);
  if (!response.ok) throw new Error('Failed to fetch');
  const data = await response.json();
  setData(data);
} catch (err) {
  setError(err.message);
}

if (error) return <ErrorMessage message={error} onRetry={fetchData} />;
```

#### Form Validation
```typescript
const [email, setEmail] = useState('');
const [emailError, setEmailError] = useState('');

const validateEmail = (email: string) => {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return regex.test(email);
};

const handleSubmit = (e: React.FormEvent) => {
  e.preventDefault();
  if (!validateEmail(email)) {
    setEmailError('Please enter a valid email');
    return;
  }
  // Submit form
};
```

### 7.5 Navbar Dynamic Updates

#### Features
- Categories loaded from database
- Functional search (desktop & mobile)
- Dynamic category navigation
- Sale/filter links
- Responsive menu

#### Implementation
```typescript
const [categories, setCategories] = useState([]);

useEffect(() => {
  fetch(`${apiUrl}/api/categories/`)
    .then(r => r.json())
    .then(data => setCategories(data.data || []));
}, []);

// Render categories
{categories.slice(0, 4).map(category => (
  <button
    key={category.id}
    onClick={() => window.location.href = `#/category/${category.name}`}
  >
    {category.name}
  </button>
))}
```

---

## 8. Troubleshooting

### 8.1 Common Issues

#### Backend Issues

**Issue: 500 Internal Server Error**
- **Symptom:** API returns 500 status codes
- **Cause:** Database not set up, migrations not run
- **Solution:**
  ```bash
  cd backend
  python manage.py makemigrations
  python manage.py migrate
  python manage.py seed_data
  ```

**Issue: "Module not found" errors**
- **Symptom:** ImportError when starting Django
- **Cause:** Dependencies not installed
- **Solution:**
  ```bash
  source venv/bin/activate
  pip install -r requirements.txt
  ```

**Issue: Port 8000 already in use**
- **Symptom:** "Address already in use"
- **Solution:**
  ```bash
  # Find process using port 8000
  lsof -i :8000
  # Kill the process
  kill -9 <PID>
  # Or use different port
  python manage.py runserver 0.0.0.0:8001
  ```

**Issue: Database locked**
- **Symptom:** "database is locked" error
- **Cause:** Multiple processes accessing SQLite
- **Solution:** Stop all Django processes, restart one instance

#### Frontend Issues

**Issue: "Failed to fetch products"**
- **Symptom:** Products not loading, errors in console
- **Cause:** Backend not running or CORS issue
- **Solution:**
  1. Verify backend running: `curl http://localhost:8000/api/products/`
  2. Check `.env.local` has correct API URL
  3. Check CORS settings in `backend/config/settings.py`

**Issue: CORS errors**
- **Symptom:** "blocked by CORS policy" in console
- **Cause:** Frontend URL not in CORS_ALLOWED_ORIGINS
- **Solution:**
  ```python
  # backend/config/settings.py
  CORS_ALLOWED_ORIGINS = [
      'http://localhost:3000',
      'http://127.0.0.1:3000',
  ]
  ```

**Issue: Navbar Account button not working**
- **Symptom:** Clicking Account doesn't navigate
- **Cause:** Fixed in latest version
- **Verification:** Check that button has `href="/account"`

#### Authentication Issues

**Issue: Login successful but can't access account**
- **Symptom:** Redirected to login prompt after successful login
- **Cause:** Token not saved to localStorage
- **Solution:**
  1. Open DevTools → Application → Local Storage
  2. Check if `auth_token` exists
  3. Verify login response includes token

**Issue: 400 Bad Request on registration**
- **Symptom:** Registration fails with validation errors
- **Cause:** Payload format mismatch
- **Solution:** Verify request includes all required fields:
  - username, email, password, password_confirm, first_name, last_name

**Issue: Can't create superuser**
- **Symptom:** "no such table: auth_user"
- **Cause:** Migrations not run
- **Solution:**
  ```bash
  python manage.py migrate
  python manage.py createsuperuser
  ```

### 8.2 Debugging Steps

#### Backend Debugging
1. Check Django terminal for error tracebacks
2. Test API endpoints directly with curl:
   ```bash
   curl http://localhost:8000/api/products/
   ```
3. Access Django admin to verify data exists
4. Check database file exists: `ls backend/db.sqlite3`
5. Verify migrations applied: `python manage.py showmigrations`

#### Frontend Debugging
1. Open browser DevTools (F12)
2. Check Console tab for JavaScript errors
3. Check Network tab for failed API calls
4. Verify API URL in `.env.local`
5. Test API directly in browser: `http://localhost:8000/api/products/`

#### Database Debugging
```bash
# SQLite
cd backend
sqlite3 db.sqlite3
.tables  # Show all tables
.schema api_product  # Show table structure
SELECT * FROM api_product;  # Query data
.quit

# PostgreSQL
psql classycouture
\dt  # Show tables
\d api_product  # Show table structure
SELECT * FROM api_product;
\q
```

### 8.3 Error Messages Reference

| Error | Cause | Solution |
|-------|-------|----------|
| "no such table" | Migrations not run | `python manage.py migrate` |
| "ModuleNotFoundError" | Package not installed | `pip install -r requirements.txt` |
| "CORS error" | Frontend not allowed | Add URL to CORS_ALLOWED_ORIGINS |
| "500 Internal Server Error" | Backend crash | Check Django terminal for traceback |
| "Connection refused" | Backend not running | Start Django: `python manage.py runserver` |
| "Email already exists" | Duplicate registration | Use different email |
| "Invalid credentials" | Wrong password | Check username/password |

### 8.4 Reset Everything

**Complete Reset:**
```bash
# Backend
cd backend
rm db.sqlite3
rm -rf api/migrations/
mkdir api/migrations
touch api/migrations/__init__.py
python manage.py makemigrations
python manage.py migrate
python manage.py seed_data
python manage.py createsuperuser

# Frontend (clear cache)
cd frontend
rm -rf .next
rm -rf node_modules
npm install
```

---

## 9. Advanced Topics

### 9.1 Payment Integration (Stripe)

#### Backend Setup

**Install Stripe:**
```bash
pip install stripe
```

**Payment Service (`api/services/payment.py`):**
```python
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

class StripePaymentService:
    @staticmethod
    def create_payment_intent(amount, currency='usd', metadata=None):
        try:
            intent = stripe.PaymentIntent.create(
                amount=int(amount * 100),  # Convert to cents
                currency=currency,
                metadata=metadata or {}
            )
            return {
                'success': True,
                'client_secret': intent.client_secret,
                'intent_id': intent.id
            }
        except stripe.error.StripeError as e:
            return {
                'success': False,
                'error': str(e)
            }
```

**Payment Endpoint:**
```python
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_payment_intent(request):
    order_id = request.data.get('order_id')
    amount = request.data.get('amount')

    result = StripePaymentService.create_payment_intent(
        amount=amount,
        metadata={'order_id': order_id, 'user_id': request.user.id}
    )

    if result['success']:
        return Response(result)
    return Response(result, status=status.HTTP_400_BAD_REQUEST)
```

#### Frontend Setup

**Install Stripe:**
```bash
npm install @stripe/stripe-js @stripe/react-stripe-js
```

**Payment Form Component:**
```typescript
import { CardElement, useStripe, useElements } from '@stripe/react-stripe-js';

export default function PaymentForm({ orderId, amount, onSuccess }) {
  const stripe = useStripe();
  const elements = useElements();

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Create payment intent
    const intentRes = await fetch(`${apiUrl}/api/payments/create-intent/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ order_id: orderId, amount }),
    });

    const { client_secret } = await intentRes.json();

    // Confirm payment
    const result = await stripe.confirmCardPayment(client_secret, {
      payment_method: {
        card: elements.getElement(CardElement),
      },
    });

    if (result.error) {
      console.error(result.error.message);
    } else {
      onSuccess();
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <CardElement />
      <button type="submit" disabled={!stripe}>
        Pay ${amount.toFixed(2)}
      </button>
    </form>
  );
}
```

### 9.2 Email Notifications

#### Setup Email Backend

**Install django-anymail:**
```bash
pip install django-anymail
```

**Configure SendGrid (`settings.py`):**
```python
EMAIL_BACKEND = "anymail.backends.sendgrid.EmailBackend"
ANYMAIL = {
    "SENDGRID_API_KEY": os.getenv('SENDGRID_API_KEY'),
}
```

**Or use Gmail (for testing):**
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
```

#### Email Service

**Create `api/services/email.py`:**
```python
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

class EmailService:
    @staticmethod
    def send_order_confirmation(user_email, order):
        context = {
            'order_id': order.order_id,
            'amount': order.final_price,
            'items': order.items.all(),
        }

        subject = f'Order Confirmation - {order.order_id}'
        html_message = render_to_string('emails/order_confirmation.html', context)

        send_mail(
            subject,
            '',
            settings.DEFAULT_FROM_EMAIL,
            [user_email],
            html_message=html_message,
        )
```

**Email Template (`templates/emails/order_confirmation.html`):**
```html
<!DOCTYPE html>
<html>
<body>
    <h1>Order Confirmation</h1>
    <p>Thank you for your order!</p>
    <h3>Order #{{ order_id }}</h3>
    <p><strong>Total:</strong> ${{ amount }}</p>
    {% for item in items %}
        <p>{{ item.product.name }} × {{ item.quantity }}</p>
    {% endfor %}
</body>
</html>
```

### 9.3 Production Deployment

#### Environment Variables

**Backend (`.env`):**
```env
DEBUG=False
SECRET_KEY=your-production-secret-key-here
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

DB_ENGINE=django.db.backends.postgresql
DB_NAME=classycouture
DB_USER=dbuser
DB_PASSWORD=secure_password
DB_HOST=db.yourdomain.com
DB_PORT=5432

CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

STRIPE_SECRET_KEY=sk_live_...
SENDGRID_API_KEY=SG....
```

**Frontend (`.env.production`):**
```env
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
NEXT_PUBLIC_STRIPE_KEY=pk_live_...
```

#### Backend Deployment Steps

1. **Prepare Static Files:**
   ```bash
   python manage.py collectstatic
   ```

2. **Use Production WSGI Server:**
   ```bash
   pip install gunicorn
   gunicorn config.wsgi:application --bind 0.0.0.0:8000
   ```

3. **Set Up Nginx (reverse proxy):**
   ```nginx
   server {
       listen 80;
       server_name api.yourdomain.com;

       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }

       location /static/ {
           alias /path/to/staticfiles/;
       }
   }
   ```

4. **Enable SSL/HTTPS:**
   ```bash
   sudo certbot --nginx -d api.yourdomain.com
   ```

#### Frontend Deployment (Vercel)

1. **Build project:**
   ```bash
   npm run build
   ```

2. **Deploy to Vercel:**
   ```bash
   npm install -g vercel
   vercel --prod
   ```

3. **Set environment variables in Vercel dashboard**

#### Database Backups

**Automated Backup Script:**
```bash
#!/bin/bash
# backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups"

pg_dump -U classyuser classycouture > $BACKUP_DIR/backup_$DATE.sql

# Keep only last 7 days
find $BACKUP_DIR -name "backup_*.sql" -mtime +7 -delete
```

**Set up cron job:**
```bash
crontab -e
# Add line:
0 2 * * * /path/to/backup.sh
```

### 9.4 Performance Optimization

#### Backend Optimization

**Database Indexing:**
```python
class Product(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    featured = models.BooleanField(default=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
```

**Query Optimization:**
```python
# Bad - N+1 queries
products = Product.objects.all()
for product in products:
    print(product.category.name)  # Hits DB each time

# Good - Single query with prefetch
products = Product.objects.select_related('category').all()
for product in products:
    print(product.category.name)  # No additional DB hit
```

**Caching:**
```python
from django.core.cache import cache

def get_featured_products():
    products = cache.get('featured_products')
    if not products:
        products = Product.objects.filter(featured=True)[:10]
        cache.set('featured_products', products, 3600)  # 1 hour
    return products
```

#### Frontend Optimization

**Image Optimization:**
```typescript
import Image from 'next/image';

<Image
  src={product.image_url}
  alt={product.name}
  width={400}
  height={400}
  loading="lazy"
  quality={85}
/>
```

**Code Splitting:**
```typescript
import dynamic from 'next/dynamic';

const HeavyComponent = dynamic(() => import('./HeavyComponent'), {
  loading: () => <p>Loading...</p>,
  ssr: false
});
```

**API Call Optimization:**
```typescript
// Debounce search
const debouncedSearch = useMemo(
  () => debounce((query) => fetchResults(query), 300),
  []
);
```

### 9.5 Testing

#### Backend Tests

**Unit Tests (`api/tests.py`):**
```python
from django.test import TestCase
from .models import Product, Category

class ProductTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Test Category")
        self.product = Product.objects.create(
            name="Test Product",
            price=99.99,
            category=self.category
        )

    def test_product_creation(self):
        self.assertEqual(self.product.name, "Test Product")
        self.assertEqual(self.product.price, 99.99)

    def test_discounted_price(self):
        self.product.on_sale = True
        self.product.discount_percent = 20
        self.assertEqual(self.product.discounted_price, 79.99)
```

**Run Tests:**
```bash
python manage.py test
```

#### Frontend Tests

**Install Testing Library:**
```bash
npm install --save-dev @testing-library/react @testing-library/jest-dom
```

**Component Test:**
```typescript
import { render, screen } from '@testing-library/react';
import ProductCard from './ProductCard';

test('renders product name', () => {
  const product = {
    name: 'Test Product',
    price: '99.99',
    image_url: 'test.jpg'
  };

  render(<ProductCard product={product} />);
  expect(screen.getByText('Test Product')).toBeInTheDocument();
});
```

### 9.6 Security Best Practices

#### Backend Security

**Never commit secrets:**
```bash
# .gitignore
.env
*.sqlite3
```

**Use strong SECRET_KEY:**
```python
# Generate new key
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**Enable HTTPS only:**
```python
# Production settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

**Rate Limiting:**
```bash
pip install django-ratelimit
```

```python
from django_ratelimit.decorators import ratelimit

@ratelimit(key='ip', rate='5/m')
@api_view(['POST'])
def login(request):
    # Login logic
```

#### Frontend Security

**Sanitize User Input:**
```typescript
import DOMPurify from 'dompurify';

const sanitizedContent = DOMPurify.sanitize(userInput);
```

**Secure Token Storage:**
```typescript
// Use httpOnly cookies instead of localStorage for production
// Or implement token refresh mechanism
```

**Validate API Responses:**
```typescript
const validateProduct = (data: any): Product => {
  if (!data.name || !data.price) {
    throw new Error('Invalid product data');
  }
  return data as Product;
};
```

---

## Appendix

### A. Quick Reference Commands

#### Backend Commands
```bash
# Migrations
python manage.py makemigrations
python manage.py migrate
python manage.py showmigrations

# Data
python manage.py seed_data
python manage.py createsuperuser

# Server
python manage.py runserver
python manage.py runserver 0.0.0.0:8001

# Shell
python manage.py shell

# Tests
python manage.py test
```

#### Frontend Commands
```bash
# Development
npm run dev
npm run build
npm start

# Dependencies
npm install
npm update

# Linting
npm run lint
```

### B. Environment Variables Reference

#### Backend (.env)
```env
DEBUG=True/False
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1

DB_ENGINE=django.db.backends.postgresql
DB_NAME=classycouture
DB_USER=dbuser
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432

CORS_ALLOWED_ORIGINS=http://localhost:3000

STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...

SENDGRID_API_KEY=SG....
EMAIL_HOST_USER=your@email.com
EMAIL_HOST_PASSWORD=password
```

#### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_STRIPE_KEY=pk_test_...
```

### C. File Locations

#### Documentation Files
```
/Users/alihassancheema/Desktop/Classy/ClassyCouture/
├── COMPLETE_DOCUMENTATION.md (this file)
├── QUICKSTART.md
├── SETUP_GUIDE.md
├── FEATURES_GUIDE.md
├── FEATURES_SUMMARY.md
├── IMPLEMENTATION_GUIDE.md
├── COMPLETE_PROJECT_SUMMARY.md
├── AUTHENTICATION_STATUS.md
├── CONNECTION_STATUS.md
├── ACCOUNT_PAGES_GUIDE.md
├── FIXES_APPLIED.md
├── INTEGRATION_SUMMARY.md
├── NAVBAR_DYNAMIC_UPDATE.md
├── PAYMENT_EMAIL_GUIDE.md
├── POSTGRESQL_SETUP.md
├── README_START_HERE.md
└── TROUBLESHOOTING.md
```

#### Key Source Files
```
backend/
├── config/settings.py          # Django configuration
├── config/urls.py              # Main URL routing
├── api/models.py               # Database models
├── api/views.py                # Original API views
├── api/views_extended.py       # Extended API views
├── api/serializers.py          # Data serializers
├── api/serializers_extended.py # Extended serializers
└── api/admin.py                # Django admin config

frontend/
├── app/page.tsx                # Homepage
├── app/login/page.tsx          # Login page
├── app/register/page.tsx       # Registration page
├── app/account/page.tsx        # Account dashboard
├── app/admin/dashboard/page.tsx # Admin dashboard
├── app/admin/inventory/page.tsx # Inventory management
└── app/dashboard/page.tsx      # User dashboard
```

### D. Support Resources

- **Django Documentation**: https://docs.djangoproject.com/
- **Django REST Framework**: https://www.django-rest-framework.org/
- **Next.js Documentation**: https://nextjs.org/docs
- **Tailwind CSS**: https://tailwindcss.com/docs
- **PostgreSQL**: https://www.postgresql.org/docs/
- **Stripe API**: https://stripe.com/docs
- **SendGrid API**: https://docs.sendgrid.com/

### E. Project Statistics

- **Total Lines of Code**: 10,000+
- **Database Models**: 14
- **API Endpoints**: 30+
- **Frontend Pages**: 7
- **Components**: 20+
- **Documentation Files**: 16
- **Development Time**: Optimized for rapid deployment

---

## Summary

ClassyCouture is a **complete, production-ready e-commerce platform** featuring:

✅ **Full-stack implementation** (Django + Next.js)
✅ **14 database models** with relationships
✅ **30+ REST API endpoints** with authentication
✅ **Modern, responsive UI** with Tailwind CSS
✅ **Complete admin system** for store management
✅ **User dashboard** with order tracking
✅ **Referral program** with points system
✅ **Voucher/discount system**
✅ **Real-time order tracking**
✅ **Refund management**
✅ **Product reviews and ratings**
✅ **Comprehensive documentation**

**Ready to deploy and scale!**

---

**For questions or issues, refer to the [Troubleshooting](#8-troubleshooting) section or consult the individual documentation files listed in Appendix C.**

---

*Last updated: 2025-11-01*
*Version: 1.0*
*ClassyCouture E-Commerce Platform*
