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
- [x] Lupa password — flow: email input → OTP/link → reset password
- [x] Redirect setelah login: customer → `/`, admin toko → `/admin-toko/`, owner → `/jasmine/`
- [x] Setup Django Permission Groups: `AdminToko`, `Owner`
- [x] Buat `OwnerRequiredMixin` dan `AdminTokoRequiredMixin`
- [x] Halaman profil customer: edit nama, telepon, alamat default, ganti password, avatar

---

## Sprint 2 — Product Models & Storefront Katalog

### Models
- [x] Model `Category`: nama, slug, icon, urutan
- [x] Model `Brand`: nama, slug, logo
- [x] Model `Product`:
  - nama, slug, brand (FK), kategori (FK)
  - deskripsi, kondisi (new/second)
  - harga, harga_coret (untuk diskon)
  - is_active, is_featured, created_at
- [x] Model `ProductImage`: product (FK), image, is_primary, urutan
- [x] Model `ProductSize`: product (FK), ukuran (35-46), stok (int)
- [x] Model `Banner`: judul, subtitle, gambar, link, urutan, is_active

### Storefront — Homepage
- [x] Layout base template:
  - Navbar sticky: logo kiri, menu tengah, search + cart icon + avatar kanan
  - Footer: info toko, link, sosial media
- [x] Hero carousel: full-width, dark overlay, teks bold, numbered bullets
- [x] Trust badge strip: 5 badge horizontal (ikon + teks singkat)
- [x] Section "Koleksi Terbaru" — grid 4 kolom dari produk terbaru

#### 🎨 [UI POLISH] Homepage — Browse All / Hot Items
> **Architectural & Design Vision (Senior System Designer):**
> Kita harus memberikan kesan *premium, eksklusif, dan dinamis* ala brand hypebeast global (seperti StockX atau SNKRS). Pengalaman *scrolling* harus diselingi dengan micro-animations yang halus, hover state yang memberi *feedback* instan, dan tipografi yang kuat (menggunakan Outfit). 

**A. "Browse All" / Koleksi Terbaru (The Discovery Section)**
- [ ] **Section Header:** Tipografi tebal (Extrabold) uppercase "KOLEKSI TERBARU" di sebelah kiri, dengan sub-label berwarna abu-abu (gray-500) "Diperbarui setiap minggu.".
- [ ] **Tombol "Lihat Semua":** Posisi rata kanan, dengan efek *underline* yang mengembang (*expand on hover*) menggunakan warna primer (`#0B6A42`).
- [ ] **Card Produk (Grid):**
  - **Elevasi & Shadow:** Default state tanpa shadow (flat), saat di-*hover* card sedikit terangkat (`translate-y-[-4px]`) dengan `shadow-xl` yang lembut (blur tinggi, opacity rendah).
  - **Image Container:** Aspek rasio 1:1, latar belakang `#F9F9F9`. Gambar sepatu harus di-crop presisi di tengah. Saat di-*hover*, gambar sepatu melakukan *scale-up* 105% perlahan (`duration-500 ease-out`).
  - **Interaksi Beli (Add to Cart):** Pada *mobile*, user klik untuk masuk ke detail. Pada *desktop*, hover ke gambar akan memunculkan overlay gradien dari bawah yang membawa tombol "Pilih Ukuran" atau "Lihat Detail" (karena sepatu wajib pilih ukuran sebelum masuk keranjang).
  - **Wishlist Toggle:** Icon *Heart* di pojok kanan atas card. Gunakan micro-interaction (efek *bounce* kecil) saat diklik, dengan HTMX agar state langsung berubah (merah) tanpa *reload*. (Saat ini sudah ada, pastikan animasinya *smooth*).
  - **Status Badges:** Label "BARU" (hijau) atau "SECOND" (abu-abu gelap) di kiri atas.

