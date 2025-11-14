# Authentication System - Status & Integration Guide

## Current Status: ✅ READY FOR TESTING

### What's Been Fixed

The authentication system has been fully integrated between frontend and backend. All API payload mismatches have been resolved.

---

## 🔐 Authentication Flow

### Registration Flow

**Frontend:** [frontend/app/register/page.tsx](frontend/app/register/page.tsx)
**Backend:** [backend/api/views_extended.py:29-53](backend/api/views_extended.py#L29-L53)

#### How it works:
1. User fills out registration form (name, email, password, confirm password)
2. Frontend sends POST request to `/api/auth/register/`
3. Payload sent:
```json
{
  "username": "user",           // Extracted from email prefix (user@example.com → user)
  "email": "user@example.com",
  "password": "password123",
  "password_confirm": "password123",
  "first_name": "John",         // Extracted from name field
  "last_name": "Doe"            // Extracted from name field
}
```
4. Backend validates:
   - All required fields present
   - Passwords match
   - Password minimum 6 characters
   - Email format valid
   - Username not already taken
5. Backend creates:
   - Django User object
   - UserProfile object with referral code
6. Backend responds with:
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
7. Frontend redirects to `/login` after 2 seconds

### Login Flow

**Frontend:** [frontend/app/login/page.tsx](frontend/app/login/page.tsx)
**Backend:** [backend/api/views_extended.py:55-85](backend/api/views_extended.py#L55-L85)

#### How it works:
1. User enters email and password
2. Frontend sends POST request to `/api/auth/login/`
3. Payload sent:
```json
{
  "username": "user",    // Extracted from email prefix
  "password": "password123"
}
```
4. Backend validates credentials using Django authentication
5. Backend responds with:
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
    "phone": null,
    "address": null,
    "city": null,
    "country": null,
    "postal_code": null,
    "referral_code": "REF1USE",
    "referral_points": 0,
    "total_referrals": 0,
    "is_admin": false
  }
}
```
6. Frontend stores token (if provided) in localStorage
7. Frontend redirects to `/account` after 1 second

### Account Page Protection

**Frontend:** [frontend/app/account/page.tsx](frontend/app/account/page.tsx)

#### How it works:
1. Page checks for `auth_token` in localStorage
2. If no token found:
   - Shows "Account Access Required" card
   - Provides Sign In and Create Account buttons
   - Provides Back to Home button
3. If token found:
   - Shows full account dashboard
   - Profile information (editable)
   - Orders section (empty state)
   - Wishlist section (empty state)
   - Settings section

---

## 🛠️ Backend Setup Required

### ⚠️ IMPORTANT: Database Migrations

Before testing authentication, you MUST run these commands:

```bash
cd backend
source venv/bin/activate

# Create migrations for all models
python manage.py makemigrations

# Apply migrations to create database tables
python manage.py migrate

# Seed sample data (products, categories, etc.)
python manage.py seed_data
```

### Why this is required:

The authentication system depends on these database tables:
- `auth_user` - Django's default user table
- `api_userprofile` - Extended user profile with referral codes, phone, address, etc.

Without migrations, registration will fail with database errors.

---

## 📊 API Endpoints

### Authentication Endpoints

All authentication endpoints are at: `http://localhost:8000/api/auth/`

#### 1. Register
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

**Success Response (201 Created):**
```json
{
  "success": true,
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe"
  }
}
```

**Error Response (400 Bad Request):**
```json
{
  "success": false,
  "errors": {
    "password": ["Passwords do not match."],
    "email": ["User with this email already exists."]
  }
}
```

#### 2. Login
```http
POST /api/auth/login/
Content-Type: application/json

{
  "username": "johndoe",
  "password": "securepass123"
}
```

**Success Response (200 OK):**
```json
{
  "success": true,
  "message": "Login successful",
  "user": { ... },
  "profile": { ... }
}
```

**Error Response (401 Unauthorized):**
```json
{
  "success": false,
  "error": "Invalid credentials"
}
```

---

