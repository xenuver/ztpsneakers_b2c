# PRD — ZTP Sneakers B2C Platform

> **Versi:** 1.0  
> **Tanggal:** 2026  
> **Author:** Wahyu Ahmad Cahyadi (221103805)  
> **Stack:** Django 5.x + HTMX 2.x + Tailwind CSS 3.x + PostgreSQL  
> **Hosting:** Shared Hosting (cPanel/Niagahoster) + WhatsApp/Crisp Chat  
> **Referensi Visual:** 807garage.com (dark, premium, street culture aesthetic)

---

## 1. Latar Belakang & Tujuan

ZTP Sneakers adalah UMKM penjual sepatu second berbasis di Pontianak yang selama ini mengandalkan Instagram dan tatap muka langsung. Masalah utama:

- Pelanggan harus chat manual untuk cek stok, warna, dan ukuran
- Produk terjual tidak dihapus dari Instagram → penumpukan konten
- Tidak ada sistem tracking pesanan
- Jangkauan terbatas ke Pontianak saja

**Tujuan platform:** menghasilkan website B2C yang memfasilitasi penjualan digital, interaksi pelanggan, dan layanan purna jual melalui lima konsep e-commerce: **Automation, Integration, Interaction, Publication, Transaction**.

---

## 2. Pengguna & Role

| Role | URL | Deskripsi |
|---|---|---|
| **Customer** | `/` | Pengunjung & pembeli terdaftar |
| **Admin Toko** | `/admin-toko/` | Staf operasional, akses terbatas |
| **Jasmine (Owner)** | `/jasmine/` | Pemilik, full access, dashboard premium |

---

## 3. Catatan Hosting (Shared Hosting)

Karena menggunakan **shared hosting (cPanel)**, beberapa penyesuaian wajib:

- Gunakan **Passenger WSGI** untuk deploy Django (bukan Gunicorn standalone)
- Database: **MySQL** (bukan PostgreSQL) — shared hosting umumnya tidak sediakan PostgreSQL. Gunakan `mysqlclient` atau `django-mysql`
- Static files: upload ke `public_html/static/` via cPanel File Manager atau FTP
- Media files: simpan di `public_html/media/`
- Gunakan `.htaccess` untuk routing ke Passenger
- **RajaOngkir:** panggil dari backend Django (server-side request), bukan dari frontend, agar API key tidak exposed
- **Midtrans:** gunakan mode `Sandbox` selama development, `Production` setelah go-live
- **Crisp:** embed widget JS di `base.html` — tidak perlu backend integration khusus
- **Email:** gunakan SMTP dari cPanel (Roundcube) atau Gmail SMTP + App Password
- Hindari Celery/Redis (tidak tersedia di shared hosting) — gunakan **django-apscheduler** atau cron job cPanel untuk task berkala

---

## 4. Modul & Fitur Lengkap

### 4.1 Storefront (Customer-Facing)

#### Auth & Profil
- Register + Login satu halaman (tab toggle, HTMX)
- Google OAuth via django-allauth
- Lupa password via email OTP
- Halaman profil: edit biodata, ganti password, riwayat pesanan

#### Katalog & Produk
- Hero carousel full-width (auto-slide, dark overlay, numbered bullets)
- Trust badge strip: Garansi Puas · 7 Hari Return · Free Ongkir · 100% Authentic · Koleksi Terlengkap
- Grid produk: 4 kolom desktop / 2 kolom mobile
- Filter: brand, ukuran, harga (range slider), kondisi
- Sort: terbaru, terlaris, harga terendah/tertinggi
- HTMX live search (tanpa reload)
- Produk card: foto besar, nama, harga, badge (NEW/SOLD OUT)
- Detail produk: galeri swipe, pilih ukuran, stok real-time, tab deskripsi/ulasan/garansi

#### Wishlist
- Tambah/hapus wishlist via HTMX (tanpa reload)
- Halaman `/wishlist/` — grid produk tersimpan
- Notifikasi jika produk di wishlist hampir habis stok