**B. "Hot Items" / Trending (The FOMO Section)**
- [ ] **Layout Berbeda:** Jangan gunakan grid statis. Gunakan *horizontal scroll* (*carousel-like* tapi berbasis *native CSS scroll snap*) agar terasa beda dari "Koleksi Terbaru".
- [ ] **Algoritma "Hot":** Secara *backend*, *query* produk dengan kombinasi (Paling Banyak Dilihat + Rating Tinggi + Terjual). Filter: `review_count >= 3`, `average_rating >= 4.5`, atau fallback ke `is_featured=True`.
- [ ] **Visual "Hot":**
  - Tambahkan badge "🔥 TRENDING" dengan aksen warna merah/oranye gradien (`bg-gradient-to-r from-red-500 to-orange-500`) di kiri atas card.
  - Tampilkan elemen *social proof*: Teks kecil di bawah harga "⭐ 4.9 | 24 Terjual bulan ini" untuk memancing rasa *Fear Of Missing Out* (FOMO).

**C. Categories Section (The Gateway)**
- [ ] **Grid Layout Dinamis:** Gunakan grid 3 kolom (Desktop) atau *Bento Box Layout* di mana salah satu kategori prioritas (misal: "Nike") mendapat ukuran *span* lebih besar (2 kolom).
- [ ] **Visual Card Kategori:** 
  - Tinggi card konsisten (`h-96`).
  - Gambar menggunakan *full-cover background* dengan filter *dark overlay* (`bg-black/40`).
  - Saat card di-*hover*, gambar belakang perlahan membesar (`scale-110`) dan *overlay* menjadi sedikit lebih terang, sementara panah "Shop Collection →" bergeser sedikit ke kanan (`translate-x-2`).
- [ ] **Tipografi Kategori:** Teks nama kategori besar (3XL-4XL), *bold uppercase*, di posisi tengah atau kiri bawah. Tampilkan jumlah produk secara dinamis di bawahnya (misal: "128 Styles").
- [ ] **Fallback Elegan:** Jika gambar kategori kosong, jangan gunakan abu-abu mati. Gunakan *subtle gradient mesh* (gabungan warna utama toko) atau pattern geometri minimalis.

**D. Brand Strip / Brand Logos**
- [ ] Tambah section "BRAND TERPOPULER" setelah hero, sebelum koleksi terbaru
- [ ] Layout: logo brand horizontal, scrollable di mobile, centered di desktop
- [ ] Setiap logo: klik → filter katalog by brand
- [ ] Style: logo grayscale, hover → full color + pointer scale(1.05)

**E. Trust Badge Strip**
- [ ] Pastikan 5 badge tampil: 🛡 Garansi Puas | ↩ 7 Hari Return | 🚚 Free Ongkir | ✓ 100% Authentic | 👟 Koleksi Terlengkap
- [ ] Mobile: scrollable horizontal
- [ ] Animasi marquee/scrolling otomatis di mobile

### Storefront — Katalog
- [x] Halaman `/katalog/` — grid produk 4 kolom desktop, 2 mobile
- [x] Filter brand via HTMX (update grid tanpa reload)
- [x] Sort dropdown: Terbaru, Terlaris, Harga ↑, Harga ↓
- [x] Filter + sort via HTMX (update grid tanpa reload halaman)
- [x] HTMX live search (debounce 300ms)
- [x] Produk card: foto hover scale, nama, harga
- [x] Pagination infinite scroll via HTMX `hx-trigger="revealed"`

#### 🎨 [UI POLISH] Katalog — Filter Sidebar
> Filter yang ada di sidebar sudah partial. Berikut desain lengkapnya:

**Filter yang perlu diimplementasikan:**
- [ ] Filter ukuran (Size): pill toggle interaktif, ukuran dari data DB (`ProductSize`), bukan hardcode
  - Query: `ProductSize.objects.values_list('size', flat=True).distinct().order_by('size')`
  - Tampil sebagai grid pill: `[38] [39] [40] [41] [42]` — hitam jika aktif
- [ ] Filter harga: range slider dual-handle (min-max), format Rp
  - Range: Rp 0 – Rp 5.000.000
  - Gunakan `<input type="range">` native HTML + JS update label harga real-time
- [ ] Filter kondisi: radio (Semua / Baru / Second)
- [ ] Tombol "Reset Filter" — clear semua filter sekaligus
- [ ] Filter count: tampilkan jumlah produk per filter aktif `(12)`
- [ ] Mobile: sidebar → bottom sheet drawer (toggle tombol "Filter")
- [ ] Badge aktif: "3 Filter Aktif" di header katalog saat ada filter

