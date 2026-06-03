# TASK LIST — ZTP Sneakers B2C Platform

> Metode: RAD (Rapid Application Development)  
> Setiap sprint ≈ 1–2 minggu  
> Wajib baca `PRD.md` dan `UIUX_FLOW.md` sebelum mengerjakan task apapun

---

## Sprint 0 — Setup & Persiapan Hosting

### Environment & Project
- [ ] Install Python 3.12 di shared hosting via cPanel Python App
- [x] Buat virtual environment + install dependencies
- [x] Setup Django 5.x project dengan struktur multi-app:
  ```
  ztpsneakers/
  ├── config/          # settings, urls, wsgi
  ├── apps/
  │   ├── storefront/  # customer-facing
  │   ├── admin_toko/  # staff panel
  │   ├── jasmine/     # owner dashboard
  │   ├── accounts/    # custom user model
  │   ├── products/    # produk, kategori, stok
  │   ├── orders/      # pesanan, cart, checkout
  │   ├── aftersales/  # ulasan, garansi, notifikasi
  │   └── core/        # utils, mixins, base templates
  ├── static/
  ├── media/
  ├── templates/
  └── manage.py
  ```
- [x] Konfigurasi Tailwind CSS via CDN (play.min.js untuk dev)
- [x] Setup HTMX 2.x via CDN
- [x] Konfigurasi WhiteNoise untuk static files
- [x] Buat `.env` file dengan semua secrets (Django secret key, DB creds, API keys)
- [x] Setup `requirements.txt` yang shared-hosting-compatible:
  ```
  Django>=5.0
  mysqlclient
  django-allauth
  htmx
  whitenoise
  python-midtransclient
  requests (untuk RajaOngkir)
  openpyxl
  django-apscheduler (ganti Celery)
  Pillow
  ```
- [ ] Konfigurasi Passenger WSGI (`passenger_wsgi.py`) untuk deploy
- [ ] Test deployment dummy ke shared hosting

---

## Sprint 1 — Custom User Model & Auth System

### Models
- [x] Buat `CustomUser` model (extend AbstractUser):
  - `phone_number`, `address`, `avatar`, `role` (customer/admin_toko/owner)
- [x] Buat `UserProfile` model untuk data tambahan pelanggan

### Auth Pages (Dark Theme — 807 Style)
- [x] Halaman `/auth/` — Register + Login dalam satu halaman (tab toggle via HTMX)
  - Form register: nama, email, password, konfirmasi password
  - Form login: email, password + "Ingat Saya"
  - Tab switch tanpa reload (HTMX `hx-swap`)
- [x] Google OAuth via `django-allauth` — tombol "Masuk dengan Google"
- [ ] Lupa password — flow: email input → OTP/link → reset password
- [x] Redirect setelah login: customer → `/`, admin toko → `/admin-toko/`, owner → `/jasmine/`
- [ ] Setup Django Permission Groups: `AdminToko`, `Owner`
- [x] Buat `OwnerRequiredMixin` dan `AdminTokoRequiredMixin`
- [/] Halaman profil customer: edit nama, telepon, alamat default, ganti password, avatar

---

## Sprint 2 — Product Models & Storefront Katalog

### Models
- [ ] Model `Category`: nama, slug, icon, urutan
- [ ] Model `Brand`: nama, slug, logo
- [ ] Model `Product`:
  - nama, slug, brand (FK), kategori (FK)
  - deskripsi, kondisi (new/second)
  - harga, harga_coret (untuk diskon)
  - is_active, is_featured, created_at
- [ ] Model `ProductImage`: product (FK), image, is_primary, urutan
- [ ] Model `ProductSize`: product (FK), ukuran (35-46), stok (int)
- [ ] Model `Banner`: judul, subtitle, gambar, link, urutan, is_active

### Storefront — Homepage
- [ ] Layout base template dark theme:
  - Navbar sticky: logo kiri, menu tengah (Katalog, Brand, Tentang), search + cart icon + avatar kanan
  - Footer: info toko, link, sosial media
