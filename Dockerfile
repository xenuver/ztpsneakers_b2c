FROM python:3.12-slim

# System dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Workdir
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Simpan seed media di path TERPISAH (tidak kena volume mount)
# Entrypoint akan copy ke /app/media saat startup jika file belum ada
RUN cp -r /app/media /app/media_seed

# Copy entrypoint dan set executable
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh


# Port Django/Gunicorn
EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]