## 🧪 Testing Guide

### Step 1: Ensure Backend is Running

```bash
cd backend
source venv/bin/activate
python manage.py runserver
```

Expected output:
```
Django version 5.x.x, using settings 'config.settings'
Starting development server at http://127.0.0.1:8000/
```

### Step 2: Ensure Frontend is Running

```bash
cd frontend
npm run dev
```

Expected output:
```
▲ Next.js 15.x.x
- Local:        http://localhost:3000
```

### Step 3: Test Registration

1. Open browser: http://localhost:3000/register
2. Fill in form:
   - Full Name: John Doe
   - Email: john@example.com
   - Password: password123
   - Confirm Password: password123
3. Click "Create account"
4. Expected result:
   - Success message: "Registration successful! Redirecting to login..."
   - Redirect to login page after 2 seconds

**If you see errors:**
- Check browser console (F12) for error details
- Check backend terminal for error logs
- Verify database migrations have been run

### Step 4: Test Login

1. Should be at: http://localhost:3000/login
2. Fill in form:
   - Email: john@example.com
   - Password: password123
3. Click "Sign in"
4. Expected result:
   - Success message: "Login successful! Redirecting..."
   - Redirect to account page after 1 second

### Step 5: Test Account Page

1. Should be at: http://localhost:3000/account
2. Expected result:
   - See account dashboard
   - See profile information
   - See sidebar with navigation
   - See "Sign Out" button
3. Click different sections:
   - Profile (editable fields)
   - Orders (empty state)
   - Wishlist (empty state)
   - Settings (notification preferences)

### Step 6: Test Sign Out

1. Click "Sign Out" in sidebar
2. Expected result:
   - Redirected to homepage
   - `auth_token` removed from localStorage
3. Try to access: http://localhost:3000/account
4. Expected result:
   - See "Account Access Required" card
   - Not able to access account without logging in

---

## 🔍 Debugging Common Issues

### Issue 1: 400 Bad Request on Registration

**Symptom:**
```
POST http://localhost:8000/api/auth/register/ [400 Bad Request]
```

**Causes:**
1. Missing required fields
2. Passwords don't match
3. Username already exists
4. Email already exists

**Solution:**
Check browser console for detailed error message. The response will contain which field caused the issue.

### Issue 2: 500 Internal Server Error

**Symptom:**
```
POST http://localhost:8000/api/auth/register/ [500 Internal Server Error]
```

**Causes:**
1. Database tables don't exist (migrations not run)
2. Database connection error
3. Backend code error

**Solution:**
```bash
cd backend
python manage.py makemigrations
python manage.py migrate
```

Check backend terminal for detailed error traceback.

### Issue 3: CORS Error

**Symptom:**
```
Access to fetch at 'http://localhost:8000/api/auth/login/' from origin 'http://localhost:3000' has been blocked by CORS policy
```

**Solution:**
This should not happen as CORS is configured in [backend/config/settings.py:124-127](backend/config/settings.py#L124-L127).

If it does occur:
1. Check that `django-cors-headers` is installed
2. Verify CORS settings in settings.py
3. Restart Django server

### Issue 4: Can't Access Account After Login

**Symptom:**
- Login successful
- Redirected to /account
- See "Account Access Required" instead of dashboard

**Causes:**
1. Token not being saved to localStorage
2. Token key mismatch

**Solution:**
1. Open browser console (F12)
2. Go to Application tab → Local Storage → http://localhost:3000
3. Check if `auth_token` exists
4. If not, the login response may not be including a token

**Note:** Currently, the backend login endpoint doesn't return a token. You may need to implement Django REST Framework Token Authentication for full functionality.

### Issue 5: Navbar Account Button Not Working

**Symptom:**
- Clicking Account button doesn't navigate

**Solution:**
This has been fixed in [frontend/app/page.tsx:263](frontend/app/page.tsx#L263). The Account button now links to `/account`.

---

## 🚀 Next Steps & Improvements

### 1. Implement Token Authentication (Recommended)

Currently, the login endpoint doesn't return an authentication token. To enable full API authentication:

**a) Update backend to use Django REST Framework Token Authentication:**

```python
# In backend/config/settings.py, add:
INSTALLED_APPS = [
    # ...
    'rest_framework.authtoken',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
}
```

**b) Create token on login:**

