# Account Pages - Implementation Guide

## ✅ Pages Created

Your ClassyCouture site now has complete authentication and account management pages!

### 1. **Login Page** - `/login`
- **URL**: http://localhost:3000/login
- **Features**:
  - Email and password authentication
  - "Forgot password?" link
  - Social login placeholders (Google, GitHub)
  - Link to registration page
  - Form validation and error handling
  - Success messages and redirects
  - Stores auth token in localStorage

### 2. **Register Page** - `/register`
- **URL**: http://localhost:3000/register
- **Features**:
  - Full name, email, and password fields
  - Password confirmation validation
  - Minimum password length (8 characters)
  - Social registration placeholders
  - Link to login page
  - Success messages and redirects
  - Terms of service and privacy policy links

### 3. **Account/Profile Page** - `/account`
- **URL**: http://localhost:3000/account
- **Features**:
  - Protected route (requires login)
  - Profile information management
  - Recent orders section
  - Wishlist section
  - Account settings
  - Email notifications preferences
  - Password change
  - Account deletion option
  - Logout functionality

## 🔗 Navigation

The **Account** button in the navbar is now **clickable** and links to:
- `/account` - Your account dashboard
- If not logged in, redirects to login page with options to sign in or register

## 🎨 Design Features

All pages include:
- ✅ Beautiful, modern UI with shadcn/ui components
- ✅ Responsive design (mobile, tablet, desktop)
- ✅ Form validation
- ✅ Loading states
- ✅ Error handling
- ✅ Success messages
- ✅ Smooth animations
- ✅ Consistent branding with ClassyCouture

## 🔐 Authentication Flow

```
1. User clicks "Account" in navbar
   ↓
2. Check if user is logged in (localStorage token)
   ↓
3a. If YES → Show account dashboard
   ↓
3b. If NO → Show login/register options
   ↓
4. User signs in/registers
   ↓
5. Token stored in localStorage
   ↓
6. Redirect to account page
```

## 🛠️ Backend Integration (TODO)

The frontend is ready for backend integration. You'll need to implement these Django API endpoints:

### Required Endpoints:

1. **Login**
   ```
   POST /api/auth/login/
   Body: { email, password }
   Response: { token, user: {...} }
   ```

2. **Register**
   ```
   POST /api/auth/register/
   Body: { username, email, password }
   Response: { success, message }
   ```

3. **Get User Profile**
   ```
   GET /api/auth/profile/
   Headers: Authorization: Token <token>
   Response: { user: {...} }
   ```

4. **Update Profile**
   ```
   PATCH /api/auth/profile/
   Headers: Authorization: Token <token>
   Body: { name, email, phone, address }
   ```

5. **Logout**
   ```
   POST /api/auth/logout/
   Headers: Authorization: Token <token>
   ```

## 📝 How to Test

1. **Visit Login Page**
   ```
   http://localhost:3000/login
   ```

2. **Try Registration**
   ```
   http://localhost:3000/register
   ```

3. **Click Account in Navbar**
   - Should show login/register options if not logged in

4. **After Login**
   - Click Account button
   - Should show account dashboard

## 🔄 Current Behavior (Without Backend)

Right now:
- Login and register forms are displayed correctly
- Forms submit to `/api/auth/login/` and `/api/auth/register/`
- These endpoints don't exist yet (will return 404)
- You can still navigate and see all pages
- Account page shows when you're logged in (based on localStorage)

## 🚀 Next Steps to Make It Fully Functional

### Option 1: Quick Mock (For Testing)
You can temporarily mock the login by:
1. Go to browser console
2. Run: `localStorage.setItem('auth_token', 'mock-token')`
3. Click Account button - you'll see the dashboard!

### Option 2: Implement Backend Auth (Recommended)

Create Django authentication endpoints. Here's a quick guide:

**In `backend/api/views_extended.py`, the `AuthViewSet` already exists!**

You just need to ensure:
1. Django REST Framework Token Authentication is set up
2. CORS allows authentication headers
3. User model is properly configured

## 📱 Pages Overview

### Login Page
- Clean, centered card design
- Email/password fields with icons
- Remember me option (future feature)
- Forgot password link
- Social login buttons (disabled - ready for OAuth)
- Link to register

### Register Page
- Similar design to login
- Additional fields: name, confirm password
- Password strength indicator (future feature)
- Password validation
- Terms acceptance (future feature)
- Social registration buttons

### Account Page
**Layout:**
- Sidebar with user profile and navigation
- Main content area with tabs:
  - Profile (editable fields)
  - Orders (empty state - ready for order data)
  - Wishlist (empty state - ready for wishlist items)
  - Settings (email preferences, password change, account deletion)

## 🎯 Features Ready for Backend

All these features just need backend endpoints:
- ✅ User registration
- ✅ Email/password login
- ✅ Token-based authentication
- ✅ Profile management
- ✅ Order history display
- ✅ Wishlist management
- ✅ Account settings
- ✅ Password change
- ✅ Account deletion

## 💡 Tips

1. **Testing Login Flow**
   - Open DevTools Console
   - Check Network tab when submitting forms
   - See localStorage for auth token

2. **Customization**
   - All pages use shadcn/ui components
   - Easy to customize colors in [tailwind.config.ts](frontend/tailwind.config.ts)
   - Modify [globals.css](frontend/app/globals.css) for global styles

3. **Adding Features**
   - Social login: Connect OAuth providers
   - Email verification: Add email service
   - Two-factor auth: Add 2FA component
   - Profile picture: Add image upload

## 📚 Files Created

- [frontend/app/login/page.tsx](frontend/app/login/page.tsx) - Login page
- [frontend/app/register/page.tsx](frontend/app/register/page.tsx) - Registration page
- [frontend/app/account/page.tsx](frontend/app/account/page.tsx) - Account dashboard
- Updated: [frontend/app/page.tsx](frontend/app/page.tsx) - Made Account button clickable

## ✨ Summary

You now have a complete authentication system UI ready to connect to your Django backend. The Account button in the navbar works and takes users through a proper authentication flow. All pages are beautifully designed, responsive, and ready for backend integration!
