import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Create or update admin user
try:
    user = User.objects.get(username='admin')
    print(f'User "admin" already exists. Updating...')
except User.DoesNotExist:
    user = User(username='admin', email='admin@classycouture.com')
    print('Creating new admin user...')

user.set_password('admin123')
user.is_staff = True
user.is_superuser = True
user.is_active = True
user.save()

print('✅ Staff account created/updated successfully!')
print('')
print('Login Credentials:')
print('━' * 40)
print(f'Username: admin')
print(f'Password: admin123')
print(f'Email:    admin@classycouture.com')
print('━' * 40)
print(f'Admin URL: http://127.0.0.1:8000/admin/')
print('')