#### Keranjang & Checkout
- Persistent cart (session + database untuk user login)
- Update qty, hapus item via HTMX
- Checkout multi-step: Alamat → Pengiriman → Pembayaran → Konfirmasi
- Autocomplete alamat (Kelurahan/Kecamatan API atau input manual)
- Kalkulasi ongkir otomatis via **RajaOngkir API** (JNE, POS, TIKI)
- Pilih layanan ekspedisi (REG, YES, OKE)
- Pembayaran via **Midtrans Snap**: Virtual Account (BCA, Mandiri, BNI), DANA, OVO, GoPay

#### Pesanan
- Halaman riwayat pesanan dengan status badge
- Status: `Menunggu Pembayaran → Dibayar → Diproses → Dikirim → Selesai → Dibatalkan`
- Detail pesanan: item, total, resi, ekspedisi
- Update status pengiriman dikelola admin (input resi manual)
- Email notifikasi otomatis setiap perubahan status

#### Layanan Purna Jual *(sesuai skripsi — lihat Seksi 5)*
- Ulasan & rating produk (hanya setelah order status "Selesai")
- Form laporan kendala/garansi produk
- Live Chat via **Crisp** (seluruh halaman)
- Notifikasi email after-sales

#### Rekomendasi Produk
- Berdasarkan rating produk tertinggi (simple recommendation)
- Ditampilkan di: halaman detail produk ("Produk Terkait"), homepage ("Pilihan Untukmu")

---

### 4.2 Admin Toko (Staf — Akses Terbatas)

URL: `/admin-toko/` | Django permission group: `AdminToko`

| Modul | Boleh | Tidak Boleh |
|---|---|---|
| Produk | Tambah, edit, nonaktifkan | Hapus permanen, kelola kategori |
| Stok | Update stok per ukuran | — |
| Pesanan | Lihat, proses, input resi, update status | Override pembayaran, refund |
| Pelanggan | Lihat profil, riwayat beli | Edit data, hapus akun |
| Ulasan | Moderasi (tampilkan/sembunyikan) | Hapus permanen |
| Laporan Garansi | Lihat & update status laporan | — |
| Laporan Penjualan | Lihat saja | Export |
| Crisp Chat | Balas dari inbox Crisp | — |

---

### 4.3 Jasmine — Owner Dashboard (Full Access)

URL: `/jasmine/` | Django permission: `is_staff=True` + group `Owner`

| Modul | Fitur Lengkap |
|---|---|
| Dashboard | KPI cards (revenue, orders, customers baru, produk terlaris) + sparkline charts |
| Analytics | Grafik penjualan harian/bulanan/tahunan, produk terlaris, sumber traffic |
| Produk | CRUD lengkap: produk, kategori, banner homepage |
| Pengguna | Buat/suspend/atur permission akun Admin Toko |
| Pesanan | Semua pesanan, override status, tandai masalah |
| Garansi | Lihat semua laporan garansi, update resolusi, eskalasi |
| Laporan | Export Excel (openpyxl), filter bulan-tahun |
| Pengaturan | Token Crisp, konfigurasi Midtrans, teks & logo toko, SMTP email |

---

## 5. Layanan Purna Jual (After-Sales Service)

> Sesuai skripsi: *"Layanan garansi pada sistem ini dibatasi sebatas fitur komunikasi pelaporan kendala produk. Sistem pengembalian dana secara otomatis melalui website tidak termasuk ke dalam lingkup pengerjaan sistem."* — Batasan Masalah, BAB 1

### 5.1 Komponen Purna Jual

#### A. Ulasan & Rating Produk
- Trigger: order status berubah ke `Selesai` → email dikirim ke customer dengan link ulasan
- Form ulasan: rating bintang 1–5 + komentar teks + foto opsional (maks 3 foto)
- Satu ulasan per item per order
- Ulasan tampil di halaman detail produk, rata-rata bintang di card produk
- Admin dapat moderasi (sembunyikan) ulasan yang tidak pantas

