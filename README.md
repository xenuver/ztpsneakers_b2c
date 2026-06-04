# 👟 ZTP Sneakers — Platform E-Commerce B2C



<p align="center">
  <strong>Platform penjualan sepatu second (preloved) berbasis web untuk UMKM ZTP Sneakers, Pontianak.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Django-5.2-092E20?style=for-the-badge&logo=django&logoColor=white">
  <img src="https://img.shields.io/badge/HTMX-2.x-3466CC?style=for-the-badge&logo=htmx&logoColor=white">
  <img src="https://img.shields.io/badge/Tailwind_CSS-3.x-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white">
  <img src="https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/PostgreSQL-16-4169E1?style=for-the-badge&logo=postgresql&logoColor=white">
</p>

---

## 📋 Daftar Isi

- [Tentang Proyek](#-tentang-proyek)
- [Fitur Utama](#-fitur-utama)
- [Role Pengguna](#-role-pengguna)
- [Daftar Halaman](#-halaman--screenshot)
  - [Storefront (Customer)](#storefront-customer)
  - [Admin Toko](#admin-toko-staf)
  - [Jasmine Dashboard (Owner)](#jasmine-dashboard-owner)
- [Stack Teknologi](#-stack-teknologi)
- [Struktur Proyek](#-struktur-proyek)
- [Cara Instalasi Lokal](#-cara-instalasi-lokal)
  - [Windows](#windows)
  - [macOS](#macos)
- [Konfigurasi Environment](#-konfigurasi-environment)
- [Menjalankan Aplikasi](#-menjalankan-aplikasi)
- [Informasi Proyek](#-informasi-proyek)

---

## 🏪 Tentang Proyek

**ZTP Sneakers** adalah platform B2C (Business-to-Consumer) yang dikembangkan untuk memdigitalisasi operasional penjualan UMKM ZTP Sneakers — sebuah toko sepatu second/preloved yang berbasis di Pontianak, Kalimantan Barat.

Sebelumnya, ZTP Sneakers mengandalkan Instagram dan transaksi tatap muka. Platform ini hadir untuk menyelesaikan permasalahan operasional utama:

| Masalah Lama | Solusi Platform |
|---|---|
| Pelanggan harus chat manual untuk cek stok | Katalog real-time dengan filter ukuran & ketersediaan |
| Produk terjual tidak dihapus dari Instagram | Status produk otomatis (SOLD OUT badge) |
| Tidak ada sistem tracking pesanan | Timeline status pesanan lengkap |
| Jangkauan terbatas ke Pontianak | Platform online dengan pengiriman nasional via RajaOngkir |
| Tidak ada layanan purna jual terstruktur | Sistem ulasan, laporan garansi, dan live chat |

Platform ini dibangun mengikuti lima konsep e-commerce modern: **Automation, Integration, Interaction, Publication, Transaction**.

---

## ✨ Fitur Utama

### 🛍️ Storefront (Customer)

- **Hero Carousel** — Slideshow full-width auto-slide 5 detik dengan overlay gelap dan CTA button
- **Trust Badge Strip** — Banner kepercayaan: Garansi Puas · 7 Hari Return · Free Ongkir · 100% Authentic · Koleksi Terlengkap
- **Katalog Produk** — Grid 4 kolom (desktop) / 2 kolom (mobile) dengan infinite scroll
- **Live Search** — Pencarian real-time tanpa reload halaman (HTMX, debounce 300ms)
- **Filter & Sort** — Filter by brand, ukuran, kondisi, range harga; sort terbaru/terlaris/harga
- **Detail Produk** — Galeri foto swipe, pilih ukuran, stok real-time, tab deskripsi/ulasan/garansi
- **Wishlist** — Simpan produk favorit, notifikasi stok menipis
- **Keranjang Belanja** — Persistent cart, update qty tanpa reload (HTMX)
- **Checkout Multi-Step** — Alamat → Pengiriman → Pembayaran
- **Kalkulasi Ongkir** — Otomatis via RajaOngkir API (JNE, POS, TIKI)
- **Pembayaran Midtrans** — Virtual Account (BCA, Mandiri, BNI), DANA, OVO, GoPay
- **Riwayat Pesanan** — Status timeline lengkap dengan filter tab
- **Ulasan & Rating** — Review bintang + foto, hanya bisa setelah order selesai
- **Laporan Garansi** — Form laporan kendala produk dengan tracking status
- **Live Chat Crisp** — Widget chat di seluruh halaman
- **Notifikasi Email** — Email otomatis setiap perubahan status pesanan

### 🔐 Auth & Profil

- Register + Login di satu halaman (tab toggle, HTMX)
- Google OAuth via django-allauth
- Lupa password via email OTP
- Halaman profil: edit biodata, ganti password, riwayat pesanan

### 🖥️ Admin Toko (Staf)

- Dashboard ringkas: pesanan hari ini, stok menipis, garansi baru
- Manajemen produk: tambah, edit, nonaktifkan
- Manajemen pesanan: proses, input nomor resi, update status
- Lihat data pelanggan & riwayat pembelian
- Moderasi ulasan pelanggan
- Penanganan laporan garansi

### 👑 Jasmine Dashboard (Owner)

- **KPI Cards** — Revenue, total pesanan, customer baru, produk terlaris dengan sparkline chart
- **Analytics** — Grafik penjualan harian/bulanan/tahunan (Chart.js)
- **CRUD Lengkap** — Produk, kategori, brand, banner homepage
- **Manajemen Pengguna** — Buat/suspend akun Admin Toko
- **Override Pesanan** — Tandai masalah, override status
- **Export Laporan** — Download Excel (.xlsx) dengan filter bulan-tahun
- **Pengaturan Toko** — Konfigurasi Midtrans, Crisp token, SMTP email

---

## 👤 Role Pengguna

| Role | URL | Deskripsi | Akses |
|---|---|---|---|
| **Customer** | `/` | Pengunjung & pembeli terdaftar | Katalog, cart, checkout, pesanan, wishlist, ulasan, garansi |
| **Admin Toko** | `/admintoko/` | Staf operasional | Kelola produk, pesanan, ulasan, garansi (terbatas) |
| **Django Admin** | `/admin/` | Superuser / Developer | Full Django admin (Jazzmin UI) |

---

## 📸 Daftar Halaman


### Storefront (Customer)

#### 🏠 Homepage — `/`

Halaman utama dengan hero carousel, trust badge strip, produk featured, dan rekomendasi produk berdasarkan rating tertinggi.



**Komponen:**
- Hero carousel full-width (auto-slide, numbered bullets, CTA "Lihat Koleksi")
- Trust badge strip horizontal: ikon + teks singkat
- Section "KOLEKSI TERPILIH" — produk is_featured=True
- Section "PILIHAN UNTUKMU" — produk rating tertinggi

---

#### 🗂️ Katalog — `/katalog/`

Halaman semua produk dengan filter sidebar, live search, dan infinite scroll.



**Komponen:**
- Filter sidebar: brand, ukuran (pill), kondisi, harga (range slider), reset filter
- Search bar HTMX live (debounce 300ms)
- Sort: Terbaru, Terlaris, Harga ↑, Harga ↓
- Grid produk 4 kolom (desktop) / 2 kolom (mobile)
- Infinite scroll via HTMX `hx-trigger="revealed"`

---

#### 👟 Detail Produk — `/produk/[slug]/`

Halaman lengkap informasi produk dengan galeri foto, pilih ukuran, dan tab informasi.



**Komponen:**
- Galeri foto swipe + thumbnail row (klik ganti foto utama)
- Info produk: brand badge, nama (h1), rating bintang, harga, pilih ukuran, stok real-time
- Tombol "Tambah ke Keranjang" & "Simpan ke Wishlist" (HTMX)
- Tab: Deskripsi | Ulasan (n) | Garansi & Return
- Section produk terkait (brand sama, 4 card)

---

#### 🔐 Auth — `/auth/`

Halaman login dan registrasi dalam satu halaman dengan tab toggle.



**Komponen:**
- Layout split screen: foto lifestyle (kiri) + form area (kanan)
- Tab toggle: Masuk / Daftar
- Login dengan Google OAuth
- Link "Lupa Password?"

---

#### ❤️ Wishlist — `/wishlist/`

Daftar produk yang disimpan oleh customer.



**Komponen:**
- Grid produk tersimpan
- Tombol hapus dari wishlist (HTMX, tanpa reload)
- Notifikasi jika produk hampir habis stok
- Empty state dengan ilustrasi

---

#### 🛒 Keranjang — `/cart/`

Ringkasan item yang akan dibeli sebelum checkout.



**Komponen:**
- List item: foto, nama, ukuran, harga satuan
- Update qty dan hapus item (HTMX)
- Ringkasan total harga
- Tombol "Checkout"

---

#### 💳 Checkout — `/checkout/`

Proses checkout tiga langkah.



**Step 1 — Alamat:**
- Form: nama penerima, no. telepon
- Dropdown chained: Provinsi → Kota → Kecamatan (HTMX)
- Alamat detail, kode pos

**Step 2 — Pengiriman:**
- Loading spinner saat kalkulasi RajaOngkir
- List opsi ekspedisi: JNE, POS, TIKI dengan harga dan estimasi

**Step 3 — Pembayaran:**
- Ringkasan order: item, subtotal, ongkir, total
- Tombol "Bayar Sekarang" → trigger Midtrans Snap popup

---

#### ✅ Sukses Pembayaran — `/checkout/success/`

Halaman konfirmasi setelah pembayaran berhasil.



---

#### 📦 Riwayat Pesanan — `/orders/`

Daftar semua pesanan customer dengan filter status.



**Komponen:**
- Tab filter: Semua | Menunggu Bayar | Diproses | Dikirim | Selesai
- Card per order: nomor order, tanggal, thumbnail produk, total, status badge
- Tombol "Lihat Detail" dan "Bayar Sekarang" (jika masih pending)

---

#### 📋 Detail Pesanan — `/orders/[id]/`

Detail lengkap satu pesanan dengan timeline status dan aksi purna jual.



**Komponen:**
- Status timeline horizontal: Dibayar → Diproses → Dikirim → Selesai
- Info pengiriman: nama, alamat, ekspedisi, nomor resi
- Daftar item yang dibeli
- Ringkasan biaya: subtotal, ongkir, total
- Tombol kondisional: "Pesanan Diterima", "Tulis Ulasan", "Laporkan Masalah"

---

#### ⭐ Form Ulasan — `/orders/review/[id]/`

Form penulisan ulasan produk setelah pesanan selesai.



**Komponen:**
- Rating bintang interaktif (klik 1–5)
- Textarea komentar
- Upload foto bukti (drag & drop, max 3 foto, preview thumbnail)

---

#### ⚠️ Form Laporan Garansi — `/orders/garansi/[id]/`

Form pelaporan kendala/masalah produk.



**Komponen:**
- Dropdown pilih item bermasalah
- Kategori masalah: Cacat Produk / Salah Ukuran / Tidak Sesuai Foto / Lainnya
- Deskripsi masalah (textarea min 50 karakter)
- Upload foto bukti (max 5 foto, min 1 wajib)

---

#### 🔍 Tracking Garansi — `/orders/garansi/tracking/[id]/`

Halaman pelacakan status laporan garansi.



**Komponen:**
- Status badge + tanggal setiap perubahan
- Catatan resolusi dari admin (jika ada)
- Tombol "Chat dengan CS" (buka Crisp)

---

#### 👤 Profil — `/profile/`

Halaman pengelolaan akun customer.



**Komponen:**
- Edit biodata: nama, email, nomor telepon, avatar
- Ganti password
- Tab riwayat pesanan singkat

---

### Admin Toko (Staf)

> URL: `/admin-toko/` | Akses dengan akun group `AdminToko`

#### 📊 Dashboard Admin — `/admin-toko/`



KPI hari ini: pesanan masuk, stok menipis, laporan garansi baru. Tabel pesanan terbaru dengan aksi cepat.

---

#### 📦 Daftar Produk — `/admin-toko/products/`



Tabel produk dengan filter, pencarian, tombol tambah/edit/nonaktifkan.

---

#### ➕ Form Produk — `/admin-toko/products/add/`



Form lengkap tambah/edit produk: nama, brand, kategori, harga, kondisi, foto, stok per ukuran.

---

#### 🏷️ Brand & Kategori



Manajemen daftar brand dan kategori produk.

---

#### 🛒 Pesanan — `/admin-toko/orders/`



Tabel semua pesanan dengan filter status, tombol proses, input resi pengiriman, dan update status.

---

#### 👥 Pelanggan — `/admin-toko/customers/`



Daftar pelanggan terdaftar dengan riwayat pembelian. (Read-only)

---

#### 💬 Ulasan — `/admin-toko/reviews/`



Moderasi ulasan pelanggan: tampilkan/sembunyikan ulasan yang tidak pantas.

---

#### 🛡️ Laporan Garansi — `/admin-toko/warranty/`



Daftar laporan garansi masuk dengan update status dan penulisan catatan resolusi.

---

### Jasmine Dashboard (Owner)

> URL: `/jasmine/` | Akses dengan akun `is_staff=True` + group `Owner`

#### 📈 Dashboard Jasmine — `/jasmine/`



**Komponen:**
- Greeting section: nama owner + tanggal hari ini
- 4 KPI Cards dengan sparkline: Revenue Bulan Ini, Total Pesanan, Customer Baru, Produk Terlaris
- Grafik penjualan Chart.js (toggle: Harian / Bulanan / Tahunan)
- Tabel produk terlaris: foto, nama, terjual, revenue, stok

---

#### 📊 Export Laporan — `/jasmine/export/`



Filter laporan per bulan/tahun, preview tabel, dan download langsung file `.xlsx` (openpyxl).

---

## 🛠️ Stack Teknologi

| Layer | Teknologi |
|---|---|
| **Backend** | Python 3.12 + Django 5.2 |
| **Frontend** | HTMX 2.x + Tailwind CSS 3.x (CDN) |
| **Database** | PostgreSQL 16 |
| **Auth** | django-allauth (email + Google OAuth) |
| **Payment** | Midtrans Snap (python-midtransclient) |
| **Shipping** | RajaOngkir API (server-side) |
| **Admin UI** | Jazzmin (Django Admin tema premium) |
| **HTMX Helper** | django-htmx + django-widget-tweaks |
| **Export** | openpyxl (Excel .xlsx) |
| **Email** | Console (dev) / SMTP Gmail (prod) |
| **Static Files** | WhiteNoise (middleware) |
| **Deploy Target** | Shared Hosting cPanel + Passenger WSGI |

---

## 📁 Struktur Proyek

```
ztpsneakers/
├── admintoko/          # App: panel admin toko (staf)
├── aftersales/         # App: ulasan & laporan garansi
├── core/               # App: halaman utama, homepage, katalog
├── docs/               # Dokumentasi proyek
│   ├── PRD.md
│   ├── TASK.md
│   ├── UIUX_FLOW.md
│   └── screenshots/    # Screenshot halaman (isi manual)
├── orders/             # App: cart, checkout, pesanan
├── products/           # App: model produk, brand, kategori
├── storefront/         # App: views storefront customer-facing
├── templates/          # HTML templates (Django)
│   ├── admintoko/      # Template admin toko
│   ├── jasmine/        # Template dashboard owner
│   ├── orders/         # Template pesanan & checkout
│   ├── storefront/     # Template halaman customer
│   └── userauths/      # Template auth & profil
├── userauths/          # App: auth, profil, Google OAuth
├── ztpsneakers/        # Django project settings
├── static/             # Static files (CSS, JS, images)
├── media/              # File upload (foto produk, ulasan)
├── manage.py
├── requirements.txt
├── seed.py             # Script seeder data awal
├── .env.example        # Template environment variables (aman di-commit)
└── .env                # Environment aktual kamu (JANGAN di-commit!)
```

---

## 💻 Cara Instalasi Lokal

### Prasyarat

Pastikan sudah terinstall:
- **Python 3.12+**
- **pip** (sudah bundled dengan Python)
- **Git**
- **PostgreSQL 16+** (download di https://www.postgresql.org/download/)
- **venv** (built-in Python, tidak perlu install tambahan)

---

### Windows

#### 1. Clone Repository

```powershell
git clone https://github.com/[username]/ztpsneakers.git
cd ztpsneakers
```

#### 2. Buat Virtual Environment

```powershell
python -m venv venv
venv\Scripts\activate
```

> Jika muncul error policy di PowerShell, jalankan dulu:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

#### 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

#### 4. Setup Database PostgreSQL

Buka **pgAdmin** atau jalankan via **psql** command line:

```sql
CREATE DATABASE db_ztpsneakers;
```

Atau via PowerShell:

```powershell
psql -U postgres -c "CREATE DATABASE db_ztpsneakers;"
```

#### 5. Konfigurasi Environment

Salin file template ke `.env` lalu isi nilainya:

```powershell
copy .env.example .env
```

Buka `.env` dengan editor (VS Code, Notepad, dll.) dan isi semua nilai yang bertanda `<...>`:

```powershell
code .env
```

Lihat detail setiap variabel di bagian [Konfigurasi Environment](#-konfigurasi-environment) di bawah.

#### 6. Jalankan Migrasi

```powershell
python manage.py migrate
```

#### 7. (Opsional) Isi Data Awal

```powershell
python seed.py
```

#### 8. Buat Superuser

```powershell
python manage.py createsuperuser
```

#### 9. Jalankan Server Development

```powershell
python manage.py runserver
```

Buka browser dan akses: **http://127.0.0.1:8000**

---

### macOS

#### 1. Clone Repository

```bash
git clone https://github.com/[username]/ztpsneakers.git
cd ztpsneakers
```

#### 2. Buat Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

> **Catatan:** Jika ada error saat install `psycopg2`, gunakan versi binary:
>
> ```bash
> pip install psycopg2-binary
> ```

#### 4. Setup Database PostgreSQL

Install PostgreSQL via Homebrew jika belum ada:

```bash
brew install postgresql@16
brew services start postgresql@16
```

Buat database:

```bash
psql -U postgres -c "CREATE DATABASE db_ztpsneakers;"
```

#### 5. Konfigurasi Environment

Salin file template ke `.env` lalu isi nilainya:

```bash
cp .env.example .env
```

Buka `.env` dengan editor dan isi semua nilai yang bertanda `<...>`:

```bash
code .env
# atau
nano .env
```

Lihat detail setiap variabel di bagian [Konfigurasi Environment](#-konfigurasi-environment) di bawah.

#### 6. Jalankan Migrasi

```bash
python manage.py migrate
```

#### 7. (Opsional) Isi Data Awal

```bash
python seed.py
```

#### 8. Buat Superuser

```bash
python manage.py createsuperuser
```

#### 9. Jalankan Server Development

```bash
python manage.py runserver
```

Buka browser dan akses: **http://127.0.0.1:8000**

---

## ⚙️ Konfigurasi Environment

File [`.env.example`](.env.example) sudah tersedia di repository. Salin dan isi nilainya:

```bash
# Windows
copy .env.example .env

# macOS / Linux
cp .env.example .env
```

Berikut penjelasan setiap variabel:

```env
# ==========================================
# DJANGO CORE
# ==========================================
SECRET_KEY=your-secret-key-ganti-dengan-string-random-panjang
DEBUG=True

# ==========================================
# DATABASE (PostgreSQL)
# ==========================================
DB_NAME=db_ztpsneakers
DB_USER=postgres
DB_PASSWORD=your_postgres_password
DB_HOST=localhost
DB_PORT=5432

# ==========================================
# MIDTRANS PAYMENT GATEWAY
# ==========================================
MIDTRANS_SERVER_KEY=Mid-server-xxxxxxxxxxxx
MIDTRANS_CLIENT_KEY=Mid-client-xxxxxxxxxxxx
MIDTRANS_IS_PRODUCTION=False

# ==========================================
# RAJAONGKIR API (Kalkulasi Ongkir)
# ==========================================
RAJAONGKIR_API_KEY=your_rajaongkir_api_key
```

> **Catatan Email:** Saat `DEBUG=True`, semua email otomatis dicetak ke **terminal/console** saja (tidak dikirim sungguhan). Untuk production, ubah `DEBUG=False` dan tambahkan konfigurasi SMTP di `settings.py`.

> **⚠️ Penting:** Jangan pernah commit file `.env` ke repository! File ini sudah terdaftar di `.gitignore`.

---

## 🚀 Menjalankan Aplikasi

### Development

```bash
# Windows
python manage.py runserver

# macOS/Linux
python3 manage.py runserver
```

### Akses Panel Admin

| Panel | URL | Keterangan |
|---|---|---|
| Storefront | http://127.0.0.1:8000 | Halaman publik customer |
| Admin Toko | http://127.0.0.1:8000/admintoko/ | Login akun group `AdminToko` |
| Django Admin (Jazzmin) | http://127.0.0.1:8000/admin/ | Login superuser |

### Perintah Berguna

```bash
# Membuat dan menjalankan migrasi
python manage.py makemigrations
python manage.py migrate

# Mengumpulkan static files (untuk production)
python manage.py collectstatic

# Membuat superuser baru
python manage.py createsuperuser

# Mengisi data awal (seeder)
python seed.py

# Membuka Django shell
python manage.py shell
```

---