- [ ] Hero carousel: full-width, dark overlay, teks bold, numbered bullets, auto-slide 5s
- [ ] Trust badge strip: 5 badge horizontal (ikon + teks singkat)
- [ ] Section "Produk Featured" — grid 4 kolom dari `is_featured=True`
- [ ] Section "Pilihan Untukmu" — rekomendasi berdasarkan rating tertinggi

### Storefront — Katalog
- [ ] Halaman `/katalog/` — grid produk 4 kolom desktop, 2 mobile
- [ ] Filter sidebar/drawer: brand (checkbox), ukuran (pill toggle), harga (range slider), kondisi
- [ ] Sort dropdown: Terbaru, Terlaris, Harga ↑, Harga ↓
- [ ] Filter + sort via HTMX (update grid tanpa reload halaman)
- [ ] HTMX live search (debounce 300ms)
- [ ] Produk card: foto hover scale, nama, harga, badge SOLD OUT / NEW
- [ ] Pagination infinite scroll via HTMX `hx-trigger="revealed"`

### Storefront — Detail Produk
- [ ] Galeri foto: foto utama besar + thumbnail kecil, klik ganti foto utama
- [ ] Pilih ukuran: pill button, disabled jika stok 0
- [ ] Tampilan stok: "Tersisa X" jika stok ≤ 3
- [ ] Tombol "Tambah ke Keranjang" (HTMX, update cart badge navbar)
- [ ] Tombol "Tambah ke Wishlist" (HTMX, toggle heart icon)
- [ ] Tab: Deskripsi | Ulasan (count) | Garansi & Return
- [ ] Tab Ulasan: tampilkan review + rata-rata bintang + distribusi bintang
- [ ] Tab Garansi: teks kebijakan garansi toko
- [ ] Section "Produk Terkait" (brand sama, 4 card)

---

## Sprint 3 — Wishlist, Keranjang & Checkout

### Wishlist
- [ ] Model `Wishlist`: customer (FK), product (FK), created_at
- [ ] HTMX toggle wishlist dari card produk dan halaman detail
- [ ] Halaman `/wishlist/` — grid produk + tombol hapus
- [ ] Kirim email notifikasi jika produk di wishlist stok hampir habis (≤ 2)

### Keranjang
- [ ] Model `Cart` + `CartItem`
- [ ] Persistent cart: simpan ke DB jika login, session jika guest → merge saat login
- [ ] Sidebar cart (drawer kanan) via HTMX `hx-swap="innerHTML"`
- [ ] Update qty + hapus item via HTMX
- [ ] Halaman `/cart/` — full cart view
- [ ] Validasi stok saat add to cart dan saat checkout

### Checkout
- [ ] Multi-step checkout (3 langkah, progress bar):
  1. **Alamat**: nama penerima, telepon, provinsi, kota, kecamatan, detail alamat, kode pos
  2. **Pengiriman**: pilih ekspedisi + layanan (dari RajaOngkir), tampilkan estimasi + biaya
  3. **Pembayaran**: ringkasan order + tombol bayar via Midtrans
- [ ] Autocomplete alamat (dropdown province → city → subdistrict via RajaOngkir atau data statis)
- [ ] RajaOngkir API: `ongkoskirim` endpoint, dipanggil dari backend Django (key tidak exposed ke frontend)
- [ ] Model `Order`, `OrderItem`, `ShippingAddress`
- [ ] Integrasi Midtrans Snap: buat transaksi dari backend, tampilkan Snap popup
- [ ] Webhook Midtrans: update `Order.status` berdasarkan notifikasi payment
- [ ] Halaman sukses pembayaran + redirect ke detail order
- [ ] Email konfirmasi order (HTML template branded)

---

## Sprint 4 — Manajemen Pesanan & Notifikasi