#### 🎨 [UI POLISH] Katalog — Card Produk
- [ ] Badge "LAST PAIR" (merah) otomatis jika total stok = 1
- [ ] Badge "SOLD OUT" (abu-abu) overlay jika semua stok = 0 dan `is_active=False`
- [ ] Badge "BARU" jika produk dibuat < 7 hari yang lalu
- [ ] Badge "HOT" jika `average_rating >= 4.0` dan `review_count >= 3`
- [ ] Wishlist toggle di card: heart icon pojok kanan atas (sudah ada, pastikan fungsional)
- [x] Hover: add-to-cart quick button muncul dari bawah (overlay) — pilih ukuran dulu di detail
- [x] Rating stars kecil di bawah nama produk jika ada review

### Storefront — Detail Produk
- [x] Galeri foto: foto utama besar + thumbnail kecil, klik ganti foto utama
- [x] Pilih ukuran: pill button, disabled jika stok 0
- [x] Tombol "Tambah ke Keranjang" (HTMX) + Tombol Wishlist (HTMX toggle)
- [x] Section "Produk Terkait" (brand sama, 4 card)
- [x] Tampilkan stok real-time per ukuran: "Tersisa 2" jika stok ≤ 3 (via template tag)
- [x] Badge "LAST PAIR" jika 1 pasang, "SOLD OUT" jika stok 0 semua ukuran
- [x] Breadcrumb: Home > Katalog > [Brand] > [Nama Produk]
- [x] Ganti accordion jadi Tab UI: [Deskripsi] [Ulasan (N)] [Garansi & Return]
- [x] Tab Ulasan: ringkasan bintang 1-5 progress bar + list ulasan + foto pembeli

---

## 🎨 [ANALISIS] Sistem Warna Produk — Keputusan & Desain Teknis (Senior System Designer)

> **Keputusan Mutlak:** YA, sistem warna sangat krusial dan wajib diimplementasikan.
> 
> **Rasionalisasi Bisnis & UX:** Di industri *sneakers*, *colorway* adalah identitas produk. Pengguna mencari sepatu secara spesifik berdasarkan warna (misal: "Air Jordan 1 Chicago" merah vs "Panda" hitam-putih). Tanpa sistem warna yang *database-driven*:
> 1. Filter sidebar di katalog tidak akan berfungsi nyata.
> 2. UX akan buruk karena pengguna harus menebak warna dari foto.
> 3. *Data structuring* berantakan; sulit melakukan analitik tren penjualan berdasarkan warna.

### Rancangan Sistem Warna (Color System Architecture)

#### A. Model Schema (Database Layer)
Kita perlu field warna yang terstandarisasi, bukan *free-text*, agar *filtering* akurat.
- [x] Tambahkan field `color` di model `Product` menggunakan `CharField` dengan `choices` warna *fixed* (Putih, Hitam, Abu, Merah, Biru, dll).
- [x] *(Opsional tapi direkomendasikan)* Tambahkan `color_secondary` untuk sepatu dengan kombinasi warna ikonik (misal: Hitam & Merah).
- [x] Mapping kode HEX di *frontend* harus merujuk pada nilai statis dari *choices* ini.

#### B. Filter Katalog (UX Layer)
- [x] **UI Filter Interaktif:** Jangan gunakan *dropdown* standar. Gunakan bulatan warna (*color swatches*) berjejer membentuk grid di sidebar.
- [x] **State Active:** Saat diklik, bulatan warna akan memiliki *ring border* hitam tebal (`ring-2 ring-black ring-offset-2`).
- [x] **Multiple Selection:** Pengguna harus bisa memilih >1 warna (misal: filter Hitam ATAU Putih). Integrasikan *state*-nya ke URL query parameter (contoh: `?color=black,white`) via HTMX agar URL *shareable*.
- [x] **Dynamic Tooltip:** Tambahkan atribut `title` atau tooltip CSS murni untuk menampilkan nama teks warna saat di-*hover* (membantu aksesibilitas).

#### C. Card Produk (Homepage & Katalog)
- [x] **Indikator Visual Ringkas:** Tampilkan 1-2 titik warna kecil (ukuran `w-3 h-3`) sejajar secara horizontal tepat di bawah nama produk atau di sebelah harga.
- [x] Jika `color_secondary` tersedia, titik kedua agak saling tumpang tindih (*overlap*) dengan titik pertama.

