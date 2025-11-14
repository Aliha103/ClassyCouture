#!/bin/bash

echo "=== ClassyCouture Backend Setup ==="
echo ""

# Navigate to backend directory
cd "$(dirname "$0")"

echo "Step 1: Checking for migrations directory..."
if [ ! -d "api/migrations" ]; then
    echo "Creating migrations directory..."
    mkdir -p api/migrations
    touch api/migrations/__init__.py
    echo "✓ Created migrations directory"
else
    echo "✓ Migrations directory exists"
fi

echo ""
echo "Step 2: Creating migration files..."
python3 manage.py makemigrations

echo ""
echo "Step 3: Applying migrations..."
python3 manage.py migrate

echo ""
echo "Step 4: Seeding database with sample data..."
python3 manage.py seed_data

echo ""
echo "=== Setup Complete! ==="
echo ""
echo "You can now start the server with:"
echo "  python3 manage.py runserver"
