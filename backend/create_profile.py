import os
import django
import uuid

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from api.models import UserProfile

User = get_user_model()

# Get admin user
try:
    user = User.objects.get(username='admin')

    # Check if profile exists
    try:
        profile = user.profile
        print(f'Profile already exists for user "{user.username}"')
    except UserProfile.DoesNotExist:
        # Create profile with unique referral code
        referral_code = uuid.uuid4().hex[:8].upper()
        profile = UserProfile.objects.create(
            user=user,
            phone='',
            address='',
            city='',
            country='',
            postal_code='',
            referral_code=referral_code,
            is_admin=True
        )
        print(f'✅ Profile created for user "{user.username}"')
        print(f'Referral code: {referral_code}')

    print('')
    print('User can now login successfully!')

except User.DoesNotExist:
    print('❌ Admin user not found. Please create admin user first.')