#### D. Detail Produk (Conversion Layer)
- [x] **Section Pilihan Warna:** Sebelum pemilihan ukuran (Size), tampilkan section "WARNA" dengan informasi teks yang jelas. Contoh: `WARNA: Putih / Varsity Red`.
- [x] **Cross-Linking Colorways (Advanced):** Di skenario masa depan, jika ada produk dengan model sama namun warna beda (misal produk A hitam, produk B putih), kita bisa me-render *thumbnail* produk B di halaman produk A sebagai *alternative colorways*. Saat ini, cukup fokuskan pada penampilan spesifikasi warna produk yang sedang dilihat.

#### E. Admin Panel (Backend Layer)
- [x] **Form Produk:** Admin wajib memilih *color* dari dropdown (required) saat membuat/mengedit produk.
- [x] Sediakan fitur migrasi data (satu kali) untuk memberikan *default value* (misal: 'multi') pada semua data sepatu lama di database agar web tidak error saat implementasi.

---



## Sprint 3 — Wishlist, Keranjang & Checkout

### Wishlist
- [x] Model `Wishlist`: customer (FK), product (FK), created_at
- [x] HTMX toggle wishlist dari card produk dan halaman detail
- [x] Halaman `/wishlist/` — grid produk + tombol hapus
- [ ] Notif in-app: produk di wishlist stok hampir habis (≤ 2) — via signal ProductSize save

### Keranjang
- [x] Model `Cart` + `CartItem`
- [x] Persistent cart: simpan ke DB jika login, session jika guest → merge saat login
- [x] Tambah ke keranjang (dengan pilihan ukuran) -> langsung redirect ke `/cart/`
- [x] HTMX Keranjang: update qty (+/-), hapus item (tanpa reload)
- [x] Halaman `/cart/` penuh (Laci/Drawer ditiadakan)
- [x] Validasi stok saat add to cart dan saat checkout

### Checkout
- [x] Model `Order`, `OrderItem`, `ShippingAddress`
- [x] RajaOngkir API: `ongkoskirim` endpoint, dipanggil dari backend Django
- [x] Autocomplete Provinsi & Kota (Dimuat secara *Asynchronous HTMX* agar halaman tidak lag)
- [x] Pilihan Pengiriman Dinamis: Menampilkan seluruh layanan JNE, POS, TIKI sekaligus berdasarkan Kota
- [x] Data Cadangan (Fallback): Mencegah dropdown kosong jika API RajaOngkir *timeout*
- [x] Hitung ongkos kirim berdasarkan berat, tujuan, dan kurir (RajaOngkir)
- [x] Real-time update total pembayaran saat memilih layanan pengiriman (client-side JS)
- [x] Generate Snap Token untuk pesanan (auto-detect Production vs Sandbox)
- [x] Popup Midtrans Snap di halaman checkout sukses (auto-open, URL Production/Sandbox otomatis)
- [x] Webhook endpoint untuk update status otomatis (Pending → Paid)
- [x] In-app notif setelah bayar sukses + redirect ke detail order
- [x] Form checkout unified (`id="checkout-form"`) — semua input (alamat, kurir, pengiriman) dalam satu form
- [ ] Merge cart guest → user saat login (session cart dipindah ke user cart)

---

## 🛒 [ANALISIS ARCHITECTURE] Sistem Checkout, Cart Persistance & Voucher (Senior System Designer)

> **Evaluasi Sistem Saat Ini:** Berdasarkan audit sistem, ditemukan beberapa *bottleneck* kritis pada alur checkout yang menyebabkan performa lambat, *state* keranjang hilang, dan disfungsi pada API pihak ketiga. Berikut adalah rancangan arsitektur perbaikannya:

### A. Persistensi Keranjang (Cart Session Fix)
- [x] **Masalah:** Saat ini *guest user* (belum login) kehilangan keranjang belanja saat kembali ke halaman utama (*homepage*). Ini terjadi karena `request.session.create()` di Django tidak otomatis mengirimkan *cookie* jika tidak ada data sesi yang secara spesifik dimodifikasi (aturan *session.modified*).
- [x] **Desain Solusi:** 
  - [x] Modifikasi fungsi `get_or_create_cart` di `orders/views.py`.
  - [x] Berikan trigger mutasi sesi: `request.session['cart_initialized'] = True` tepat setelah membuat sesi baru. Hal ini memaksa *middleware* Django untuk menyimpan *cookie* `sessionid` di peramban (browser) pengguna.

