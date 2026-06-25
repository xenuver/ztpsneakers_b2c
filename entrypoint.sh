#!/bin/sh
set -e

echo "========================================"
echo " ZTP Sneakers — Container Startup"
echo "========================================"

# Tunggu PostgreSQL siap
echo "[1/4] Waiting for PostgreSQL..."
until python -c "
import os, sys, psycopg2
try:
    psycopg2.connect(
        dbname=os.environ.get('DB_NAME','db_ztpsneakers'),
        user=os.environ.get('DB_USER','postgres'),
        password=os.environ.get('DB_PASSWORD',''),
        host=os.environ.get('DB_HOST','db'),
        port=os.environ.get('DB_PORT','5432'),
    )
    sys.exit(0)
except Exception:
    sys.exit(1)
"; do
  echo "   PostgreSQL belum siap, retry dalam 2 detik..."
  sleep 2
done
echo "   PostgreSQL siap!"

# Jalankan migrasi
echo "[2/4] Running migrations..."
python manage.py migrate --noinput

# Jalankan collectstatic
echo "[3/4] Collecting static files..."
python manage.py collectstatic --noinput

# Jalankan seed (idempotent — skip jika data sudah ada)
echo "[4/4] Running seed (idempotent)..."
python seed.py

echo "========================================"
echo " Starting Gunicorn..."
echo "========================================"
exec gunicorn ztpsneakers.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -
