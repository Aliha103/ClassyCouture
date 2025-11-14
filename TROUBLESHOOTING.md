# Troubleshooting Guide - ClassyCouture

## Current Issue: 500 Internal Server Error

You're seeing these errors in the browser console:
```
GET http://localhost:8000/api/products/?featured=true [HTTP/1.1 500 Internal Server Error]
GET http://localhost:8000/api/reviews/?limit=6 [HTTP/1.1 500 Internal Server Error]
GET http://localhost:8000/api/categories/ [HTTP/1.1 500 Internal Server Error]
```

### Root Cause
The Django backend is running but the **database hasn't been set up** (no migrations run, no tables created).

---

## Solution: Set Up the Backend Database

### Quick Fix (Automated)

**In your terminal, run this script:**

```bash
cd /Users/alihassancheema/Desktop/Classy/ClassyCouture/backend
./setup_backend.sh
```

Then restart your Django server.

---

### Manual Fix (Step by Step)

**1. Stop the Django Server**
- Go to the terminal where Django is running
- Press `Ctrl+C` to stop it

**2. Navigate to Backend Directory**
```bash
cd /Users/alihassancheema/Desktop/Classy/ClassyCouture/backend
```

**3. Check if Virtual Environment Exists**
```bash
ls -la venv/
```

If it doesn't exist, create one:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

If it exists, activate it:
```bash
source venv/bin/activate
```

**4. Verify Migrations Directory Exists**
```bash
ls api/migrations/
```

If you see an error, create it:
```bash
mkdir -p api/migrations
touch api/migrations/__init__.py
```

**5. Create Migration Files**
```bash
python manage.py makemigrations
```

You should see:
```
Migrations for 'api':
  api/migrations/0001_initial.py
    - Create model Category
    - Create model Product
    - Create model Review
    - Create model Newsletter
    ... (and other models)
```

**6. Apply Migrations (Create Database Tables)**
```bash
python manage.py migrate
```

You should see:
```
Operations to perform:
  Apply all migrations: admin, api, auth, contenttypes, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  ... (many more)
  Applying api.0001_initial... OK
```

**7. Seed Database with Sample Data**
```bash
python manage.py seed_data
```

You should see:
```
✓ Created category: Women
✓ Created category: Men
✓ Created category: Accessories
✓ Created category: Shoes
✓ Created product: Classic Black Blazer
... (more products)
✓ Created review: Sarah Johnson - Classic Black Blazer
... (more reviews)
✓ Database seeded successfully!
```

**8. Restart Django Server**
```bash
python manage.py runserver
```

**9. Test the API Endpoints**

Open a new terminal and test:

```bash
# Test products
curl http://localhost:8000/api/products/?featured=true

# Test categories
curl http://localhost:8000/api/categories/

# Test reviews
curl http://localhost:8000/api/reviews/?limit=6
```

Each should return JSON data with a `data` array.

**10. Refresh Your Browser**

Go to http://localhost:3000 and you should now see:
- ✓ Featured products loaded
- ✓ Categories displayed
- ✓ Customer reviews shown
- ✓ Newsletter signup working

---

## Common Issues

### Issue: "ModuleNotFoundError: No module named 'django'"

**Solution:** Django is not installed. Install dependencies:
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: "No such file or directory: api/migrations"

**Solution:** Create the migrations directory:
```bash
mkdir -p backend/api/migrations
touch backend/api/migrations/__init__.py
```

### Issue: "python manage.py: command not found"

**Solution:** Make sure you're in the backend directory:
```bash
cd /Users/alihassancheema/Desktop/Classy/ClassyCouture/backend
```

### Issue: Port 8000 already in use

**Solution:** Kill the existing process:
```bash
lsof -i :8000
# Note the PID number
kill -9 <PID>
```

### Issue: npm permission errors

**Solution:** Use custom cache directory:
```bash
cd frontend
npm install --cache /tmp/npm-cache
```

Or fix permissions:
```bash
sudo chown -R 501:20 "/Users/alihassancheema/.npm"
```

---

## Verification Checklist

After setup, verify everything is working:

- [ ] Backend running on http://localhost:8000
- [ ] Frontend running on http://localhost:3000
- [ ] Database file exists: `backend/db.sqlite3`
- [ ] Migrations directory exists: `backend/api/migrations/`
- [ ] API returns 200 status codes (not 500)
- [ ] Frontend displays products, categories, and reviews
- [ ] No errors in browser console (except favicon.ico 404)

---

## Getting Help

If you're still seeing 500 errors after following these steps:

1. **Check Django terminal output** for the actual error traceback
2. **Share the error message** - it will tell you exactly what's wrong
3. **Verify database exists**: `ls -la backend/db.sqlite3`
4. **Check migrations were applied**: `python manage.py showmigrations`

The Django error logs will show the exact problem - look for lines starting with `Traceback` or `Error`.