### B. Optimasi Kecepatan Checkout & Integrasi RajaOngkir
- [x] **Masalah:** Halaman `/checkout/` memuat sangat lambat karena melakukan panggilan API *Synchronous* ke RajaOngkir (`get_rajaongkir_provinces`) setiap kali halaman di-*load*.
- [x] **Desain Solusi:**
  - [x] **Caching Layer:** Terapkan `django.core.cache` (Memcached/Redis atau FileBasedCache) untuk menyimpan data Provinsi dan Kota selama minimal 24 jam. Hal ini akan memangkas waktu muat dari 2000ms menjadi 10ms.
  - [ ] **Validasi Kredensial:** Pastikan `RAJAONGKIR_API_KEY` di *Environment* (`.env`) adalah kunci yang valid (bukan *dummy*), karena API tidak akan membalas dengan JSON yang benar jika kuncinya ditolak.
  - [ ] **Error Handling UI:** Tambahkan *fallback* teks merah di UI menggunakan HTMX jika API RajaOngkir *timeout* atau gagal (saat ini error *backend* hanya ditangkap oleh `print()`).

### C. Pembayaran Midtrans Snap
- [ ] **Masalah:** *Popup* Midtrans belum muncul dengan benar.
- [ ] **Desain Solusi:**
  - [ ] Kunci `MIDTRANS_SERVER_KEY` dan `MIDTRANS_CLIENT_KEY` di `.env` harus valid (gunakan *sandbox* untuk pengujian).
  - [ ] Pastikan di `checkout_success.html` sudah me-render `<script src="https://app.sandbox.midtrans.com/snap/snap.js" data-client-key="{{ client_key }}"></script>` dan otomatis men-trigger `window.snap.pay('{{ order.midtrans_transaction_id }}')`.

### D. Sistem Voucher (Ekspansi Masa Depan)
> Fitur ini ditambahkan ke antrean *backlog* (*task list*) untuk dieksekusi agar pembeli bisa menggunakan kode promo (karena fitur "ZTP Point" telah resmi dihapus untuk menyederhanakan UX).

- [ ] **Skema Database (`Voucher` Model):**
  - [ ] `code` (CharField, unique)
  - [ ] `discount_type` (Choices: 'percentage' atau 'nominal')
  - [ ] `discount_value` (DecimalField)
  - [ ] `min_purchase` (DecimalField)
  - [ ] `valid_from` & `valid_to` (DateTimeField)
  - [ ] `quota` (IntegerField)
  - [ ] `is_active` (BooleanField)
- [ ] **Modifikasi Cart:** Tambahkan relasi `voucher = models.ForeignKey(Voucher, null=True, blank=True)` pada model `Cart`.
- [ ] **API HTMX (`/api/apply-voucher/`):** Endpoint yang menerima input teks, memvalidasi aturan voucher, mengunci *state* ke keranjang pengguna, dan mengembalikan *swap* nilai pada blok `#total-payment` beserta diskonnya.

---

## Sprint 4 — Manajemen Pesanan & Notifikasi

### Order Management (Customer)
- [x] Daftar Pesanan (`/orders/`): riwayat transaksi, filter status (Semua, Belum Bayar, Dikirim, Selesai)
- [ ] Filter tab status di halaman riwayat pesanan (Semua, Menunggu Bayar, Diproses, Dikirim, Selesai)
- [x] Detail Pesanan (`/orders/<id>/`): resi kurir, item dibeli, rincian pembayaran
- [x] Tombol "Tandai Selesai" (muncul saat status Shipped)
- [x] Cetak Invoice sederhana (PDF / Print view)
- [ ] Tombol "Bayar Sekarang" di riwayat pesanan untuk order status `pending` (re-trigger Midtrans Snap)