#### B. Form Laporan Kendala / Garansi
- Tersedia di: halaman detail pesanan (untuk order yang sudah `Selesai`)
- Field: pilih item bermasalah, kategori masalah (cacat produk / salah ukuran / tidak sesuai foto / lainnya), deskripsi, foto bukti (maks 5 foto)
- Status laporan: `Diterima → Ditinjau → Diselesaikan / Ditolak`
- Notifikasi email ke pelanggan setiap perubahan status
- Admin/Jasmine dapat tulis catatan resolusi yang dilihat pelanggan

#### C. Live Chat (Crisp)
- Widget Crisp tertanam di seluruh halaman storefront
- Untuk pertanyaan produk, status pesanan, dan laporan masalah cepat
- Admin Toko dapat balas dari Crisp Inbox
- Jasmine dapat lihat semua percakapan dari dashboard Crisp

#### D. Notifikasi Email After-Sales
- Email "Terima kasih telah berbelanja" + ajakan ulasan (7 hari setelah `Selesai`)
- Email update status laporan garansi
- Semua email menggunakan template HTML branded ZTP Sneakers

### 5.2 Model Data Purna Jual

```
Review
  - id, order_item (FK), customer (FK)
  - rating (1–5), komentar, foto[]
  - is_visible (bool), created_at

GaransiLaporan
  - id, order_item (FK), customer (FK)
  - kategori (choices), deskripsi, foto[]
  - status (diterima/ditinjau/diselesaikan/ditolak)
  - catatan_resolusi (admin), created_at, updated_at
```

---

## 6. Stack Teknis

```
Backend:    Python 3.12 + Django 5.x
Frontend:   HTMX 2.x + Tailwind CSS 3.x (CDN play di dev, build di prod)
Database:   MySQL 8.x (shared hosting compatible)
Auth:       django-allauth (email + Google OAuth)
Payment:    Midtrans Snap SDK (python-midtransclient)
Shipping:   RajaOngkir API (server-side, key di .env)
Chat:       Crisp Chat widget JS
Export:     openpyxl (Excel)
Email:      Django email + SMTP (cPanel/Gmail)
Deploy:     Shared Hosting cPanel + Passenger WSGI
Static:     WhiteNoise atau cPanel File Manager
```

---

## 7. Design System (Referensi 807garage.com)

```css
/* Warna Utama */
--bg-base:       #0D0D0D;   /* near-black, dominant */
--bg-surface:    #1A1A1A;   /* card surface */
--bg-elevated:   #222222;   /* hover state */
--border:        #2A2A2A;
--text-primary:  #F5F5F5;
--text-muted:    #A0A0A0;
--accent:        #E8FF00;   /* neon yellow — sneaker culture CTA */
--accent-red:    #FF3B30;   /* flash sale / badge */
--success:       #22C55E;
--warning:       #F59E0B;

/* Typography */
--font-display:  'Space Grotesk', sans-serif;  /* heading bold */
--font-body:     'Inter', sans-serif;

/* Layout */
--max-width:     1440px;
--radius-card:   8px;
--radius-btn:    6px;
```

**Pola UI dari 807garage yang diterapkan:**
- Hero carousel full-width dengan overlay gelap + teks bold putih besar
- Trust badge strip horizontal langsung di bawah hero (ikon + teks singkat)
- Product card: foto dominan, nama kecil di bawah, harga dengan accent color
- Navbar sticky: logo kiri, nav tengah, search + cart + avatar kanan
- Filter by brand sebagai navigasi utama dengan tombol pill aktif
- Hover product card: scale(1.02) + subtle border accent
- CTA button: background accent (`#E8FF00`) + teks hitam bold

---

## 8. Batasan Sistem (sesuai skripsi)

- Tidak ada aplikasi mobile (Android/iOS)
- Tidak ada tracking pengiriman real-time (hanya update status manual)
- Tidak ada refund otomatis (laporan garansi = komunikasi manual)
- Tidak ada migrasi data historis penjualan fisik sejak 2022
- Keamanan transaksi sepenuhnya via Midtrans
