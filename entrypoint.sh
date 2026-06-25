#!/bin/sh
set -e

echo "========================================"
echo " ZTP Sneakers — Container Startup"
echo "========================================"

# --------------------------------------------------------
# [0/5] Copy seed media files ke volume (skip jika ada)
# Diperlukan karena volume mount menimpa /app/media dari image
# -n = no-clobber (tidak timpa file yang sudah ada)
# --------------------------------------------------------
echo "[0/5] Ensuring seed media files in volume..."
if [ -d "/app/media_seed" ]; then
    cp -rn /app/media_seed/. /app/media/ 2>/dev/null || true
    echo "   Seed media files ready."
else
    echo "   [WARN] /app/media_seed tidak ditemukan, skip."
fi

# --------------------------------------------------------
# [1/5] Tunggu PostgreSQL siap
# --------------------------------------------------------
echo "[1/5] Waiting for PostgreSQL..."
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

# --------------------------------------------------------
# [2/5] Jalankan migrasi
# --------------------------------------------------------
echo "[2/5] Running migrations..."
python manage.py migrate --noinput

# --------------------------------------------------------
# [3/5] Collect static files
# --------------------------------------------------------
echo "[3/5] Collecting static files..."
python manage.py collectstatic --noinput

# --------------------------------------------------------
# [4/5] Jalankan seed (idempotent — skip jika sudah ada)
# --------------------------------------------------------
echo "[4/5] Running seed (idempotent)..."
python seed.py

# --------------------------------------------------------
# [5/5] Start Gunicorn
# --------------------------------------------------------
echo "========================================"
echo "[5/5] Starting Gunicorn..."
echo "========================================"
exec gunicorn ztpsneakers.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -
