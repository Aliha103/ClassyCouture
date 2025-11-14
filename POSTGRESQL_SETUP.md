# PostgreSQL Setup Guide for ClassyCouture

## Current Status
✅ Frontend connected to Django backend at http://localhost:8000
❌ Backend using SQLite (needs to be migrated to PostgreSQL)

## Step-by-Step PostgreSQL Migration

### Step 1: Install PostgreSQL

**On macOS:**
```bash
# Using Homebrew
brew install postgresql@15

# Start PostgreSQL service
brew services start postgresql@15
```

**On Ubuntu/Linux:**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
```

**On Windows:**
Download and install from: https://www.postgresql.org/download/windows/

### Step 2: Create PostgreSQL Database

```bash
# Access PostgreSQL prompt
psql postgres

# In PostgreSQL prompt, run:
CREATE DATABASE classycouture;
CREATE USER classyuser WITH PASSWORD 'your_secure_password';
ALTER ROLE classyuser SET client_encoding TO 'utf8';
ALTER ROLE classyuser SET default_transaction_isolation TO 'read committed';
ALTER ROLE classyuser SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE classycouture TO classyuser;

# PostgreSQL 15+ requires additional permission:
\c classycouture
GRANT ALL ON SCHEMA public TO classyuser;

# Exit PostgreSQL prompt
\q
```

### Step 3: Install Python PostgreSQL Adapter

```bash
cd backend

# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate  # Windows

# Install psycopg2
pip install psycopg2-binary
```

### Step 4: Update Django Settings

The settings file has been prepared. Create a `.env` file:

```bash
cd backend
cp .env.example .env
```

Edit `.env` and add these lines:
```env
DB_ENGINE=django.db.backends.postgresql
DB_NAME=classycouture
DB_USER=classyuser
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=5432
```

### Step 5: Export Data from SQLite (Optional - to preserve existing data)

```bash
# In backend directory, with venv activated:
python manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission --indent 2 > data_backup.json
```

### Step 6: Migrate to PostgreSQL

```bash
# Run migrations on PostgreSQL
python manage.py migrate

# Load data if you backed it up (optional)
python manage.py loaddata data_backup.json

# OR seed fresh data
python manage.py seed_data

# Create superuser
python manage.py createsuperuser
```

### Step 7: Restart Django Server

```bash
python manage.py runserver
```

### Step 8: Verify Connection

Test the API:
```bash
curl http://localhost:8000/api/products/?featured=true
curl http://localhost:8000/api/categories/
```

## Troubleshooting

### Error: "psycopg2-binary not found"
```bash
pip install psycopg2-binary
```

### Error: "FATAL: database does not exist"
```bash
psql postgres
CREATE DATABASE classycouture;
\q
```

### Error: "FATAL: role does not exist"
```bash
psql postgres
CREATE USER classyuser WITH PASSWORD 'your_secure_password';
\q
```

### Error: "permission denied for schema public"
```bash
psql classycouture
GRANT ALL ON SCHEMA public TO classyuser;
\q
```

## Verify Database Connection

Check which database Django is using:
```bash
python manage.py shell
>>> from django.db import connection
>>> connection.settings_dict['ENGINE']
# Should show: 'django.db.backends.postgresql'
>>> connection.settings_dict['NAME']
# Should show: 'classycouture'
>>> exit()
```

## Production Considerations

For production deployment:
1. Use strong passwords
2. Enable SSL for database connections
3. Use connection pooling
4. Regular backups
5. Monitor database performance
6. Configure PostgreSQL for production workloads

## Database Backup (PostgreSQL)

```bash
# Backup
pg_dump -U classyuser classycouture > backup.sql

# Restore
psql -U classyuser classycouture < backup.sql
```

## Next Steps

After PostgreSQL is configured:
1. ✅ Frontend will automatically work (no changes needed)
2. ✅ All API endpoints will use PostgreSQL
3. ✅ Data persists in production-ready database
4. ✅ Better performance and scalability
