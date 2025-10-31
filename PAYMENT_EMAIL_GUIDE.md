# Payment & Email Notifications Implementation Guide

Complete guide for adding Stripe payment processing and email notifications to ClassyCouture.

---

## Part 1: Payment Processing with Stripe

### Step 1: Install Stripe

**Backend**
```bash
cd backend
pip install stripe
```

**Frontend**
```bash
cd frontend
npm install @stripe/stripe-js @stripe/react-stripe-js
```

### Step 2: Add Stripe to Django Settings

**backend/config/settings.py**
```python
# Add to end of file
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')
STRIPE_PUBLISHABLE_KEY = os.getenv('STRIPE_PUBLISHABLE_KEY')
```

### Step 3: Environment Variables

**backend/.env**
```
STRIPE_SECRET_KEY=sk_test_your_secret_key_here
STRIPE_PUBLISHABLE_KEY=pk_test_your_public_key_here
```

**frontend/.env.local**
```
NEXT_PUBLIC_STRIPE_KEY=pk_test_your_public_key_here
```

### Step 4: Create Payment Service

**backend/api/services/payment.py**
```python
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

class StripePaymentService:
    @staticmethod
    def create_payment_intent(amount, currency='usd', metadata=None):
        """Create a payment intent for Stripe"""
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

    @staticmethod
    def confirm_payment(intent_id):
        """Confirm payment was successful"""
        try:
            intent = stripe.PaymentIntent.retrieve(intent_id)
            return intent.status == 'succeeded'
        except stripe.error.StripeError:
            return False
```

### Step 5: Create Payment Endpoint

**backend/api/views_payment.py**
```python
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .services.payment import StripePaymentService
from .models import Order

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_payment_intent(request):
    """Create payment intent for order"""
    order_id = request.data.get('order_id')
    amount = request.data.get('amount')

    if not order_id or not amount:
        return Response(
            {'error': 'Missing order_id or amount'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        order = Order.objects.get(id=order_id, user=request.user)
    except Order.DoesNotExist:
        return Response(
            {'error': 'Order not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    result = StripePaymentService.create_payment_intent(
        amount=amount,
        metadata={'order_id': order_id, 'user_id': request.user.id}
    )

    if result['success']:
        return Response(result)
    return Response(result, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def confirm_payment(request):
    """Confirm payment and update order"""
    intent_id = request.data.get('intent_id')
    order_id = request.data.get('order_id')

    if StripePaymentService.confirm_payment(intent_id):
        order = Order.objects.get(id=order_id)
        order.payment_status = 'completed'
        order.save()
        return Response({'success': True})

    return Response(
        {'success': False, 'error': 'Payment confirmation failed'},
        status=status.HTTP_400_BAD_REQUEST
    )
```

### Step 6: Add Payment Routes

**backend/api/urls.py** - Add:
```python
from .views_payment import create_payment_intent, confirm_payment

urlpatterns = [
    # ... existing patterns
    path('payments/create-intent/', create_payment_intent, name='create-payment-intent'),
    path('payments/confirm/', confirm_payment, name='confirm-payment'),
]
```

### Step 7: Frontend Payment Component

