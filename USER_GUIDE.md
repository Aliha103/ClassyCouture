# ClassyCouture - Complete User Guide

**Version:** 2.0
**Last Updated:** January 2025
**Platform:** Full-stack E-commerce Application

---

## Table of Contents

1. [Introduction](#introduction)
2. [Quick Start](#quick-start)
3. [System Architecture](#system-architecture)
4. [User Roles & Access](#user-roles--access)
5. [Admin Dashboard Guide](#admin-dashboard-guide)
6. [Customer Features](#customer-features)
7. [API Documentation](#api-documentation)
8. [Database Models](#database-models)
9. [Common Tasks](#common-tasks)
10. [Troubleshooting](#troubleshooting)

---

## Introduction

ClassyCouture is a production-ready e-commerce platform built with:
- **Backend:** Django 5.1.4 + Django REST Framework
- **Frontend:** Next.js 14.2.5 + React 18 + TypeScript
- **Database:** PostgreSQL
- **Styling:** Tailwind CSS v3.4.18

### Key Features
- User authentication & authorization
- Product catalog with categories & collections
- Shopping cart & wishlist
- Order management & tracking
- Advanced analytics dashboard
- Voucher & discount system
- Returns & refunds management
- Referral program
- Review & complaint system

---

## Quick Start

### Prerequisites
- Python 3.9+ with Anaconda
- Node.js 18+ and npm
- PostgreSQL 12+

### Backend Setup

```bash
# Navigate to backend directory
cd ClassyCouture/backend

# Install dependencies (using Anaconda Python)
/Users/alihassancheema/opt/anaconda3/bin/pip install -r requirements.txt

# Configure database in backend/config/settings.py
# Update DATABASES section with your PostgreSQL credentials

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Start development server
uvicorn config.asgi:application --host 127.0.0.1 --port 8000 --reload
```

### Frontend Setup

```bash
# Navigate to frontend directory
cd ClassyCouture/frontend

# Install dependencies
npm install

# Create environment file
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

# Start development server
npm run dev
```

### Access Points
- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000/api/
- **Django Admin:** http://localhost:8000/admin/
- **Admin Dashboard:** http://localhost:3000/admin-dashboard

---

## System Architecture

### Backend Structure
```
backend/
├── api/
│   ├── models.py           # 14 database models
│   ├── views.py            # Core API views
│   ├── views_extended.py   # Admin & extended features
│   ├── serializers.py      # Core serializers
│   ├── serializers_extended.py  # Extended serializers
│   ├── urls.py             # API routing
│   ├── admin.py            # Django admin config
│   └── signals.py          # Auto-profile creation
├── config/
│   ├── settings.py         # Django settings
│   ├── urls.py             # Root URL config
│   └── asgi.py             # ASGI application
└── requirements.txt        # Python dependencies
```

### Frontend Structure
```
frontend/
├── app/
│   ├── admin-dashboard/    # Admin interface
│   ├── auth/               # Login & register
│   ├── shop/               # Product browsing
│   └── page.tsx            # Homepage
├── components/
│   ├── admin/              # Admin components
│   │   ├── AdvancedAnalytics.tsx
│   │   ├── CollectionsManager.tsx
│   │   └── CollectionForm.tsx
│   ├── ui/                 # Reusable UI components
│   └── Navbar.tsx          # Navigation
└── public/                 # Static assets
```

---

## User Roles & Access

### 1. Regular Users
**Access:** Public pages + User dashboard
**Features:**
- Browse products & collections
- Add items to cart & wishlist
- Place orders
- Track order status
- Write reviews
- File complaints
- Use voucher codes
- Earn referral points

### 2. Staff/Admin Users
**Access:** Everything + Admin dashboard
**Features:**
- All regular user features
- Access admin dashboard at `/admin-dashboard`
- Manage products, categories, collections
- View analytics & reports
- Process orders & refunds
- Create vouchers & promotions
- Manage users
- View sales data

### 3. Superuser
**Access:** Everything + Django Admin
**Features:**
- All staff features
- Full database access via Django Admin
- Create/modify staff users
- System configuration

---

## Admin Dashboard Guide

### Accessing the Dashboard

1. **Login as staff user**
   ```
   URL: http://localhost:3000/auth/login
   Ensure user has is_staff=True in Django admin
   ```

2. **Navigate to admin dashboard**
   ```
   URL: http://localhost:3000/admin-dashboard
   ```

3. **Verification**
   - Dashboard checks localStorage for user_data
   - Requires is_staff, is_superuser, or is_admin flag
   - Shows "Access Denied" for non-staff users

---

### Tab 1: Overview

**Purpose:** Main dashboard with real-time business metrics

#### Header Controls
- **Date Range Selector:** Today | Last 7 Days | Last 30 Days | This Year
- **Quick Actions:**
  - Back to Home
  - Open Django Admin
  - Export Data

#### Quick Metrics Bar
| Metric | Description |
|--------|-------------|
| Active Now | Current active users (127) |
| Avg Order Value | Average transaction amount ($68.15) |
| Conversion Rate | Purchase conversion percentage (3.24%) |
| Returning Customers | Repeat customer rate (42%) |

#### Main Statistics Cards

**1. Total Revenue**
- Amount: $125,847.50
- Change: +32.4%
- Icon: Dollar sign (green)
- Shows: Trending up

**2. Total Orders**
- Count: 1,847 orders
- Change: +18.7%
- Icon: Shopping bag (blue)
- Shows: Growth trend

**3. Total Products**
- Count: 342 products
- Change: +8.2%
- Icon: Package (purple)
- Shows: Inventory growth

**4. Total Users**
- Count: 8,934 users
- Change: +24.1%
- Icon: Users (orange)
- Shows: User base growth

#### Revenue Overview Chart
- **Type:** Horizontal bar chart
- **Time Period:** Last 7 days (Mon-Sun)
- **Data Shown:**
  - Daily revenue amount
  - Number of orders per day
  - Visual comparison across week
- **Total Weekly Revenue:** $115,847

#### Live Activity Feed
Real-time updates showing:
- Recent orders placed
- High-value sales alerts
- New user registrations
- Payment confirmations
- System alerts

**Example Activities:**
```
New order #8392 from Sarah M. - $245.00
Large sale alert: Order #8391 - $1,299.00
New user registered: Alex Thompson
Payment received: Order #8389 - $145.50
```

#### Payment Methods Distribution
Visual breakdown of payment preferences:
- **Credit Card:** 52% ($65,441)
- **PayPal:** 28% ($35,237)
- **Debit Card:** 15% ($18,877)
- **Other:** 5% ($6,292)

#### Traffic Sources
Where customers are coming from:
- **Direct:** 3,456 visitors (38%)
- **Google:** 2,891 visitors (32%)
- **Social Media:** 1,823 visitors (20%)
- **Email:** 910 visitors (10%)

#### Device Breakdown
Customer device usage:
- **Mobile:** 58%
- **Desktop:** 32%
- **Tablet:** 10%

#### Recent Orders Section
Shows 5 most recent orders with:
- Order ID & timestamp
- Customer name
- Order amount
- Payment method
- Current status

**Order Tracking Steps:**
1. Order Placed ✓
2. Payment Confirmed ✓
3. Shipped 🚚
4. Delivered 📦

**Additional Info:**
- Tracking number
- Shipping address
- Estimated delivery
- Status badges (color-coded)

#### Top Products Section
Top 5 best-selling products showing:
- Product name
- Units sold
- Total revenue
- Current stock level
- Trend indicator (↑/↓)
- Low stock alerts

---

### Tab 2: Analytics

**Purpose:** Advanced business intelligence and metrics

#### Time Range Filters
Select data period:
- 7 Days
- 30 Days
- 90 Days
- 1 Year

*All charts and metrics update based on selected range*

#### Key Metrics Grid

**1. Total Revenue Card**
- Display: Large dollar amount
- Growth percentage vs previous period
- Trend indicator (↑ up / ↓ down)
- Icon: Dollar sign (green background)
- Time context: "Last X days"

**2. Total Orders Card**
- Display: Order count
- Average order value calculation
- Icon: Shopping bag (blue background)
- Shows: "Avg: $XX.XX per order"

**3. Items Sold Card**
- Display: Total items count
- Context: "Across all orders"
- Icon: Package (purple background)

**4. Unique Customers Card**
- Display: Customer count
- Label: "Active customers"
- Icon: Users (orange background)

#### Revenue Trend Chart

**Features:**
- Custom bar chart visualization
- Responsive height based on max revenue
- Hover tooltips showing exact amounts
- Date labels (for ≤31 days)
- Gradient colors (gray scale)

**Calculations:**
- Normalizes bars to max revenue
- Minimum height: 4px for visibility
- Interactive hover effects

**Data Source:** `/api/analytics/`

#### Top Performing Products

**Display Format:**
```
Rank | Product Name      | Category        | Revenue    | Units
#1   | Product Name      | Category Name   | $X,XXX     | XXX sold
#2   | Product Name      | Category Name   | $X,XXX     | XXX sold
```

**Features:**
- Top 5 products by revenue
- Sortable rankings
- Category information
- Sales metrics
- Revenue calculations

**Data Source:** `/api/products/` with sales data

#### Performance Metrics Panel

**Average Order Value**
- Formula: Total Revenue / Total Orders
- Display: $XX.XX
- Icon: Dollar sign (blue)

**Total Profit**
- Aggregated from all orders
- Display: $XX,XXX
- Icon: Trending up (green)

**Profit Margin**
- Formula: (Total Profit / Total Revenue) × 100
- Display: XX.X%
- Icon: Bar chart (purple)

#### Export Analytics Report

**Functionality:**
- CSV export button
- Downloads complete analytics data
- Includes all metrics from selected time range
- Button: "Export CSV" with download icon

---

### Tab 3: Categories & Collections

**Purpose:** Manage hierarchical product organization

#### Header Section
- **Title:** Categories & Collections
- **Description:** "Organize your catalog with hierarchical categories and curated collections"
- **Action Button:** "+ Create Collection"

#### Search & Filter
```
[🔍 Search categories...]
```
- Real-time search filtering
- Searches: name, description
- Updates tree view instantly

#### Collections Tree View

**Structure:**
```
📁 Top-Level Collection 1
   └─ 📦 Sub-Collection 1.1
   └─ 📦 Sub-Collection 1.2
📁 Top-Level Collection 2
   └─ 📦 Sub-Collection 2.1
      └─ 📦 Sub-Sub-Collection 2.1.1
```

**Display Elements:**
- **Icons:**
  - 📁 Folder icon for parent collections
  - 📦 Package icon for leaf categories
- **Badges:**
  - "Collection" badge for top-level
  - Product count badge (e.g., "42 products")
- **Image Thumbnails:** 32×32px preview
- **Indentation:** Visual hierarchy with padding

**Per-Item Information:**
- Category/Collection name
- Short description (truncated)
- Product count
- Is collection indicator
- Display order

**Action Buttons (per item):**
1. **Add Sub-Collection** (📁+)
   - Opens form with parent pre-selected
   - Creates child category

2. **Edit** (✏️)
   - Opens form in edit mode
   - Loads existing data

3. **Delete** (🗑️)
   - Shows confirmation dialog
   - Warning for recursive delete
   - Deletes category and all children

#### Collection Form Modal

**Triggered By:**
- Create Collection button (new)
- Add Sub-Collection button (child)
- Edit button (modify)

**Form Fields:**

**1. Collection Name** (required)
```
[                              ]
Input: "e.g., Summer Collection 2025"
Help: The name of your collection or category
```

**2. Description** (optional)
```
[                              ]
[                              ]
[                              ]
Textarea: Multi-line description
Help: Optional description for your collection
```

**3. Image URL** (required)
```
[https://example.com/image.jpg]
Preview: [Shows 128×128px thumbnail]
Help: URL to the collection's cover image
Auto-validation: Shows placeholder on error
```

**4. Parent Collection** (conditional)
```
[None (Top-Level Collection)  ▼]
Dropdown options:
- None (Top-Level Collection)
- Collection 1
- Collection 2
- etc.

Help: Choose a parent collection to create a sub-collection
Only shown: When creating new (not editing, not from Add Sub)
```

**5. Display Order** (number)
```
[0                             ]
Input: Number field, min=0
Help: Lower numbers appear first (0 = highest priority)
Default: 0
```

**6. Mark as Top-Level Collection** (checkbox)
```
☐ Mark as Top-Level Collection
Only shown: When no parent selected
Auto-checked: When parent is null
```

**Form Actions:**
- **Primary Button:** "Create Collection" or "Update Collection"
  - Loading state: "Saving..."
  - Disabled during save

- **Secondary Button:** "Cancel"
  - Closes modal
  - Resets form

**Form Behavior:**
- **Create Mode:** Empty form, all fields editable
- **Edit Mode:** Pre-filled with existing data
- **Sub-Collection Mode:** Parent pre-selected, locked
- **Auto-slug:** Generated from name on save
- **Validation:** Client-side + server-side

**API Endpoints:**
- Create: `POST /api/categories/`
- Update: `PUT /api/categories/{id}/`
- Delete: `DELETE /api/categories/{id}/`
- List: `GET /api/categories/`
- Filter: `GET /api/categories/?collections_only=true`

#### Footer Summary
```
Total Collections: XX
[🔄 Refresh]
```

---

### Tab 4: Products

**Purpose:** Product inventory management (partial implementation)

#### Current Features

**Search Bar:**
```
[🔍 Search products...]
```

**Filter Dropdown:**
```
[All Products          ▼]
Options:
- All Products
- New Arrivals
- Featured
- On Sale
- Low Stock
```

**Action Buttons:**
- **Export** - Download product data
- **+ Add Product** - Create new product

#### Status
```
⚙️ Product management interface with real-time updates coming soon.
For now, manage products through Django Admin.

[Open Django Admin] → /admin/api/product/
```

**Planned Features:**
- Full CRUD interface
- Bulk edit capabilities
- Image upload
- Inventory tracking
- Price management
- Category assignment

---

### Tab 5: Orders

**Purpose:** Order fulfillment and management (partial implementation)

#### Current Features

**Action Button:**
- **+ Add New** - Manual order entry

#### Status
```
📦 Full CRUD interface coming soon.
Manage orders through Django Admin for now.

[Open Django Admin] → /admin/api/orders/
```

**Planned Features:**
- Order listing with filters
- Status updates
- Order details view
- Shipping label generation
- Customer communication
- Bulk actions

---

### Tab 6: Returns

**Purpose:** Complete returns and refunds management system

#### Returns Statistics Panel

**Four Key Metrics:**

**1. Total Returns**
```
Icon: ↩️ (Rotate CCW - orange)
Value: 5
Label: Returns this period
```

**2. Pending Returns**
```
Icon: ⏰ (Clock - yellow)
Value: 2
Label: Awaiting action
```

**3. Total Refunded**
```
Icon: 💵 (Dollar - green)
Value: $740.75
Label: Amount refunded
```

**4. Items Returned**
```
Icon: 📦 (Package - blue)
Value: 9
Label: Total items
```

#### Returns List

**Each Return Card Shows:**

**Header Section:**
```
Return ID: RET-XXXX          Status: [Badge]
Order ID: ORD-XXXXXXXXXX     Payment: [Badge]
Customer: John Doe
Amount: $XXX.XX
Requested: Jan XX, 2025 XX:XX AM
```

**Status Badges:**
- **Requested** (blue) - Initial state
- **Processing** (yellow) - Under review
- **Approved** (green) - Accepted
- **Rejected** (red) - Denied
- **Completed** (gray) - Finished

**Payment Status:**
- **Pending Refund** (yellow)
- **Processing** (blue)
- **Refunded** (green)
- **Not Refunded** (gray)

**Items Section:**
```
Items: Product 1, Product 2, Product 3 (3 items)
Reason: [Reason for return]
```

**Common Reasons:**
- Size too large/small
- Wrong color/style
- Quality issues
- Damaged in shipping
- Changed mind
- Item not as described

**Tracking Information:**
```
📦 Tracking: TRACK123456789
Current Status: In Transit / Delivered
Location: Distribution Center, City, ST
Product Received: Yes/No
ETA: Jan XX, 2025
```

**Action Buttons:**

**For "Requested" Status:**
```
[✓ Approve]  [✗ Reject]  [👁️ View Details]  [📍 Track]
```

**For "Processing" Status:**
```
[✓ Complete]  [👁️ View Details]  [📍 Track]
```

**For Other Statuses:**
```
[👁️ View Details]  [📍 Track]
```

#### Sample Return Scenarios

**Return 1: Standard Return**
```
ID: RET-2891
Order: ORD-9801234567
Customer: John Doe
Amount: $89.99
Status: Requested → Needs approval
Payment: Pending Refund
Items: Classic White Sneakers (1 item)
Reason: Size too large
Actions: Approve/Reject available
```

**Return 2: In Transit**
```
ID: RET-2890
Customer: Jane Smith
Amount: $149.50
Status: Processing → Returning to warehouse
Payment: Processing
Tracking: TRACK123456789
Location: Distribution Center, Austin, TX
ETA: Jan 20, 2025
Items: 2 items
Reason: Wrong color
Actions: Complete when received
```

**Return 3: Completed**
```
ID: RET-2889
Customer: Bob Wilson
Amount: $299.99
Status: Completed ✓
Payment: Refunded ✓
Items: Premium Leather Jacket
Received: Yes
Refund Date: Jan 15, 2025
Actions: View only
```

---

### Tab 7: Users

**Purpose:** Customer management (partial implementation)

#### Current Features

**Action Button:**
- **+ Add New** - Create user account

#### Status
```
👥 Full CRUD interface coming soon.
Manage users through Django Admin for now.

[Open Django Admin] → /admin/auth/user/
```

**Planned Features:**
- User listing with search
- Profile management
- Role assignment
- Activity history
- Order history per user
- Communication tools

---

### Tab 8: Payments

**Purpose:** Payment gateway configuration and monitoring

#### Payment Gateway Cards

**Gateway 1: Stripe**
```
[Stripe Logo]
Stripe
Status: ● Active
$89,234 this month
[Configure]
```

**Gateway 2: PayPal**
```
[PayPal Logo]
PayPal
Status: ● Active
$35,237 this month
[Configure]
```

**Gateway 3: Square**
```
[Square Logo]
Square
Status: ○ Inactive
$0 this month
[Configure]
```

#### Features
- Gateway status monitoring
- Monthly transaction totals
- Quick toggle active/inactive
- Configuration access

#### Action Button
```
[+ Add Payment Gateway]
```

#### Status Note
```
💳 Full transaction management interface coming soon.

[Open Django Admin] → /admin/api/payments/
```

**Planned Features:**
- Transaction history
- Refund processing
- Gateway analytics
- Fee tracking
- Settlement reports

---

### Tab 9: Promotions

**Purpose:** Marketing and discount management (partial implementation)

#### Current Features

**Action Button:**
- **+ Add New** - Create promotion

#### Status
```
🎁 Full CRUD interface coming soon.
Manage promotions through Django Admin for now.

[Open Django Admin] → /admin/api/voucher/
```

**Planned Features:**
- Voucher creation wizard
- Promotion calendar
- Usage analytics
- A/B testing
- Automatic expiration
- Customer targeting

---

## Customer Features

### 1. Browse Products

**Accessing Products:**
```
Home → Shop → Categories → Products
```

**Product Cards Show:**
- Product image
- Name and price
- Rating (1-5 stars)
- Review count
- Sale badge (if discounted)
- Discounted price
- Stock status

**Filtering Options:**
- By category
- By collection
- Price range
- Rating
- Availability

**Sorting Options:**
- Price: Low to High
- Price: High to Low
- Newest First
- Best Rated
- Most Popular

### 2. Shopping Cart

**Add to Cart:**
```javascript
// Frontend automatically calls:
// Add item logic (localStorage or API)
```

**Cart Features:**
- Quantity adjustment
- Remove items
- Save for later
- Apply voucher code
- See subtotal and total
- Shipping calculation

### 3. Wishlist

**Add to Wishlist:**
- Click heart icon on product
- Saves to user's watchlist
- Access from navbar or user dashboard

**Wishlist Management:**
- View all saved items
- Move to cart
- Remove items
- Share wishlist

**API Endpoint:**
```
GET /api/watchlist/{user_id}/
POST /api/watchlist/{user_id}/add_product/
DELETE /api/watchlist/{user_id}/remove_product/
```

### 4. Place Order

**Checkout Process:**

**Step 1: Cart Review**
- Review all items
- Update quantities
- Apply voucher

**Step 2: Shipping Information**
```json
{
  "address": "123 Main St",
  "city": "New York",
  "postal_code": "10001",
  "country": "USA",
  "phone": "+1234567890"
}
```

**Step 3: Payment Method**
- Credit/Debit Card
- PayPal
- Other gateways

**Step 4: Order Confirmation**
- Order ID generated
- Email confirmation
- Order tracking link

**API Endpoint:**
```
POST /api/orders/
Request body:
{
  "items": [
    {"product_id": 1, "quantity": 2},
    {"product_id": 5, "quantity": 1}
  ],
  "shipping_address": "...",
  "phone": "...",
  "payment_method": "credit_card",
  "voucher_code": "SUMMER50"
}
```

### 5. Track Orders

**Access Order Tracking:**
```
Dashboard → My Orders → [Order ID] → Track
```

**Tracking Stages:**
1. **Order Placed** ✓
   - Timestamp shown
   - Order confirmed

2. **Payment Confirmed** ✓
   - Payment processed
   - Order in queue

3. **Shipped** 🚚
   - Tracking number provided
   - Carrier information
   - Estimated delivery

4. **Delivered** 📦
   - Delivery confirmation
   - Signature (if required)

**API Endpoint:**
```
GET /api/orders/{order_id}/tracking/
```

### 6. Reviews

**Write a Review:**

**Requirements:**
- Must have purchased product
- Rating: 1-5 stars
- Review text (optional)

**Form Fields:**
```
Name: [Auto-filled from profile]
Email: [Auto-filled from profile]
Rating: ⭐⭐⭐⭐⭐
Review: [Text area]
```

**API Endpoint:**
```
POST /api/reviews/
{
  "product_id": 123,
  "customer_name": "John Doe",
  "email": "john@example.com",
  "rating": 5,
  "review_text": "Great product!"
}
```

### 7. Complaints

**File a Complaint:**

**Access:**
```
Dashboard → My Orders → [Order] → File Complaint
```

**Form Fields:**
```
Order Item: [Dropdown of order items]
Title: [Brief description]
Description: [Detailed explanation]
```

**Complaint Statuses:**
- **Open** (blue) - Just filed
- **In Progress** (yellow) - Being reviewed
- **Resolved** (green) - Issue fixed
- **Closed** (gray) - Completed

**API Endpoint:**
```
POST /api/complaints/
{
  "order_item_id": 456,
  "title": "Item damaged",
  "description": "The product arrived with scratches..."
}
```

### 8. Referral System

**How It Works:**

**Step 1: Get Your Referral Code**
```
Dashboard → Referral Program → Your Code
Example: REFJOHN1DO
```

**Step 2: Share Code**
- Share with friends
- Via social media
- Direct link with code

**Step 3: Earn Points**
- Friend registers with code
- Friend makes first purchase
- You earn referral points

**Points Usage:**
- 100 points = $10 discount
- 500 points = $60 discount
- Custom redemption rates

**API Endpoints:**
```
GET /api/profile/{user_id}/
Response includes:
{
  "referral_code": "REFJOHN1DO",
  "referral_points": 500,
  "total_referrals": 5
}

POST /api/auth/register/
{
  "username": "newuser",
  "email": "new@example.com",
  "password": "...",
  "referred_by": "REFJOHN1DO"
}
```

### 9. Voucher Codes

**Apply Voucher:**

**At Checkout:**
```
[Enter voucher code...]  [Apply]
```

**Validation:**
- Checks if code exists
- Verifies not expired
- Checks minimum purchase
- Confirms max uses not reached

**API Endpoint:**
```
POST /api/vouchers/validate_code/
{
  "code": "SUMMER50"
}

Response:
{
  "valid": true,
  "voucher": {
    "code": "SUMMER50",
    "discount_type": "percentage",
    "discount_value": 50,
    "min_purchase": 100.00
  }
}
```

**Discount Types:**
- **Percentage:** X% off total
- **Fixed Amount:** $X off total

**Example Calculation:**
```
Cart Total: $200.00
Voucher: SUMMER50 (50% off)
Minimum: $100.00 ✓
Discount: -$100.00
Final Total: $100.00
```

---

## API Documentation

### Base URL
```
http://localhost:8000/api/
```

### Authentication

**Register User**
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

Response: 201 Created
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

**Login**
```http
POST /api/auth/login/
Content-Type: application/json

{
  "username": "johndoe",
  "password": "securepass123"
}

Response: 200 OK
{
  "success": true,
  "message": "Login successful",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe"
  },
  "profile": {
    "phone": "",
    "address": "",
    "city": "",
    "country": "",
    "referral_code": "REFJOHN1DO",
    "referral_points": 0,
    "total_referrals": 0,
    "is_admin": false
  }
}
```

### Products

**List Products**
```http
GET /api/products/
GET /api/products/?featured=true
GET /api/products/?new_arrivals=true
GET /api/products/?limit=8

Response: 200 OK
{
  "data": [
    {
      "id": 1,
      "name": "Classic Black Blazer",
      "description": "Elegant black blazer...",
      "price": "129.99",
      "discounted_price": 103.99,
      "image_url": "https://...",
      "rating": 4.5,
      "review_count": 23,
      "featured": true,
      "new_arrival": false,
      "inventory": 50,
      "sku": "BLZ-001",
      "on_sale": true,
      "discount_percent": 20,
      "is_in_stock": true,
      "category_name": "Blazers"
    }
  ]
}
```

**Get Single Product**
```http
GET /api/products/{id}/

Response: 200 OK
{
  "data": { /* product object */ }
}
```

### Categories

**List Categories**
```http
GET /api/categories/
GET /api/categories/?collections_only=true
GET /api/categories/?parent={id}
GET /api/categories/?top_level=true

Response: 200 OK
{
  "data": [
    {
      "id": 1,
      "name": "Summer Collection",
      "slug": "summer-collection",
      "description": "Latest summer styles",
      "image_url": "https://...",
      "parent": null,
      "parent_name": null,
      "is_collection": true,
      "display_order": 0,
      "subcategories": [
        {
          "id": 2,
          "name": "Beach Wear",
          "slug": "beach-wear",
          "parent": 1,
          /* ... */
        }
      ],
      "product_count": 42
    }
  ]
}
```

**Create Category**
```http
POST /api/categories/
Content-Type: application/json

{
  "name": "Winter Collection",
  "description": "Cozy winter essentials",
  "image_url": "https://...",
  "parent": null,
  "is_collection": true,
  "display_order": 0
}

Response: 201 Created
```

**Update Category**
```http
PUT /api/categories/{id}/
Content-Type: application/json

{
  "name": "Winter Collection 2025",
  "display_order": 1
}

Response: 200 OK
```

**Delete Category**
```http
DELETE /api/categories/{id}/

Response: 204 No Content
```

### Analytics

**Get Sales Analytics**
```http
GET /api/analytics/

Response: 200 OK
{
  "data": [
    {
      "id": 1,
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

### Orders

**Create Order**
```http
POST /api/orders/
Content-Type: application/json

{
  "items": [
    {
      "product_id": 1,
      "quantity": 2
    },
    {
      "product_id": 5,
      "quantity": 1
    }
  ],
  "shipping_address": "123 Main St, New York, NY 10001",
  "phone": "+1234567890",
  "payment_method": "credit_card",
  "voucher_code": "SUMMER50"
}

Response: 201 Created
{
  "order_id": "ORD-A1B2C3D4E5",
  "total_price": "259.98",
  "discount_amount": "50.00",
  "final_price": "209.98",
  "status": "pending"
}
```

**Get Order**
```http
GET /api/orders/{order_id}/

Response: 200 OK
{
  "order_id": "ORD-A1B2C3D4E5",
  "user": 1,
  "total_price": "259.98",
  "discount_amount": "50.00",
  "final_price": "209.98",
  "status": "shipped",
  "items": [
    {
      "product": {
        "name": "Classic Black Blazer",
        "image_url": "https://..."
      },
      "quantity": 2,
      "price_at_purchase": "129.99",
      "total": "259.98"
    }
  ],
  "tracking": {
    "tracking_number": "TRACK123456",
    "carrier": "UPS",
    "current_location": "Distribution Center",
    "estimated_delivery": "2025-01-20T12:00:00Z"
  }
}
```

### Vouchers

**Validate Voucher**
```http
POST /api/vouchers/validate_code/
Content-Type: application/json

{
  "code": "SUMMER50"
}

Response: 200 OK
{
  "valid": true,
  "voucher": {
    "code": "SUMMER50",
    "description": "50% off summer items",
    "discount_type": "percentage",
    "discount_value": "50",
    "min_purchase": "100.00"
  }
}
```

### Reviews

**Create Review**
```http
POST /api/reviews/
Content-Type: application/json

{
  "product_id": 1,
  "customer_name": "John Doe",
  "email": "john@example.com",
  "rating": 5,
  "review_text": "Excellent quality!"
}

Response: 201 Created
```

**List Reviews**
```http
GET /api/reviews/
GET /api/reviews/?limit=6

Response: 200 OK
{
  "data": [
    {
      "id": 1,
      "customer_name": "John Doe",
      "review_text": "Excellent quality!",
      "rating": 5,
      "date": "2025-01-15T10:30:00Z"
    }
  ]
}
```

### Watchlist

**Get Watchlist**
```http
GET /api/watchlist/{user_id}/

Response: 200 OK
{
  "user": 1,
  "products": [1, 5, 12]
}
```

**Add to Watchlist**
```http
POST /api/watchlist/{user_id}/add_product/
Content-Type: application/json

{
  "product_id": 15
}

Response: 200 OK
```

**Remove from Watchlist**
```http
POST /api/watchlist/{user_id}/remove_product/
Content-Type: application/json

{
  "product_id": 15
}

Response: 200 OK
```

### Newsletter

**Subscribe to Newsletter**
```http
POST /api/newsletter/subscribe/
Content-Type: application/json

{
  "email": "user@example.com"
}

Response: 201 Created
{
  "success": true,
  "message": "Successfully subscribed to newsletter",
  "email": "user@example.com"
}
```

---

## Database Models

### Core Models

**1. Category**
- Hierarchical category/collection system
- Fields: name, slug, description, image_url, parent, is_collection, display_order
- Self-referential foreign key for hierarchy
- Auto-generates slug from name
- Tracks product count recursively

**2. Product**
- Main product catalog
- Fields: name, description, price, image_url, category, featured, new_arrival, inventory, sku, on_sale, discount_percent
- Calculated: discounted_price, is_in_stock, rating, review_count
- Indexed for performance

**3. Review**
- Customer product reviews
- Fields: product, customer_name, review_text, rating (1-5), email
- Ordered by creation date

**4. UserProfile**
- Extended user information
- Auto-created on user registration (via signals)
- Fields: phone, address, city, country, postal_code, referral_code, referral_points, total_referrals, is_admin
- Unique referral code generation

### Order Management

**5. Order**
- Customer orders
- Fields: order_id, user, total_price, discount_amount, final_price, voucher_code, status, shipping_address, phone, payment_method, payment_status
- Auto-generates unique order ID
- Status choices: pending, processing, shipped, delivered, cancelled

**6. OrderItem**
- Items in an order
- Fields: order, product, quantity, price_at_purchase, total
- Auto-calculates total

**7. OrderTracking**
- Order shipment tracking
- Fields: order, current_location, estimated_delivery, carrier, tracking_number
- One-to-one with Order

**8. Refund**
- Return/refund requests
- Fields: order, reason, requested_at, amount, status, admin_notes, processed_at, processed_by
- Status choices: requested, approved, rejected, refunded

### Admin Features

**9. Banner**
- Homepage carousel banners
- Fields: title, description, image_url, cta_text, cta_link, is_active, order
- Ordered by priority

**10. Voucher**
- Discount coupons
- Fields: code, description, discount_type, discount_value, min_purchase, max_uses, current_uses, is_active, start_date, end_date
- Types: percentage or fixed amount
- Properties: is_expired, can_use

**11. SalesAnalytics**
- Daily sales tracking
- Fields: date, total_orders, total_revenue, total_items_sold, avg_order_value, total_profit, unique_customers
- Auto-populated (can be done via signals or cron)

### User Features

**12. Watchlist**
- User product wishlist
- Many-to-many with products
- One-to-one with user

**13. Complaint**
- Product/order complaints
- Fields: order_item, user, title, description, status, resolution, resolved_at
- Status choices: open, in_progress, resolved, closed

**14. Referral**
- Referral tracking
- Fields: referrer, referred_user, referral_code, is_active, points_earned
- Unique together: referrer + referred_user

**15. Newsletter**
- Email subscriptions
- Fields: email (unique), subscribed_at, is_active

---

## Common Tasks

### Task 1: Create a Staff User

```bash
# Method 1: Django Admin
1. Login to Django admin: http://localhost:8000/admin/
2. Navigate to Users
3. Create user or edit existing
4. Check "Staff status" and "Superuser status"
5. Save

# Method 2: Python Script (backend/create_staff.py)
cd backend
python create_staff.py

# Method 3: Django Shell
python manage.py shell

from django.contrib.auth.models import User
from api.models import UserProfile

user = User.objects.create_user(
    username='admin',
    email='admin@example.com',
    password='admin123',
    is_staff=True,
    is_superuser=True
)

# Profile auto-created via signals
profile = user.profile
profile.is_admin = True
profile.save()
```

### Task 2: Add Products

```bash
# Django Admin
1. Go to http://localhost:8000/admin/api/product/
2. Click "Add Product"
3. Fill in:
   - Name
   - Description
   - Price
   - Image URL
   - Category
   - Inventory
   - SKU (optional)
   - Check "Featured" or "New Arrival" if applicable
4. Save

# Via API
POST http://localhost:8000/api/products/
{
  "name": "Premium Leather Jacket",
  "description": "Handcrafted leather jacket",
  "price": "299.99",
  "image_url": "https://example.com/jacket.jpg",
  "category": 1,
  "inventory": 25,
  "sku": "JKT-001",
  "featured": true
}
```

### Task 3: Create Collections

```bash
# Via Admin Dashboard (Recommended)
1. Login to http://localhost:3000/admin-dashboard
2. Navigate to "Categories & Collections" tab
3. Click "+ Create Collection"
4. Fill in form:
   - Name: "Summer Collection 2025"
   - Description: "Bright and breezy summer styles"
   - Image URL: https://example.com/summer.jpg
   - Parent: None (for top-level)
   - Display Order: 0
   - Check "Mark as Top-Level Collection"
5. Click "Create Collection"

# Create Sub-Collection
1. Find parent collection in tree
2. Click "Add Sub-Collection" button
3. Fill in form (parent auto-selected)
4. Save
```

### Task 4: Create Voucher

```bash
# Django Admin
1. Go to http://localhost:8000/admin/api/voucher/
2. Click "Add Voucher"
3. Fill in:
   - Code: SUMMER50 (uppercase, no spaces)
   - Description: "50% off summer items"
   - Discount type: Percentage
   - Discount value: 50
   - Min purchase: 100.00
   - Max uses: 1000
   - Is active: ✓
   - Start date: 2025-01-01 00:00:00
   - End date: 2025-12-31 23:59:59
4. Save

# Via API (admin only)
POST http://localhost:8000/api/vouchers/
{
  "code": "SUMMER50",
  "description": "50% off summer items",
  "discount_type": "percentage",
  "discount_value": 50,
  "min_purchase": 100.00,
  "max_uses": 1000,
  "is_active": true,
  "start_date": "2025-01-01T00:00:00Z",
  "end_date": "2025-12-31T23:59:59Z"
}
```

### Task 5: Process a Return

```bash
# Admin Dashboard
1. Login to admin dashboard
2. Navigate to "Returns" tab
3. Find return with "Requested" status
4. Review:
   - Return reason
   - Items being returned
   - Customer information
5. Click "Approve" or "Reject"
6. If approved and product received:
   - Click "Complete"
   - System creates refund
7. Payment status updates to "Refunded"
```

### Task 6: View Analytics

```bash
# Admin Dashboard - Analytics Tab
1. Login to http://localhost:3000/admin-dashboard
2. Click "Analytics" tab
3. Select time range:
   - 7 Days
   - 30 Days
   - 90 Days
   - 1 Year
4. View metrics:
   - Total Revenue (with growth %)
   - Total Orders
   - Items Sold
   - Unique Customers
5. Analyze:
   - Revenue Trend Chart
   - Top Performing Products
   - Performance Metrics
6. Export if needed:
   - Click "Export CSV"
   - Download analytics report
```

### Task 7: Update Product Inventory

```bash
# Django Admin
1. Go to http://localhost:8000/admin/api/product/
2. Find product
3. Update "Inventory" field
4. Save

# Bulk Update (Django Shell)
python manage.py shell

from api.models import Product

# Add 10 to all inventory
Product.objects.all().update(
    inventory=F('inventory') + 10
)

# Set specific product
product = Product.objects.get(id=1)
product.inventory = 100
product.save()
```

---

## Troubleshooting

### Issue 1: Cannot Access Admin Dashboard

**Symptoms:**
- "Access Denied" message
- Redirected away from `/admin-dashboard`

**Solution:**
```bash
# Check user status in Django admin
1. Go to http://localhost:8000/admin/auth/user/
2. Find your user
3. Ensure one of these is checked:
   ☑️ Staff status
   ☑️ Superuser status
4. Save

# Also check UserProfile
1. Go to http://localhost:8000/admin/api/userprofile/
2. Find your profile
3. Check: ☑️ Is admin
4. Save

# Clear browser localStorage and re-login
localStorage.clear()
```

### Issue 2: Analytics Not Loading

**Symptoms:**
- Empty analytics page
- "No data available" message

**Solution:**
```bash
# Check SalesAnalytics data
python manage.py shell

from api.models import SalesAnalytics
SalesAnalytics.objects.all()

# Create sample data if empty
from decimal import Decimal
from datetime import date

SalesAnalytics.objects.create(
    date=date.today(),
    total_orders=10,
    total_revenue=Decimal('1000.00'),
    total_items_sold=25,
    avg_order_value=Decimal('100.00'),
    total_profit=Decimal('300.00'),
    unique_customers=8
)

# Refresh analytics page
```

### Issue 3: Collection Tree Not Showing

**Symptoms:**
- Empty categories/collections tab
- No tree structure visible

**Solution:**
```bash
# Check categories exist
1. Django admin: http://localhost:8000/admin/api/category/
2. Create at least one category with is_collection=True

# Via API
GET http://localhost:8000/api/categories/

# Verify response format
{
  "data": [ /* should have categories */ ]
}

# Check CollectionsManager component
- Ensure API call succeeds
- Check browser console for errors
- Verify data.data.results parsing
```

### Issue 4: Orders Not Creating

**Symptoms:**
- Order submission fails
- API returns error

**Common Causes & Solutions:**

**A. Product Out of Stock**
```bash
# Check inventory
GET /api/products/{id}/
# Ensure inventory > 0

# Update inventory
Django Admin → Products → Edit → Set Inventory
```

**B. Invalid Voucher**
```bash
# Check voucher validity
POST /api/vouchers/validate_code/
{"code": "YOURCODE"}

# Common issues:
- Voucher expired (end_date passed)
- Max uses reached
- Minimum purchase not met
- is_active = False
```

**C. Missing Required Fields**
```javascript
// Ensure all required fields present
{
  "items": [...],           // Required
  "shipping_address": "...", // Required
  "phone": "...",           // Required
  "payment_method": "..."   // Required
  // voucher_code is optional
}
```

### Issue 5: Migration Errors

**Symptoms:**
- Error running `python manage.py migrate`
- "no such table" errors

**Solution:**
```bash
# Reset migrations (CAREFUL: deletes data)
cd backend
rm -rf api/migrations/
python manage.py makemigrations api
python manage.py migrate

# OR keep data, fix individually
python manage.py showmigrations
python manage.py migrate api 0001 --fake
python manage.py migrate
```

### Issue 6: Frontend Build Errors

**Symptoms:**
- TypeScript errors
- Build fails
- Missing dependencies

**Solutions:**

**A. Clear Cache**
```bash
cd frontend
rm -rf .next
rm -rf node_modules/.cache
npm run dev
```

**B. Reinstall Dependencies**
```bash
rm -rf node_modules
rm package-lock.json
npm install
```

**C. TypeScript Errors**
```bash
# Check tsconfig.json is present
# Verify all @types packages installed
npm install --save-dev @types/react @types/node
```

**D. Tailwind CSS Issues**
```bash
# Ensure using v3.4.18 (not v4)
npm install tailwindcss@3.4.18 --save-dev

# Check tailwind.config.ts
# Check postcss.config.js
```

### Issue 7: CORS Errors

**Symptoms:**
- Frontend cannot fetch from backend
- "CORS policy" errors in console

**Solution:**
```python
# backend/config/settings.py

# Ensure CORS configured
INSTALLED_APPS = [
    # ...
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    # ... other middleware
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

CORS_ALLOW_CREDENTIALS = True
```

### Issue 8: Database Connection Failed

**Symptoms:**
- Cannot connect to PostgreSQL
- "authentication failed" errors

**Solution:**
```python
# backend/config/settings.py

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'classycouture_db',  # Verify DB exists
        'USER': 'your_username',     # Verify user exists
        'PASSWORD': 'your_password', # Verify password correct
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Test connection
psql -U your_username -d classycouture_db
```

```bash
# Create database if missing
psql -U postgres
CREATE DATABASE classycouture_db;
CREATE USER your_username WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE classycouture_db TO your_username;
```

### Issue 9: Static Files Not Loading

**Symptoms:**
- CSS not applying
- Images not showing
- JS not working

**Solution:**
```bash
# Django
python manage.py collectstatic

# Next.js
# Ensure images in public/ folder
# Access via /filename.jpg (not /public/filename.jpg)
```

### Issue 10: OpenSSL Error (Anaconda)

**Symptoms:**
```
AttributeError: module 'lib' has no attribute 'OpenSSL_add_all_algorithms'
```

**Solution:**
```bash
# Upgrade packages in Anaconda environment
/Users/alihassancheema/opt/anaconda3/bin/pip install --upgrade pyOpenSSL cryptography cffi

# Verify versions
pip show pyOpenSSL  # Should be 25.3.0+
pip show cryptography  # Should be 46.0.3+
pip show cffi  # Should be 2.0.0+
```

---

## Support & Resources

### Documentation
- **Django:** https://docs.djangoproject.com/
- **Django REST Framework:** https://www.django-rest-framework.org/
- **Next.js:** https://nextjs.org/docs
- **Tailwind CSS:** https://tailwindcss.com/docs

### Project Documentation
- `README_START_HERE.md` - Quick navigation
- `QUICKSTART.md` - 5-minute setup
- `SETUP_GUIDE.md` - Detailed setup
- `FEATURES_GUIDE.md` - API documentation
- `IMPLEMENTATION_GUIDE.md` - Technical details
- `COLLECTIONS_GUIDE.md` - Collections system
- `TROUBLESHOOTING.md` - Common issues

### Key Files
- Backend API: `backend/api/views.py`, `backend/api/views_extended.py`
- Models: `backend/api/models.py`
- Admin Dashboard: `frontend/app/admin-dashboard/page.tsx`
- Components: `frontend/components/admin/`

---

## Appendix

### A. Complete API Endpoint List

```
Authentication:
POST   /api/auth/register/
POST   /api/auth/login/
GET    /api/auth/profile/{id}/
PUT    /api/auth/profile/{id}/

Products:
GET    /api/products/
GET    /api/products/{id}/
POST   /api/products/        (admin)
PUT    /api/products/{id}/   (admin)
DELETE /api/products/{id}/   (admin)

Categories:
GET    /api/categories/
GET    /api/categories/{id}/
POST   /api/categories/      (admin)
PUT    /api/categories/{id}/ (admin)
DELETE /api/categories/{id}/ (admin)

Reviews:
GET    /api/reviews/
GET    /api/reviews/{id}/
POST   /api/reviews/

Newsletter:
POST   /api/newsletter/subscribe/

Analytics:
GET    /api/analytics/       (public)

Banners:
GET    /api/banners/
POST   /api/banners/         (admin)
PUT    /api/banners/{id}/    (admin)
DELETE /api/banners/{id}/    (admin)

Vouchers:
GET    /api/vouchers/        (admin)
POST   /api/vouchers/        (admin)
PUT    /api/vouchers/{id}/   (admin)
POST   /api/vouchers/validate_code/

Orders:
GET    /api/orders/
GET    /api/orders/{id}/
POST   /api/orders/
PUT    /api/orders/{id}/     (admin)

Refunds:
GET    /api/refunds/         (admin)
POST   /api/refunds/
PUT    /api/refunds/{id}/    (admin)

Watchlist:
GET    /api/watchlist/{user_id}/
POST   /api/watchlist/{user_id}/add_product/
POST   /api/watchlist/{user_id}/remove_product/

Complaints:
GET    /api/complaints/
POST   /api/complaints/
PUT    /api/complaints/{id}/ (admin)

Referrals:
GET    /api/referrals/       (admin)
POST   /api/referrals/
```

### B. Database Schema Diagram

```
User (Django Auth)
  ↓ (1:1)
UserProfile
  ├─→ Referral (referrer)
  ├─→ Referral (referred_user)
  ├─→ Order (1:M)
  ├─→ Watchlist (1:1)
  └─→ Complaint (1:M)

Category
  ├─→ Category (self-referential)
  └─→ Product (1:M)

Product
  ├─→ Review (1:M)
  ├─→ OrderItem (M:M via)
  └─→ Watchlist (M:M via)

Order
  ├─→ OrderItem (1:M)
  ├─→ OrderTracking (1:1)
  └─→ Refund (1:1)

Standalone:
- Banner
- Voucher
- SalesAnalytics
- Newsletter
```

### C. Environment Variables

**Frontend (.env.local)**
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**Backend (config/settings.py)**
```python
# Database
DATABASE_NAME=classycouture_db
DATABASE_USER=your_username
DATABASE_PASSWORD=your_password
DATABASE_HOST=localhost
DATABASE_PORT=5432

# Security
SECRET_KEY=your-secret-key-here
DEBUG=True  # False in production

# CORS
CORS_ALLOWED_ORIGINS=["http://localhost:3000"]
```

---

**End of User Guide**

For the latest updates and documentation, visit the project repository or check the documentation files in the project root.

**Version:** 2.0
**Last Updated:** January 2025