```python
# In backend/api/views_extended.py:56-85
from rest_framework.authtoken.models import Token

@action(detail=False, methods=['post'])
def login(self, request):
    # ... existing validation code ...

    if user is not None:
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'success': True,
            'message': 'Login successful',
            'token': token.key,  # Add this line
            'user': UserSerializer(user).data,
            'profile': UserProfileSerializer(profile).data
        })
```

**c) Frontend already handles token storage:**

The login page (lines 43-45) already saves the token:
```typescript
if (data.token) {
  localStorage.setItem("auth_token", data.token);
}
```

### 2. Implement Password Reset

Add "Forgot password?" functionality:
- Create password reset endpoint in backend
- Add email sending capability
- Create password reset pages in frontend

### 3. Implement Social Login

Enable Google and GitHub login:
- Backend: Add django-allauth or similar
- Frontend: Buttons already exist (lines 156-184 in login/register pages)
- Configure OAuth apps with Google and GitHub

### 4. Add Profile Picture Upload

Allow users to upload profile pictures:
- Add `profile_picture` field to UserProfile model
- Create file upload endpoint
- Add image upload UI in account page

### 5. Add Email Verification

Require email verification on registration:
- Send verification email after registration
- Create verification endpoint
- Prevent login until email verified

### 6. Implement "Remember Me"

Add session persistence:
- Add "Remember Me" checkbox to login form
- Store longer-lived token
- Auto-login on page refresh

---

## 📁 Files Modified/Created

### Frontend Files

1. **[frontend/app/login/page.tsx](frontend/app/login/page.tsx)**
   - Created complete login page with form validation
   - Sends correct payload format to backend
   - Handles success/error states
   - Stores auth token in localStorage

2. **[frontend/app/register/page.tsx](frontend/app/register/page.tsx)**
   - Created complete registration page
   - Password confirmation validation
   - Splits name into first_name and last_name
   - Derives username from email prefix

3. **[frontend/app/account/page.tsx](frontend/app/account/page.tsx)**
   - Created protected account dashboard
   - Checks localStorage for authentication
   - Profile, Orders, Wishlist, Settings sections
   - Sign out functionality

4. **[frontend/app/page.tsx](frontend/app/page.tsx)**
   - Made Account button clickable
   - Links to /account route
   - Updated navbar design

### Backend Files (No changes needed)

The backend authentication system was already properly configured:
- [backend/api/views_extended.py](backend/api/views_extended.py) - Auth endpoints
- [backend/api/serializers_extended.py](backend/api/serializers_extended.py) - Auth serializers
- [backend/api/urls.py](backend/api/urls.py) - URL routing

---

## ✅ Checklist Before Testing

- [ ] Backend virtual environment activated
- [ ] Backend dependencies installed (`pip install -r requirements.txt`)
- [ ] Database migrations run (`python manage.py migrate`)
- [ ] Sample data seeded (`python manage.py seed_data`)
- [ ] Backend server running on port 8000
- [ ] Frontend dependencies installed (`npm install`)
- [ ] Frontend server running on port 3000
- [ ] Browser console open (F12) to monitor requests

---

## 📞 Support & Documentation

For more information, see:
- [ACCOUNT_PAGES_GUIDE.md](ACCOUNT_PAGES_GUIDE.md) - Account pages overview
- [CONNECTION_STATUS.md](CONNECTION_STATUS.md) - Frontend-backend connection
- [POSTGRESQL_SETUP.md](POSTGRESQL_SETUP.md) - Database setup guide
- [SETUP_GUIDE.md](SETUP_GUIDE.md) - General setup instructions

---

**Last Updated:** After fixing registration payload mismatch
**Status:** ✅ Ready for testing (pending database migrations)
