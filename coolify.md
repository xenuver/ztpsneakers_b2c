# 🚀 Panduan Deploy ZTP Sneakers ke Coolify

Panduan lengkap untuk men-deploy aplikasi Django **ZTP Sneakers** ke [Coolify](https://coolify.io) menggunakan **Docker Compose Buildpack**.

---

## Prasyarat

| Kebutuhan | Keterangan |
|-----------|------------|
| Server VPS | Min. 1 vCPU, 1 GB RAM (2 GB direkomendasikan) |
| Coolify | Terinstall di server (`curl -fsSL https://cdn.coolify.io/install.sh \| bash`) |
| Git Repository | Project sudah di-push ke GitHub / GitLab / Gitea |
| Domain | Opsional — bisa pakai IP langsung untuk awal |

---

## Struktur File Docker yang Dibutuhkan

Pastikan file-file berikut sudah ada di root project (`ztpsneakers/`):

```
ztpsneakers/
├── Dockerfile          ✅ Sudah dibuat
├── docker-compose.yml  ✅ Sudah dibuat
├── entrypoint.sh       ✅ Sudah dibuat
├── .dockerignore       ✅ Sudah dibuat
├── requirements.txt    ✅ Sudah di-update (dengan gunicorn)
└── seed.py             ✅ Sudah diupdate (idempotent)
```

---

## Langkah 1 — Push ke Git Repository

Sebelum ke Coolify, pastikan semua perubahan sudah di-commit dan di-push:

```bash
cd ztpsneakers/
git add Dockerfile docker-compose.yml entrypoint.sh .dockerignore requirements.txt seed.py
git commit -m "chore: add Docker & Coolify deployment config"
git push origin main
```

> [!IMPORTANT]
> Jangan push file `.env` ke repository! File tersebut sudah ada di `.gitignore`.

---

## Langkah 2 — Akses Coolify Dashboard

1. Buka browser dan akses Coolify di: `http://YOUR_SERVER_IP:8000`
2. Login dengan akun Coolify Anda
3. Klik **"Projects"** di sidebar kiri

---

## Langkah 3 — Buat Project Baru

1. Klik tombol **"+ New Project"**
2. Isi nama project: `ZTP Sneakers`
3. Klik **"Create"**
4. Masuk ke project yang baru dibuat
5. Pilih environment (contoh: `production`)

---

## Langkah 4 — Tambah Resource / Service Baru

1. Di dalam environment, klik **"+ Add New Resource"**
2. Pilih **"Application"**
3. Pilih source repository Anda:
   - **GitHub** — klik "GitHub App" atau "GitHub via token"
   - **GitLab** — klik "GitLab"
   - **Public Git** — masukkan URL repo publik
4. Pilih repository `ztpsneakers_b2c` dan branch `main`

---

## Langkah 5 — Konfigurasi Build Settings

Setelah memilih repo, konfigurasi build:

| Setting | Nilai |
|---------|-------|
| **Build Pack** | `Docker Compose` |
| **Docker Compose Location** | `ztpsneakers/docker-compose.yml` |
| **Base Directory** | `ztpsneakers` (jika repo root bukan di sini) |

> [!NOTE]
> Jika root repository Anda sudah langsung di folder `ztpsneakers/`, kosongkan **Base Directory**.

---

## Langkah 6 — Set Environment Variables

Di tab **"Environment Variables"**, tambahkan semua variabel berikut:

### Required Variables

```env
SECRET_KEY=<generate-panjang-random-string>
DEBUG=False
DB_NAME=db_ztpsneakers
DB_USER=postgres
DB_PASSWORD=<password-kuat-untuk-postgres>
```

### Payment & API Keys

```env
MIDTRANS_SERVER_KEY=Mid-server-xxxxxxxxxxxx
MIDTRANS_CLIENT_KEY=Mid-client-xxxxxxxxxxxx
MIDTRANS_IS_PRODUCTION=False
RAJAONGKIR_API_KEY=<your-rajaongkir-key>
```

> [!WARNING]
> `DB_HOST` **JANGAN** diisi di environment variables Coolify — sudah di-hardcode ke `db` di `docker-compose.yml` agar mengarah ke service PostgreSQL internal.

### Generate SECRET_KEY

Jalankan di terminal lokal:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## Langkah 7 — Konfigurasi Domain (Opsional)

Di tab **"Domains"**:

1. Klik **"Add Domain"**
2. Masukkan domain Anda: `https://ztpsneakers.yourdomain.com`
3. Coolify akan otomatis generate SSL certificate via Let's Encrypt
4. Update DNS record domain Anda:
   ```
   A   ztpsneakers   →   YOUR_SERVER_IP
   ```

> [!NOTE]
> Jika belum punya domain, Anda bisa akses via `http://YOUR_SERVER_IP:8000` terlebih dahulu.

---

## Langkah 8 — Konfigurasi Ports

Di tab **"Network"** atau **"Ports"**:

| Service | Container Port | Host Port |
|---------|---------------|-----------|
| web (Django) | `8000` | `8000` |

> [!TIP]
> Jika menggunakan domain + SSL, Coolify (via Traefik proxy) akan otomatis handle port 80/443 → 8000.

---

## Langkah 8.5 — Persistent Storage

### Apakah perlu setup tambahan?

**Tidak perlu setup tambahan.** `docker-compose.yml` sudah mendefinisikan 2 named volumes yang otomatis persisten di server:

| Volume | Mount Path di Container | Isi |
|--------|------------------------|-----|
| `postgres_data` | `/var/lib/postgresql/data` | Seluruh data database |
| `media_data` | `/app/media` | Gambar produk, banner, logo brand |

Named volumes ini **tidak akan dihapus saat redeploy** — data aman setiap kali push kode baru.

### Cara kerja media files saat deploy pertama

Karena folder `media/` ikut masuk ke Docker image (tidak di-exclude `.dockerignore`):

1. **Build image** → foto produk/banner/brand sudah ada di dalam image
2. **Container start pertama kali** → Docker otomatis copy isi `media/` dari image ke volume kosong `media_data`
3. **Seed berjalan** → gambar ditemukan di `/app/media/...` → berhasil dibuat di database
4. **Redeploy berikutnya** → volume sudah berisi data → tidak ditimpa ✅

### Verifikasi volume di server (opsional)

Setelah deploy, SSH ke server dan cek:

```bash
# Lihat semua volume Docker
docker volume ls

# Cek isi volume media
docker volume inspect ztpsneakers_media_data

# Masuk ke container untuk cek file
docker exec -it <nama_container_web> ls /app/media/products/images/
```

### Opsi: Gunakan Coolify UI Persistent Storage (bind mount)

Sebagai **alternatif lebih eksplisit** (tidak wajib), Coolify menyediakan UI untuk bind mount ke path tertentu di server:

1. Di service `web`, buka tab **"Storages"** atau **"Persistent Storage"**
2. Klik **"Add"**
3. Isi:
   - **Source Path (Host)**: `/data/coolify/ztpsneakers/media`
   - **Destination Path (Container)**: `/app/media`
4. Klik **Save**

> [!WARNING]
> Jika menggunakan bind mount via Coolify UI, **hapus** baris `- media_data:/app/media` dari `docker-compose.yml` terlebih dahulu agar tidak konflik. Gunakan salah satu cara — pilih named volume (sudah ada) **ATAU** bind mount UI, tidak keduanya.

> [!TIP]
> Untuk project ini, **named volume yang sudah ada di `docker-compose.yml` sudah cukup**. Tidak perlu konfigurasi tambahan di Coolify UI.

---

## Langkah 9 — Deploy!

1. Klik tombol **"Deploy"** (tombol biru/hijau di bagian atas)
2. Coolify akan mulai proses:
   - ✅ Clone repository
   - ✅ Build Docker image
   - ✅ Start container `db` (PostgreSQL)
   - ✅ Start container `web` (Django)
   - ✅ Jalankan `entrypoint.sh`:
     - Tunggu PostgreSQL ready
     - `python manage.py migrate`
     - `python manage.py collectstatic`
     - `python seed.py` (idempotent — skip data yang sudah ada)
     - Start Gunicorn

3. Monitor log di tab **"Logs"** real-time

---

## Langkah 10 — Buat Superuser Admin

Setelah deploy berhasil, buat akun admin Django melalui terminal container:

1. Di Coolify, pergi ke service `web`
2. Klik tab **"Terminal"** atau **"Execute Command"**
3. Jalankan:
   ```bash
   python manage.py createsuperuser
   ```
4. Isi username, email, dan password
5. Akses admin panel di: `https://yourdomain.com/admin/`

---

## Persistent Data — Media Files

Media files (foto produk, logo brand, banner) disimpan di **Docker Volume** bernama `media_data`:

```yaml
volumes:
  media_data:    # ← ini persistent, tidak hilang saat redeploy
```

> [!IMPORTANT]
> **Seed pertama kali:** Seed script hanya menyimpan **path referensi** ke database. File gambar fisik di folder `media/` di dalam repository akan di-copy ke dalam image saat build. Namun volume `media_data` yang dipersist adalah volume di server.
>
> **Solusi:** File gambar di folder `media/` sudah di-commit ke Git repository, sehingga saat build Docker image, file-file tersebut akan tersedia di `/app/media/` dan seed bisa berjalan normal.

---

## Redeploy (Update Code)

Setiap kali ada perubahan kode:

1. Push ke branch `main`
2. Coolify akan **otomatis detect** perubahan (jika auto-deploy aktif)
3. Atau klik manual **"Redeploy"** di dashboard

> [!TIP]
> Aktifkan **"Auto Deploy"** di settings Coolify agar setiap `git push` otomatis trigger deployment.

Data database dan media **tidak akan hilang** karena menggunakan named volumes.

---

## Troubleshooting

### ❌ Container `web` gagal start

Cek log di Coolify → tab "Logs". Penyebab umum:

```bash
# 1. Variabel lingkungan belum diset
EnvironmentError: SECRET_KEY not found

# Solusi: Tambahkan SECRET_KEY di Environment Variables Coolify

# 2. Database belum ready (biasanya teratasi otomatis oleh health check)
# Entrypoint sudah handle wait loop — tunggu beberapa menit
```

### ❌ Static files tidak muncul (CSS/JS rusak)

```bash
# Pastikan collectstatic berhasil — cek log entrypoint
# Juga pastikan whitenoise terkonfigurasi di settings.py:
# MIDDLEWARE = ['whitenoise.middleware.WhiteNoiseMiddleware', ...]
```

### ❌ Gambar produk tidak muncul

```bash
# Periksa volume media_data sudah ter-mount:
# web → volumes → media_data:/app/media

# Pastikan file gambar ada di repository di folder:
# ztpsneakers/media/products/images/
# ztpsneakers/media/brands/logos/
# ztpsneakers/media/banners/
```

### ❌ `502 Bad Gateway`

```bash
# Gunicorn belum start atau crash
# Cek log container web
# Pastikan port 8000 sudah dibuka di firewall server
```

---

## Checklist Final Sebelum Deploy

- [ ] File `Dockerfile`, `docker-compose.yml`, `entrypoint.sh` sudah di-commit
- [ ] File `.env` **tidak** di-commit ke Git
- [ ] `requirements.txt` mengandung `gunicorn`
- [ ] Environment variables sudah diset di Coolify
- [ ] `SECRET_KEY` sudah di-generate (bukan yang default)
- [ ] `DEBUG=False` di production
- [ ] `DB_PASSWORD` menggunakan password yang kuat
- [ ] Domain (jika ada) sudah diarahkan ke IP server
- [ ] Superuser sudah dibuat setelah deploy pertama

---

## Referensi

- [Coolify Documentation](https://coolify.io/docs)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)
- [Gunicorn Configuration](https://docs.gunicorn.org/en/stable/configure.html)
- [WhiteNoise Documentation](https://whitenoise.readthedocs.io/)
