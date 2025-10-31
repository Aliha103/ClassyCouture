# ClassyCouture - New Features Guide

Complete documentation for admin and user features added to ClassyCouture.

## Table of Contents

1. [Authentication System](#authentication-system)
2. [Admin Features](#admin-features)
3. [Order System](#order-system)
4. [User Dashboard Features](#user-dashboard-features)
5. [API Endpoints](#api-endpoints)
6. [Database Models](#database-models)

---

## Authentication System

### User Registration

**Endpoint**: `POST /api/auth/register/`

**Request**:
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securepass123",
  "password_confirm": "securepass123",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Response** (201):
```json
{
  "success": true,
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com"
  }
}
```

**Auto-created items**:
- User profile with unique referral code (e.g., `REFJOHN1DO`)
- Watchlist (empty)
- 0 referral points

### User Login

**Endpoint**: `POST /api/auth/login/`

**Request**:
```json
{
  "username": "john_doe",
  "password": "securepass123"
}
```

**Response** (200):
```json
{
  "success": true,
  "message": "Login successful",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com"
  },
  "profile": {
    "phone": "+1234567890",
    "address": "123 Main St",
    "city": "New York",
    "country": "USA",
    "referral_code": "REFJOHN1DO",
    "referral_points": 100,
    "total_referrals": 5,
    "is_admin": false
  }
}
```

---

## Admin Features

### 1. Dashboard Analytics

**Access**: Only admin users

**View Sales Analytics**
- Endpoint: `GET /api/analytics/`
- Shows: Total orders, revenue, profit, items sold, unique customers

**Sample Response**:
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

### 2. Inventory Management

**Update Product Inventory**
- Endpoint: `PUT /api/products/{id}/`
- Fields: `inventory`, `sku`, `on_sale`, `discount_percent`

**Example**:
```json
{
  "name": "Classic Black Blazer",
  "price": "129.99",
  "inventory": 50,
  "sku": "BLZ-001",
  "on_sale": true,
  "discount_percent": 20
}
```

**Calculated Fields**:
- `discounted_price`: Automatically calculated when on_sale=true
- `is_in_stock`: Boolean for inventory > 0

### 3. Banner Management

**Endpoints**:
- `GET /api/banners/` - View all active banners
- `POST /api/banners/` - Create banner (admin)
- `PUT /api/banners/{id}/` - Edit banner (admin)
- `DELETE /api/banners/{id}/` - Delete banner (admin)

**Create Banner**:
```json
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

### 4. Voucher/Coupon Management

**Endpoints**:
- `GET /api/vouchers/` - View vouchers
- `POST /api/vouchers/` - Create voucher (admin)
- `PUT /api/vouchers/{id}/` - Edit voucher (admin)
- `POST /api/vouchers/validate_code/` - Validate voucher code

**Create Voucher**:
```json
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

**Validate Voucher** (User-facing):
```bash
POST /api/vouchers/validate_code/
{
  "code": "SUMMER50"
}
```

Response:
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

---

## Order System

### 1. Create Order

**Endpoint**: `POST /api/orders/`

**Request**:
```json
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

**Response** (201):
```json
{
  "id": 1,
  "order_id": "ORD-ABC123DEF45",
  "status": "pending",
  "payment_status": "pending",
  "final_price": "449.97",
  "created_at": "2025-01-15T10:30:00Z",
  "items": [
    {
      "product_name": "Classic Black Blazer",
      "quantity": 2,
      "price_at_purchase": "129.99",
      "total": "259.98"
    }
  ]
}
```

### 2. Order Tracking

**View Order Tracking**
- Endpoint: `GET /api/orders/{id}/tracking/`

**Response**:
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

### 3. Order Status

**Order Statuses**:
- `pending` - Order placed, awaiting processing
- `processing` - Order is being prepared
- `shipped` - Order has been shipped
- `delivered` - Order delivered to customer
- `cancelled` - Order cancelled

**Payment Statuses**:
- `pending` - Awaiting payment
- `completed` - Payment received
- `failed` - Payment failed

### 4. Cancel Order

**Endpoint**: `POST /api/orders/{id}/cancel/`

Only possible if order status is `pending`

**Response**:
```json
{
  "success": true,
  "message": "Order cancelled"
}
```

---

## Order Refunds

### Request Refund

**Endpoint**: `POST /api/refunds/request_refund/`

**Request**:
```json
{
  "order_id": 1,
  "reason": "Product arrived damaged"
}
```

**Response** (201):
```json
{
  "id": 1,
  "order": 1,
  "reason": "Product arrived damaged",
  "amount": "449.97",
  "status": "requested",
  "requested_at": "2025-01-15T10:30:00Z",
  "processed_at": null
}
```

### Refund Statuses

- `requested` - User requested refund
- `approved` - Admin approved the refund
- `rejected` - Admin rejected the refund
- `refunded` - Refund amount has been sent

---

## User Dashboard Features

### 1. User Profile

**Get Profile**
- Endpoint: `GET /api/profile/my_profile/`

**Update Profile**
- Endpoint: `PUT /api/profile/update_profile/`

```json
{
  "phone": "+1234567890",
  "address": "123 Main St",
  "city": "New York",
  "country": "USA",
  "postal_code": "10001"
}
```

### 2. Order Dashboard

**View My Orders**
- Endpoint: `GET /api/orders/my_orders/`

**Response**:
```json
{
  "data": [
    {
      "order_id": "ORD-ABC123DEF45",
      "status": "shipped",
      "final_price": "449.97",
      "created_at": "2025-01-15T10:30:00Z",
      "items": [...]
    }
  ]
}
```

### 3. Watchlist Management

**Get Watchlist**
- Endpoint: `GET /api/watchlist/my_watchlist/`

**Add Product to Watchlist**
- Endpoint: `POST /api/watchlist/add_product/`
- Body: `{"product_id": 1}`

**Remove Product from Watchlist**
- Endpoint: `POST /api/watchlist/remove_product/`
- Body: `{"product_id": 1}`

### 4. Product Reviews

**Leave Review**
- Endpoint: `POST /api/product-reviews/`

```json
{
  "product": 1,
  "rating": 5,
  "title": "Excellent Quality",
  "review_text": "The product is amazing! Highly recommended.",
  "is_verified_purchase": true
}
```

**Get My Reviews**
- Endpoint: `GET /api/product-reviews/my_reviews/`

**Get Product Reviews**
- Endpoint: `GET /api/product-reviews/?product_id=1`

### 5. Complaints

**File Complaint**
- Endpoint: `POST /api/complaints/`

```json
{
  "order_item": 1,
  "title": "Item Defective",
  "description": "The zipper on the blazer is broken"
}
```

**Get My Complaints**
- Endpoint: `GET /api/complaints/my_complaints/`

**Complaint Statuses**:
- `open` - Complaint received
- `in_progress` - Being investigated
- `resolved` - Resolution provided
- `closed` - Complaint closed

### 6. Referral System

**Get Referral Info**
- Endpoint: `GET /api/referrals/referral_info/`

```json
{
  "referral_code": "REFJOHN1DO",
  "referral_points": 150,
  "total_referrals": 5
}
```

**Get My Referrals**
- Endpoint: `GET /api/referrals/my_referrals/`

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

**How Referral Works**:
1. User shares their unique referral code
2. New user signs up using the code
3. Both users get referral points
4. Points can be used for discounts or rewards

---

## Complete API Endpoints List

### Authentication
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Login user

### Admin Features
- `GET/POST /api/banners/` - Manage homepage banners
- `GET/POST /api/vouchers/` - Manage vouchers
- `POST /api/vouchers/validate_code/` - Validate voucher (user-facing)
- `GET /api/analytics/` - View sales analytics

### Products
- `GET /api/products/?featured=true` - Featured products
- `PUT /api/products/{id}/` - Update product (admin) - inventory, sale, discount

### Orders & Refunds
- `GET/POST /api/orders/` - Manage orders
- `GET /api/orders/my_orders/` - View user's orders
- `POST /api/orders/{id}/cancel/` - Cancel order
- `GET /api/orders/{id}/tracking/` - Order tracking
- `POST /api/refunds/request_refund/` - Request refund
- `GET /api/refunds/` - View refunds

### User Profile
- `GET /api/profile/my_profile/` - View profile
- `PUT /api/profile/update_profile/` - Update profile

### User Features
- `GET /api/watchlist/my_watchlist/` - View watchlist
- `POST /api/watchlist/add_product/` - Add to watchlist
- `POST /api/watchlist/remove_product/` - Remove from watchlist

### Reviews & Complaints
- `POST /api/product-reviews/` - Leave review
- `GET /api/product-reviews/my_reviews/` - My reviews
- `POST /api/complaints/` - File complaint
- `GET /api/complaints/my_complaints/` - My complaints

### Referrals
- `GET /api/referrals/referral_info/` - Referral info
- `GET /api/referrals/my_referrals/` - All referrals

---

## Database Models

### User-Related Models
- **UserProfile**: Extended user info (phone, address, referral code, points)
- **Watchlist**: Products user is watching
- **ProductReview**: User reviews on products
- **Complaint**: Product complaints/issues

### Admin-Related Models
- **Banner**: Homepage banners
- **Voucher**: Discount codes/coupons
- **SalesAnalytics**: Daily sales tracking

### Order-Related Models
- **Order**: Main order record
- **OrderItem**: Individual items in order
- **OrderTracking**: Tracking info for order
- **Refund**: Refund/return requests

### Referral Model
- **Referral**: Track referral relationships

---

## Key Features Summary

### Admin Can:
✅ Control inventory (stock levels)
✅ Create/edit/delete products
✅ Add sales and discounts to products
✅ Create and manage vouchers/coupons
✅ Change homepage banners
✅ View sales analytics (revenue, profit, orders)
✅ Track order status
✅ Process refunds
✅ View all user activity

### Users Can:
✅ Register and login
✅ View ordered items in dashboard
✅ Track order status in real-time
✅ See total products ordered
✅ Apply vouchers at checkout
✅ Get and share referral codes
✅ See referral points earned
✅ Track referred friends
✅ Manage watchlist
✅ Leave product reviews
✅ File complaints about products
✅ Request refunds
✅ Check refund status

---

## Migration Commands

After making changes to models, run:

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser for admin access
python manage.py createsuperuser
```

---

## Next Steps

1. Build admin frontend dashboard
2. Build user login/registration UI
3. Build user dashboard
4. Build product/order management pages
5. Implement payment gateway
6. Add email notifications