### Sistem Notifikasi In-App (Pengganti Email — Built-in)
> Karena tidak menggunakan SMTP, seluruh notifikasi berbasis in-app via model `core.Notification`
- [x] Model `Notification`: user, title, message, link, is_read, created_at
- [x] Signal `pre_save` Order → auto-create notifikasi saat status berubah
- [x] Notif: Pembayaran Berhasil (paid)
- [x] Notif: Pesanan Diproses (processing)
- [x] Notif: Pesanan Dikirim + nomor resi (shipped)
- [x] Notif: Pesanan Selesai + ajakan ulasan (completed)
- [ ] Notif: Klaim Garansi Diterima (saat user submit klaim)
- [ ] Notif: Update status klaim garansi (pending→approved/rejected/resolved)
- [ ] Notif: Produk di wishlist stok hampir habis (≤ 2)
- [ ] Halaman notifikasi penuh `/notifications/` — list semua notif + tandai sudah dibaca
- [ ] Navbar bell: badge count in-app (auto refresh via HTMX polling setiap 60 detik)
- [x] Tombol "Tandai Semua Dibaca" di dropdown notifikasi
- [ ] Notif: Pesanan dibatalkan (cancelled) — ketika admin batalkan

---

## Sprint 5 — Layanan Purna Jual & Penyempurnaan

### Ulasan & Rating
- [x] Model `Review` + form ulasan (rating 1-5, komentar, 1 foto)
- [x] Tampil ulasan di halaman detail produk (accordion)
- [x] Rata-rata bintang di card produk dan halaman detail
- [x] Hanya order status `completed` yang bisa review
- [ ] Distribusi bintang per rating (progress bar 1★–5★) di halaman detail produk
- [ ] Upload hingga 3 foto per ulasan (sesuai PRD), bukan hanya 1
- [ ] Field `is_visible` di model Review untuk moderasi admin

### Laporan Garansi
- [x] Model `WarrantyClaim` + form klaim + upload foto bukti
- [x] Status klaim: pending → approved → rejected → resolved
- [ ] Field `kategori` di model WarrantyClaim (choices: cacat_produk/salah_ukuran/tidak_sesuai_foto/lainnya)
- [ ] Validasi batas 7 hari sejak order `completed` untuk klaim garansi
- [ ] Halaman tracking klaim garansi (`/orders/garansi/<id>/`) — timeline status + catatan resolusi admin

### Crisp Live Chat
- [x] Embed Crisp widget script di `base.html` (`window.$crisp`)
- [x] Set Crisp user identity jika login (nama, email via JS)
- [x] Widget muncul di semua halaman storefront
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

- [x] Real-time update total pembayaran saat memilih layanan pengiriman (client-side JS)
- [x] Generate Snap Token untuk pesanan (auto-detect Production vs Sandbox)
- [x] Popup Midtrans Snap di halaman checkout sukses (auto-open, URL Production/Sandbox otomatis)
- [x] Webhook endpoint untuk update status otomatis (Pending → Paid)
- [x] In-app notif setelah bayar sukses + redirect ke detail order
- [x] Form checkout unified (`id="checkout-form"`) — semua input (alamat, kurir, pengiriman) dalam satu form
- [x] Merge cart guest → user saat login (session cart dipindah ke user cart)

---

## 🛒 [ANALISIS ARCHITECTURE] Sistem Checkout, Cart Persistance & Voucher (Senior System Designer)

> **Evaluasi Sistem Saat Ini:** Berdasarkan audit sistem, ditemukan beberapa *bottleneck* kritis pada alur checkout yang menyebabkan performa lambat, *state* keranjang hilang, dan disfungsi pada API pihak ketiga. Berikut adalah rancangan arsitektur perbaikannya:

### A. Persistensi Keranjang (Cart Session Fix)
- [x] **Masalah:** Saat ini *guest user* (belum login) kehilangan keranjang belanja saat kembali ke halaman utama (*homepage*). Ini terjadi karena `request.session.create()` di Django tidak otomatis mengirimkan *cookie* jika tidak ada data sesi yang secara spesifik dimodifikasi (aturan *session.modified*).
- [x] **Desain Solusi:** 
  - [x] Modifikasi fungsi `get_or_create_cart` di `orders/views.py`.
  - [x] Berikan trigger mutasi sesi: `request.session['cart_initialized'] = True` tepat setelah membuat sesi baru. Hal ini memaksa *middleware* Django untuk menyimpan *cookie* `sessionid` di peramban (browser) pengguna.