**frontend/components/PaymentForm.tsx**
```typescript
'use client';

import { useState } from 'react';
import {
  CardElement,
  useStripe,
  useElements,
} from '@stripe/react-stripe-js';

interface PaymentFormProps {
  orderId: number;
  amount: number;
  onSuccess: () => void;
}

export default function PaymentForm({
  orderId,
  amount,
  onSuccess,
}: PaymentFormProps) {
  const stripe = useStripe();
  const elements = useElements();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    if (!stripe || !elements) return;

    try {
      // 1. Create payment intent on backend
      const intentRes = await fetch(
        `${apiUrl}/api/payments/create-intent/`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
          },
          body: JSON.stringify({ order_id: orderId, amount }),
        }
      );

      const intentData = await intentRes.json();

      if (!intentData.success) {
        setError('Failed to create payment');
        return;
      }

      // 2. Confirm payment with Stripe
      const result = await stripe.confirmCardPayment(
        intentData.client_secret,
        {
          payment_method: {
            card: elements.getElement(CardElement)!,
          },
        }
      );

      if (result.error) {
        setError(result.error.message || 'Payment failed');
        return;
      }

      // 3. Confirm payment on backend
      const confirmRes = await fetch(
        `${apiUrl}/api/payments/confirm/`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
          },
          body: JSON.stringify({
            intent_id: intentData.intent_id,
            order_id: orderId,
          }),
        }
      );

      if (confirmRes.ok) {
        onSuccess();
      } else {
        setError('Payment confirmation failed');
      }
    } catch (err) {
      setError('Payment processing error');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <CardElement
        options={{
          style: {
            base: {
              fontSize: '16px',
              color: '#424770',
            },
            invalid: {
              color: '#9e2146',
            },
          },
        }}
      />

      {error && (
        <div className="bg-red-50 border border-red-200 rounded p-3">
          <p className="text-red-800 text-sm">{error}</p>
        </div>
      )}

      <button
        type="submit"
        disabled={!stripe || loading}
        className="w-full bg-brand-blue hover:bg-blue-700 disabled:bg-gray-400 text-white px-4 py-2 rounded font-medium"
      >
        {loading ? 'Processing...' : `Pay $${amount.toFixed(2)}`}
      </button>
    </form>
  );
}
```

---

## Part 2: Email Notifications

### Step 1: Install Email Package

**backend**
```bash
pip install django-anymail
```

### Step 2: Configure Email Backend

**backend/config/settings.py**
```python
# Email Configuration
EMAIL_BACKEND = "anymail.backends.sendgrid.EmailBackend"
ANYMAIL = {
    "SENDGRID_API_KEY": os.getenv('SENDGRID_API_KEY'),
}

# Or for Gmail (less secure, for testing)
if os.getenv('EMAIL_BACKEND') == 'gmail':
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
```

### Step 3: Environment Variables

**backend/.env**
```
# SendGrid
SENDGRID_API_KEY=your_sendgrid_api_key_here

# Or Gmail (less secure)
EMAIL_BACKEND=gmail
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password_here
```

### Step 4: Create Email Service

**backend/api/services/email.py**
```python
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

class EmailService:
    @staticmethod
    def send_order_confirmation(user_email, order):
        """Send order confirmation email"""
        context = {
            'order_id': order.order_id,
            'amount': order.final_price,
            'items': order.items.all(),
            'shipping_address': order.shipping_address,
        }

        subject = f'Order Confirmation - {order.order_id}'
        html_message = render_to_string('emails/order_confirmation.html', context)

        send_mail(
            subject,
            '',
            settings.DEFAULT_FROM_EMAIL,
            [user_email],
            html_message=html_message,
            fail_silently=False,
        )

    @staticmethod
    def send_order_shipped(user_email, order):
        """Send order shipped notification"""
        context = {
            'order_id': order.order_id,
            'tracking_number': order.tracking.tracking_number if hasattr(order, 'tracking') else 'N/A',
        }

        subject = f'Your Order Has Shipped - {order.order_id}'
        html_message = render_to_string('emails/order_shipped.html', context)

        send_mail(
            subject,
            '',
            settings.DEFAULT_FROM_EMAIL,
            [user_email],
            html_message=html_message,
            fail_silently=False,
        )

    @staticmethod
    def send_refund_approved(user_email, order):
        """Send refund approved notification"""
        context = {
            'order_id': order.order_id,
            'amount': order.final_price,
        }

        subject = f'Refund Approved - {order.order_id}'
        html_message = render_to_string('emails/refund_approved.html', context)

        send_mail(
            subject,
            '',
            settings.DEFAULT_FROM_EMAIL,
            [user_email],
            html_message=html_message,
            fail_silently=False,
        )

    @staticmethod
    def send_welcome_email(user):
        """Send welcome email to new user"""
        context = {
            'name': user.first_name or user.username,
            'referral_code': user.profile.referral_code,
        }

        subject = 'Welcome to ClassyCouture!'
        html_message = render_to_string('emails/welcome.html', context)

        send_mail(
            subject,
            '',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            html_message=html_message,
            fail_silently=False,
        )
```