### Order Management (Customer)
- [ ] Halaman `/orders/` — daftar pesanan + status badge berwarna
- [ ] Detail pesanan: item, harga, ongkir, total, status timeline, info resi
- [ ] Tombol "Tandai Selesai" (customer konfirmasi penerimaan)
- [ ] Status flow: `pending → paid → processing → shipped → delivered → completed`

### Notifikasi Email
- [ ] Template email HTML branded (logo, dark theme, CTA button)
- [ ] Email: konfirmasi order (paid)
- [ ] Email: pesanan diproses (processing)
- [ ] Email: pesanan dikirim + nomor resi (shipped)
- [ ] Email: pesanan selesai + ajakan ulasan (completed, delay 1 hari via apscheduler)
- [ ] Email: update status laporan garansi
- [ ] SMTP config di `settings.py` (cPanel SMTP atau Gmail)

---

## Sprint 5 — Layanan Purna Jual (After-Sales)

> **Prioritas tinggi sesuai skripsi** — ini bagian utama yang membedakan dari e-commerce biasa

### Ulasan & Rating
- [ ] Model `Review`: order_item (FK), customer (FK), rating (1–5), komentar, foto[], is_visible, created_at
- [ ] Form ulasan hanya muncul jika `order.status == 'completed'`
- [ ] Upload foto ulasan (maks 3, preview sebelum submit)
- [ ] Validasi: 1 ulasan per item per order
- [ ] Tampilan ulasan di detail produk: daftar ulasan + foto + nama (disamarkan: "Wahyu A.")
- [ ] Rata-rata bintang + distribusi (progress bar per bintang 1–5)
- [ ] Admin Toko dapat toggle `is_visible` dari panel

### Form Laporan Garansi
- [ ] Model `GaransiLaporan`: order_item (FK), customer (FK), kategori (choices), deskripsi, foto[], status, catatan_resolusi, created_at, updated_at
- [ ] Tombol "Laporkan Masalah" di detail pesanan (hanya untuk item selesai, dalam 7 hari)
- [ ] Kategori laporan: Cacat Produk / Salah Ukuran / Tidak Sesuai Foto / Lainnya
- [ ] Upload foto bukti (maks 5)
- [ ] Halaman tracking laporan garansi untuk customer (`/orders/garansi/[id]/`)
- [ ] Status badge: Diterima → Ditinjau → Diselesaikan / Ditolak
- [ ] Email notifikasi ke customer setiap perubahan status

### Crisp Live Chat
- [ ] Embed Crisp widget script di `base.html` (`window.$crisp`)
- [ ] Set Crisp user identity jika login (nama, email via JS)
- [ ] Widget muncul di semua halaman storefront
- [ ] Tombol "Chat dengan Kami" di halaman detail produk dan pesanan

---

## Sprint 6 — Admin Toko Panel

### Layout & Auth
- [ ] Layout Admin Toko: sidebar kiri, topbar, content area — tema neutral (bukan dark total)
- [ ] Redirect ke `/admin-toko/login/` jika belum login atau bukan group `AdminToko`
- [ ] Dashboard ringkasan: pesanan hari ini, stok menipis, laporan garansi baru

### Fitur Admin Toko
- [ ] **Produk**: form tambah/edit produk + upload gambar + kelola stok per ukuran
- [ ] **Produk**: toggle aktif/nonaktif (tidak ada tombol hapus permanen)
- [ ] **Pesanan**: tabel dengan filter status, search nomor order, detail modal
- [ ] **Pesanan**: update status pesanan + input nomor resi ekspedisi
- [ ] **Pelanggan**: tabel customer + detail profil + riwayat beli (read-only)
- [ ] **Ulasan**: moderasi — toggle tampil/sembunyikan ulasan
- [ ] **Garansi**: daftar laporan masalah + update status + tulis catatan resolusi
- [ ] **Laporan**: tampilkan tabel laporan penjualan (no export button)
- [ ] Akses Crisp: link ke inbox Crisp (tab baru)

---

## Sprint 7 — Jasmine Owner Dashboard