### B. Optimasi Kecepatan Checkout & Integrasi RajaOngkir
- [x] **Masalah:** Halaman `/checkout/` memuat sangat lambat karena melakukan panggilan API *Synchronous* ke RajaOngkir (`get_rajaongkir_provinces`) setiap kali halaman di-*load*.
- [x] **Desain Solusi:**
  - [x] **Caching Layer:** Terapkan `django.core.cache` (Memcached/Redis atau FileBasedCache) untuk menyimpan data Provinsi dan Kota selama minimal 24 jam. Hal ini akan memangkas waktu muat dari 2000ms menjadi 10ms.
  - [ ] **Validasi Kredensial:** Pastikan `RAJAONGKIR_API_KEY` di *Environment* (`.env`) adalah kunci yang valid (bukan *dummy*), karena API tidak akan membalas dengan JSON yang benar jika kuncinya ditolak.
  - [x] **Error Handling UI:** Tambahkan *fallback* teks merah di UI menggunakan HTMX jika API RajaOngkir *timeout* atau gagal (saat ini error *backend* hanya ditangkap oleh `print()`).

### C. Pembayaran Midtrans Snap
- [ ] **Masalah:** *Popup* Midtrans belum muncul dengan benar.
- [ ] **Desain Solusi:**
  - [ ] Kunci `MIDTRANS_SERVER_KEY` dan `MIDTRANS_CLIENT_KEY` di `.env` harus valid (gunakan *sandbox* untuk pengujian).
  - [ ] Pastikan di `checkout_success.html` sudah me-render `<script src="https://app.sandbox.midtrans.com/snap/snap.js" data-client-key="{{ client_key }}"></script>` dan otomatis men-trigger `window.snap.pay('{{ order.midtrans_transaction_id }}')`.

### D. Sistem Voucher (Ekspansi Masa Depan)
> Fitur ini ditambahkan ke antrean *backlog* (*task list*) untuk dieksekusi agar pembeli bisa menggunakan kode promo (karena fitur "ZTP Point" telah resmi dihapus untuk menyederhanakan UX).

- [ ] **Skema Database (`Voucher` Model):**
  - [ ] `code` (CharField, unique)
  - [ ] `discount_type` (Choices: 'percentage' atau 'nominal')
  - [ ] `discount_value` (DecimalField)
  - [ ] `min_purchase` (DecimalField)
  - [ ] `valid_from` & `valid_to` (DateTimeField)
  - [ ] `quota` (IntegerField)
  - [ ] `is_active` (BooleanField)
- [ ] **Modifikasi Cart:** Tambahkan relasi `voucher = models.ForeignKey(Voucher, null=True, blank=True)` pada model `Cart`.
- [ ] **API HTMX (`/api/apply-voucher/`):** Endpoint yang menerima input teks, memvalidasi aturan voucher, mengunci *state* ke keranjang pengguna, dan mengembalikan *swap* nilai pada blok `#total-payment` beserta diskonnya.

---

## Sprint 4 — Manajemen Pesanan & Notifikasi

### Order Management (Customer)
- [x] Daftar Pesanan (`/orders/`): riwayat transaksi, filter status (Semua, Belum Bayar, Dikirim, Selesai)
- [x] Filter tab status di halaman riwayat pesanan (Semua, Menunggu Bayar, Diproses, Dikirim, Selesai)
- [x] Detail Pesanan (`/orders/<id>/`): resi kurir, item dibeli, rincian pembayaran
- [x] Tombol "Tandai Selesai" (muncul saat status Shipped)
- [x] Cetak Invoice sederhana (PDF / Print view)
- [x] Tombol "Bayar Sekarang" di riwayat pesanan untuk order status `pending` (re-trigger Midtrans Snap)

### Sistem Notifikasi In-App (Pengganti Email — Built-in)
> Karena tidak menggunakan SMTP, seluruh notifikasi berbasis in-app via model `core.Notification`
- [x] Model `Notification`: user, title, message, link, is_read, created_at
- [x] Signal `pre_save` Order → auto-create notifikasi saat status berubah
- [x] Notif: Pembayaran Berhasil (paid)
- [x] Notif: Pesanan Diproses (processing)
- [x] Notif: Pesanan Dikirim + nomor resi (shipped)
- [x] Notif: Pesanan Selesai + ajakan ulasan (completed)
- [x] Notif: Klaim Garansi Diterima (saat user submit klaim)
- [x] Notif: Update status klaim garansi (pending→approved/rejected/resolved)
- [ ] Notif: Produk di wishlist stok hampir habis (≤ 2)
- [x] Halaman notifikasi penuh `/notifications/` — list semua notif + tandai sudah dibaca
- [x] Navbar bell: badge count in-app (auto refresh via HTMX polling setiap 60 detik)
- [x] Tombol "Tandai Semua Dibaca" di dropdown notifikasi
- [x] Notif: Pesanan dibatalkan (cancelled) — ketika admin batalkan