### Step 5: Create Email Templates

**backend/templates/emails/order_confirmation.html**
```html
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background-color: #1976d2; color: white; padding: 20px; }
        .content { padding: 20px; background-color: #f9f9f9; }
        .item { padding: 10px; border-bottom: 1px solid #ddd; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Order Confirmation</h1>
        </div>
        <div class="content">
            <p>Hi there!</p>
            <p>Thank you for your order! Here are your order details:</p>

            <h3>Order #{{ order_id }}</h3>
            <p><strong>Total Amount:</strong> ${{ amount }}</p>

            <h3>Items:</h3>
            {% for item in items %}
                <div class="item">
                    <p>{{ item.product.name }} × {{ item.quantity }} - ${{ item.total }}</p>
                </div>
            {% endfor %}

            <h3>Shipping Address:</h3>
            <p>{{ shipping_address }}</p>

            <p>You'll receive a shipping notification soon!</p>
        </div>
    </div>
</body>
</html>
```

### Step 6: Send Emails After Order

**Update backend/api/models.py** - Add to Order model:
```python
def save(self, *args, **kwargs):
    is_new = not self.pk
    super().save(*args, **kwargs)

    if is_new:
        # Send confirmation email on order creation
        from .services.email import EmailService
        EmailService.send_order_confirmation(self.user.email, self)
```

### Step 7: Send Email on Status Update

**backend/api/views.py** - Update OrderViewSet:
```python
@action(detail=True, methods=['put'])
def update_status(self, request, pk=None):
    """Update order status and send notification"""
    order = self.get_object()
    new_status = request.data.get('status')

    order.status = new_status
    order.save()

    # Send email based on status
    from .services.email import EmailService
    if new_status == 'shipped':
        EmailService.send_order_shipped(order.user.email, order)
    elif new_status == 'delivered':
        EmailService.send_delivery_confirmation(order.user.email, order)

    return Response({'success': True})
```

---

## Testing Payment & Email

### Test Payment Flow
```bash
# Use Stripe test card: 4242 4242 4242 4242
# Use any future expiry date and CVC
# Card will succeed and create order
```

### Test Email
```bash
# Set EMAIL_BACKEND to 'django.core.mail.backends.console.EmailBackend'
# Emails will print to console instead of sending
```

---

## Webhook Setup (Production)

### Stripe Webhooks

**backend/api/views_webhooks.py**
```python
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import stripe
from django.conf import settings

@csrf_exempt
def stripe_webhook(request):
    """Handle Stripe webhook events"""
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        return JsonResponse({'status': 'failed'}, status=400)
    except stripe.error.SignatureVerificationError:
        return JsonResponse({'status': 'failed'}, status=400)

    # Handle event
    if event['type'] == 'payment_intent.succeeded':
        # Update order status
        pass

    return JsonResponse({'status': 'success'})
```

---

## Full Implementation Checklist

- [ ] Install Stripe packages
- [ ] Set up Stripe API keys
- [ ] Create payment service
- [ ] Add payment endpoints
- [ ] Create PaymentForm component
- [ ] Install email backend
- [ ] Configure email settings
- [ ] Create email service
- [ ] Create email templates
- [ ] Add email triggers to models
- [ ] Test payment flow with test card
- [ ] Test email sending
- [ ] Set up production credentials
- [ ] Configure Stripe webhooks (production)
- [ ] Test end-to-end flow

---

## Environment Variables Summary

**Production Backend (.env)**
```
STRIPE_SECRET_KEY=sk_live_...
STRIPE_PUBLISHABLE_KEY=pk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...
SENDGRID_API_KEY=SG....
```

**Production Frontend (.env.production)**
```
NEXT_PUBLIC_STRIPE_KEY=pk_live_...
```

---

## Resources

- Stripe Documentation: https://stripe.com/docs
- SendGrid Documentation: https://docs.sendgrid.com/
- Django Email: https://docs.djangoproject.com/en/stable/topics/email/
- Stripe React: https://stripe.com/docs/stripe-js/react