### Layout Premium
- [ ] Layout Jasmine: ultra-dark (`#0A0A0A`), sidebar elegan dengan aksen emas `#D4AF37`
- [ ] Topbar: greeting "Selamat pagi/siang/sore, [nama owner]" + notifikasi bell
- [ ] Logo ZTP + label "Jasmine" di sidebar
- [ ] Semua chart menggunakan Chart.js (via CDN, compatible dengan shared hosting)

### Dashboard & Analytics
- [ ] KPI cards: Total Revenue (bulan ini), Total Order, Customer Baru, Produk Terlaris
- [ ] Setiap KPI card punya sparkline mini (7 hari terakhir)
- [ ] Grafik penjualan: toggle Harian / Bulanan / Tahunan (HTMX swap chart)
- [ ] Tabel 10 produk terlaris bulan ini
- [ ] Heatmap jam sibuk (opsional, Chart.js matrix)

### Full Management
- [ ] **Produk**: CRUD lengkap termasuk kategori dan brand
- [ ] **Banner**: kelola banner homepage (tambah/edit/urutkan/hapus)
- [ ] **Admin Toko**: buat akun, set permission group, suspend/aktifkan
- [ ] **Semua Pesanan**: tabel lengkap + filter + override status
- [ ] **Garansi**: semua laporan + eskalasi ke resolved/rejected
- [ ] **Laporan**: filter bulan-tahun → tabel transaksi → tombol Export Excel
- [ ] Export Excel: `openpyxl`, kolom: No, Tanggal, Pelanggan, Produk, Total, Status, Ekspedisi
- [ ] **Pengaturan**: SMTP email, Crisp token, logo toko, teks header/footer

---

## Sprint 8 — Testing, Polish & Deploy

### Testing
- [ ] Blackbox testing semua user story:
  - Customer: register, browse, checkout, ulasan, laporan garansi
  - Admin Toko: kelola produk, proses pesanan, update status garansi
  - Jasmine: dashboard, export laporan, kelola admin toko
- [ ] Test payment flow Midtrans (mode sandbox)
- [ ] Test RajaOngkir API dengan berbagai kota tujuan
- [ ] Test Crisp widget di berbagai halaman
- [ ] Test email notifikasi (semua trigger)
- [ ] Test webhook Midtrans (gunakan ngrok untuk local testing)

### Responsive & Polish
- [ ] Cek tampilan mobile (≤ 768px) semua halaman storefront
- [ ] Cek tampilan tablet (768px–1024px)
- [ ] Konsistensi dark theme 807-style di seluruh halaman
- [ ] Loading state untuk semua HTMX request (spinner/skeleton)
- [ ] Error state dan empty state (keranjang kosong, hasil search kosong, dll)
- [ ] Optimize gambar produk (thumbnail via Pillow, lazy load)
- [ ] Meta tags SEO dasar (title, description per halaman)

### Deploy ke Shared Hosting
- [ ] Setup Python App di cPanel
- [ ] Upload project via FTP/File Manager atau Git (jika hosting support)
- [ ] Konfigurasi `passenger_wsgi.py`
- [ ] Jalankan `collectstatic` → upload ke `public_html/static/`
- [ ] Konfigurasi MySQL database via cPanel
- [ ] Jalankan `migrate`
- [ ] Buat superuser/owner
- [ ] Set `.env` production (DEBUG=False, ALLOWED_HOSTS, keys)
- [ ] Test semua fitur di production
- [ ] Setup HTTPS (SSL via cPanel Let's Encrypt)

---

## Catatan Prioritas

| Prioritas | Modul |
|---|---|
| 🔴 Wajib | Auth, Katalog, Keranjang, Checkout, Midtrans, Pesanan |
| 🟠 Penting | Purna Jual (Ulasan + Garansi), Admin Toko, Crisp |
| 🟡 Penting | Jasmine Dashboard, RajaOngkir, Notifikasi Email |
| 🟢 Bonus | Rekomendasi Produk, Wishlist Notif, Analytics heatmap |