---

## Sprint 5 — Layanan Purna Jual & Penyempurnaan

### Ulasan & Rating
- [x] Model `Review` + form ulasan (rating 1-5, komentar, 1 foto)
- [x] Tampil ulasan di halaman detail produk (accordion)
- [x] Rata-rata bintang di card produk dan halaman detail
- [x] Hanya order status `completed` yang bisa review
- [ ] Distribusi bintang per rating (progress bar 1★–5★) di halaman detail produk
- [ ] Upload hingga 3 foto per ulasan (sesuai PRD), bukan hanya 1
- [ ] Field `is_visible` di model Review untuk moderasi admin

### Laporan Garansi
- [x] Model `WarrantyClaim` + form klaim + upload foto bukti
- [x] Status klaim: pending → approved → rejected → resolved
- [ ] Field `kategori` di model WarrantyClaim (choices: cacat_produk/salah_ukuran/tidak_sesuai_foto/lainnya)
- [ ] Validasi batas 7 hari sejak order `completed` untuk klaim garansi
- [ ] Halaman tracking klaim garansi (`/orders/garansi/<id>/`) — timeline status + catatan resolusi admin

### Crisp Live Chat
- [x] Embed Crisp widget script di `base.html` (`window.$crisp`)
- [x] Set Crisp user identity jika login (nama, email via JS)
- [x] Widget muncul di semua halaman storefront
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

---

## B2C UI/UX System Design Improvements (Analysis Results)

### 1. Animasi & Interaktivitas UI
- [x] **Carousel Banner Otomatis:** Integrasikan Swiper.js/Alpine.js pada Hero Banner untuk transisi *slide* otomatis.
- [x] **Micro-interactions:** Tambahkan animasi *zoom-in* lambat (scale 1.05) pada _card_ produk saat di-_hover_, dan efek interaktif pada ikon profil/keranjang.

### 2. Pengelolaan Keranjang (Cart Drawer)
- [x] **Toast Notifications:** Tampilkan notifikasi kecil di pojok kanan atas layar saat produk berhasil ditambahkan ke keranjang (hilang otomatis).

### 3. Sistem Filter & Pencarian
- [x] **Mobile Filter Modal:** Pindahkan saringan kategori/urutan ke *modal* atau *bottom-sheet* saat dilihat melalui layar *mobile*.
- [x] **Live Search Results:** Buat hasil pencarian langsung muncul sebagai _dropdown_ seketika saat pengguna mengetik (menggunakan `hx-trigger`).

### 4. Alur Checkout & Pembayaran
- [x] **Validasi Ongkir Dinamis:** Integrasikan RajaOngkir API pada halaman *Checkout* untuk kalkulasi otomatis tarif pengiriman tanpa *reload*.
- [x] **Integrasi Payment Gateway:** Pasang Midtrans Snap pada tombol "Buat Pesanan" agar *popup* pembayaran instan muncul.

## Bug yang Sudah Diperbaiki (Sprint Berjalan)
- [x] Fix NameError module settings di checkout_success views
- [x] Fix Halaman keranjang kosong setelah berhasil checkout pertama kali karena keranjang tidak dikosongkan dengan benar dari session vs user cart, dan profile history yang hardcoded
- [x] Fix Tombol Bayar di detail pesanan tidak melakukan aksi jika token Midtrans API gagal tergenerate akibat kunci API tidak valid/unauthorized
- [x] Fix Salah deteksi environment Midtrans (Production vs Sandbox) akibat format kunci API tanpa awalan SB-
- [x] Tambahkan fitur tombol Cek Status Pembayaran secara manual untuk transaksi Midtrans
- [x] Hapus halaman Riwayat Pesanan ganda (orders:history) dan gabungkan sepenuhnya ke tab Pesanan Saya di halaman Profil