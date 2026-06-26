# Product Requirements Document (PRD)
# ZTP Sneakers — Platform E-Commerce B2C

> Dokumen ini adalah sumber kebenaran tunggal (*single source of truth*) tentang sistem ZTP Sneakers.
> Mencakup konteks bisnis, arsitektur, struktur data, alur sistem, dan semua halaman yang diimplementasikan.

---

## Daftar Isi

1. [Ringkasan Proyek](#1-ringkasan-proyek)
2. [Latar Belakang & Masalah](#2-latar-belakang--masalah)
3. [Tujuan & Sasaran](#3-tujuan--sasaran)
4. [Stack Teknologi](#4-stack-teknologi)
5. [Struktur Proyek](#5-struktur-proyek)
6. [Arsitektur Aplikasi](#6-arsitektur-aplikasi)
7. [Model Data & Relasi](#7-model-data--relasi)
8. [Role & Hak Akses Pengguna](#8-role--hak-akses-pengguna)
9. [Peta URL Lengkap](#9-peta-url-lengkap)
10. [Fitur & Halaman Storefront](#10-fitur--halaman-storefront)
11. [Fitur & Halaman Admin Toko](#11-fitur--halaman-admin-toko)
12. [Fitur & Halaman Owner / Jasmine](#12-fitur--halaman-owner--jasmine)
13. [Alur Bisnis Utama](#13-alur-bisnis-utama)
14. [Integrasi Pihak Ketiga](#14-integrasi-pihak-ketiga)
15. [Sistem Notifikasi & Signal](#15-sistem-notifikasi--signal)
16. [Konfigurasi & Environment](#16-konfigurasi--environment)

---

## 1. Ringkasan Proyek

| Atribut | Detail |
|---|---|
| **Nama Proyek** | ZTP Sneakers B2C Platform |
| **Tipe** | E-Commerce B2C (Business-to-Consumer) |
| **Domain Bisnis** | Penjualan sepatu sneakers second/preloved |
| **Target Pengguna** | Pembeli online nasional, utamanya segmen usia 17–35 tahun |
| **Bisnis Nyata** | UMKM ZTP Sneakers, Pontianak, Kalimantan Barat |
| **Framework** | Django 5.2 + HTMX 2.x + Tailwind CSS 3.x |
| **Database** | PostgreSQL 16 |
| **Bahasa** | Python 3.12 |
| **Status** | Development / Lokal (target deploy cPanel Shared Hosting) |

---

## 2. Latar Belakang & Masalah

ZTP Sneakers sebelumnya mengandalkan Instagram dan transaksi tatap muka. Masalah operasional utama:

| Masalah Lama | Dampak | Solusi Platform |
|---|---|---|
| Cek stok manual via DM Instagram | Respons lambat, pelanggan kabur | Katalog real-time dengan stok per ukuran |
| Produk terjual tidak dihapus dari Instagram | Pelanggan tertipu, trust rusak | Status otomatis — badge SOLD OUT langsung |
| Tidak ada tracking pesanan | Pelanggan sering komplain | Timeline status pesanan lengkap |
| Jangkauan hanya lokal Pontianak | Revenue terbatas | Platform online + ongkir nasional via RajaOngkir |
| Tidak ada purna jual terstruktur | Garansi kacau, ulasan tidak ada | Sistem review, klaim garansi, live chat |
| Tidak ada data penjualan | Owner tidak bisa analisis | Dashboard analytics + export Excel |

---

## 3. Tujuan & Sasaran

**Tujuan Utama:**
- Digitalisasi penuh operasional toko ZTP Sneakers dari Instagram ke platform web mandiri
- Meningkatkan kepercayaan pembeli dengan sistem transaksi yang terstruktur

**Lima Pilar E-Commerce yang Diimplementasikan:**
1. **Automation** — Notifikasi otomatis, update stok otomatis, perhitungan ongkir otomatis
2. **Integration** — Midtrans payment gateway, RajaOngkir API, Google OAuth
3. **Interaction** — Live chat Crisp, live search HTMX, wishlist, ulasan interaktif
4. **Publication** — Katalog online, detail produk, banner promosi, halaman info toko
5. **Transaction** — Checkout multi-step, pembayaran digital, riwayat pesanan, invoice

---

## 4. Stack Teknologi

| Layer | Teknologi | Versi | Keterangan |
|---|---|---|---|
| **Backend** | Python | 3.12 | Runtime utama |
| **Web Framework** | Django | 5.2 | MVC framework |
| **Frontend Interaktif** | HTMX | 2.x | Partial reload tanpa JS framework besar |
| **CSS Framework** | Tailwind CSS | 3.x | Utility-first, via CDN |
| **Database** | PostgreSQL | 16 | DB produksi |
| **Auth** | django-allauth | 65.x | Email + Google OAuth |
| **Payment** | Midtrans Snap | — | Virtual Account, e-wallet |
| **Shipping** | RajaOngkir Komerce API | v1 | Kalkulasi ongkir JNE/POS/TIKI |
| **Admin UI** | Jazzmin | 3.x | Django Admin tema premium |
| **HTMX Helper** | django-htmx | 1.27 | Middleware + request detection |
| **Form Helper** | django-widget-tweaks | 1.5 | Styling form Django |
| **Export** | openpyxl | 3.x | Generate file Excel (.xlsx) |
| **Static Files** | WhiteNoise | 6.x | Serve static di production |
| **Live Chat** | Crisp | — | Widget embed di frontend |
| **Email** | Console (dev) / SMTP (prod) | — | Notifikasi otomatis |
| **Deploy Target** | cPanel + Passenger WSGI | — | Shared Hosting |

**Dependencies Lengkap** (dari `requirements.txt`):
```
Django==6.0.5, django-allauth==65.18.0, django-htmx==1.27.0,
django-jazzmin==3.0.4, django-widget-tweaks==1.5.1, midtransclient==1.4.2,
openpyxl==3.1.5, psycopg2==2.9.12, pillow==12.2.0, whitenoise==6.12.0,
python-dotenv==1.2.2, requests==2.34.2, APScheduler==3.11.2
```

---

## 5. Struktur Proyek

```
ztpsneakers/                        ← Root project Django
│
├── ztpsneakers/                    ← Django project config
│   ├── settings.py                 ← Konfigurasi utama (DB, Apps, Auth, API Keys)
│   ├── urls.py                     ← URL routing root
│   ├── wsgi.py                     ← Entry point WSGI (production)
│   └── asgi.py                     ← Entry point ASGI (async)
│
├── core/                           ← App inti: notifikasi, footer icons, context
│   ├── models.py                   ← Notification, FooterIcon
│   ├── views.py                    ← Notif views, mark read, count badge
│   ├── context_processors.py       ← Inject nav_categories, nav_brands, unread_notif ke semua template
│   ├── validators.py               ← Validasi file gambar upload
│   ├── mixins.py                   ← Reusable mixins
│   └── urls.py                     ← URL: /core/notif/mark-read/, /core/notif/count/, /core/notif/all/
│
├── userauths/                      ← App auth & profil pengguna
│   ├── models.py                   ← User (AbstractUser), UserProfile
│   ├── views.py                    ← auth_main, auth_check, auth_login, auth_register, auth_logout, profile
│   ├── forms.py                    ← Form helper
│   └── urls.py                     ← URL: /user/auth/, /user/login/, /user/register/, /user/profile/
│
├── products/                       ← App katalog produk
│   ├── models.py                   ← Category, Brand, Product, ProductImage, ProductSize, Banner, Review
│   ├── views.py                    ← (views produk dihandle storefront)
│   └── admin.py                    ← Registrasi model ke Django Admin
│
├── storefront/                     ← App views halaman customer-facing
│   ├── views.py                    ← home_view, catalog_view, product_detail_view, live_search_view
│   └── urls.py                     ← URL: /, /katalog/, /produk/<slug>/, /live-search/
│
├── orders/                         ← App transaksi (cart, checkout, order, garansi)
│   ├── models.py                   ← Voucher, Wishlist, Cart, CartItem, Order, OrderItem, ShippingAddress, WarrantyClaim
│   ├── views.py                    ← Cart, wishlist, checkout, webhook, riwayat, review, garansi, voucher
│   ├── urls.py                     ← URL: /pesanan/cart/, /pesanan/checkout/, /pesanan/history/, dll.
│   ├── utils.py                    ← RajaOngkir API, Midtrans Snap, merge_guest_cart
│   ├── signals.py                  ← Signal notifikasi: order status change, warranty status change
│   ├── admin.py                    ← Registrasi model ke Django Admin
│   ├── admin_export.py             ← View export Excel untuk Owner
│   └── admin_views.py              ← API dashboard analytics untuk Jazzmin (Owner)
│
├── admintoko/                      ← App panel admin toko (staf)
│   ├── views.py                    ← Dashboard, produk CRUD, pesanan, garansi, review, pelanggan
│   └── urls.py                     ← URL: /admintoko/
│
├── aftersales/                     ← App purna jual (model kosong, logika ada di orders/)
│
├── templates/                      ← Semua template HTML Django
│   ├── base.html                   ← Base template utama
│   ├── partials/
│   │   ├── navbar.html             ← Navigasi global (kategori, brand, cart badge, notif badge)
│   │   └── footer.html             ← Footer global
│   ├── storefront/
│   │   ├── home.html               ← Halaman beranda
│   │   ├── katalog.html            ← Halaman katalog produk
│   │   ├── detail.html             ← Halaman detail produk
│   │   └── partials/               ← product_grid.html, search_results.html, dll.
│   ├── orders/
│   │   ├── cart.html               ← Halaman keranjang
│   │   ├── checkout.html           ← Halaman checkout multi-step
│   │   ├── checkout_success.html   ← Halaman sukses order
│   │   ├── detail.html             ← Detail pesanan + timeline
│   │   ├── invoice.html            ← Cetak invoice
│   │   ├── wishlist.html           ← Halaman wishlist
│   │   ├── review_form.html        ← Form tulis ulasan
│   │   ├── warranty_form.html      ← Form klaim garansi
│   │   ├── warranty_tracking.html  ← Tracking status garansi
│   │   └── partials/               ← cart_drawer_content.html, cart_count_badge.html
│   ├── userauths/
│   │   ├── auth_main.html          ← Halaman login/register (tab toggle)
│   │   ├── profile.html            ← Halaman profil pengguna
│   │   └── partials/               ← login_form.html, register_form.html, login_password.html
│   ├── admintoko/
│   │   ├── base_admin.html         ← Base layout admin toko
│   │   ├── dashboard.html, products.html, orders.html, dll.
│   ├── jasmine/
│   │   ├── base_jasmine.html       ← Base layout owner dashboard
│   │   └── dashboard.html          ← Dashboard analytics owner
│   ├── core/
│   │   └── notifications.html      ← Halaman semua notifikasi
│   ├── pages/
│   │   ├── about.html, contact.html, faq.html
│   │   ├── authenticity.html, privacy.html, return_policy.html
│   └── account/                    ← Template allauth (reset password, dll.)
│
├── static/                         ← Static files sumber (CSS, JS, images)
│   ├── assets/
│   │   ├── css/jazzmin-custom.css  ← Custom styling Jazzmin admin
│   │   └── images/ztppng.png       ← Logo toko
│   └── images/
│
├── media/                          ← File upload pengguna
│   ├── banners/                    ← Gambar banner homepage
│   ├── brands/                     ← Logo brand
│   ├── products/                   ← Foto produk
│   └── footer_icons/               ← Ikon footer
│
├── docs/                           ← Dokumentasi proyek
│   ├── PRD.md                      ← Dokumen ini
│   ├── ERD.md                      ← Entity Relationship Diagram (DBML)
│   ├── TASK.md                     ← Daftar task implementasi
│   ├── UIUX_FLOW.md                ← Alur UX per halaman
│   ├── sequence.md                 ← Sequence diagram alur transaksi
│   ├── class_diagram.md            ← Class diagram model
│   ├── normalisasi.md              ← Normalisasi database
│   └── activity.md                 ← Activity diagram
│
├── design-system/                  ← Design system ZTP Sneakers (komponen UI)
├── manage.py                       ← Django CLI management
├── requirements.txt                ← Python dependencies
├── seed.py                         ← Script seeder data awal
├── .env                            ← Environment variables aktual (tidak di-commit)
└── .env.example                    ← Template environment variables
```

---

## 6. Arsitektur Aplikasi

### Pola Arsitektur

Platform ini mengikuti pola **MVT (Model-View-Template)** bawaan Django dengan pendekatan **multi-app modular**:

```
Request Browser
      ↓
Django URL Router (ztpsneakers/urls.py)
      ↓
App URL Router (storefront/urls.py, orders/urls.py, dll.)
      ↓
View Function (views.py) ← Context Processors (core/context_processors.py)
      ↓
Model Query (models.py) ←→ PostgreSQL DB
      ↓
Template Render (templates/*.html)
      ↓
Response HTML ke Browser
      ↑
HTMX Partial Request → View → Partial Template → Swap DOM
```

### App Dependencies

```
storefront  → products (Product, Category, Brand, Banner)
            → orders   (Wishlist)

orders      → products (Product, ProductSize)
            → userauths (User)
            → core    (Notification)

admintoko   → orders   (Order, WarrantyClaim)
            → products (Product, ProductSize, Review)
            → userauths (User)

core        → userauths (User)
```

### Middleware Stack (urutan eksekusi)

1. `SecurityMiddleware` — HTTPS redirect, security headers
2. `WhiteNoiseMiddleware` — Serve static files
3. `SessionMiddleware` — Session management
4. `CommonMiddleware` — URL normalization
5. `CsrfViewMiddleware` — CSRF protection
6. `AuthenticationMiddleware` — User auth
7. `MessageMiddleware` — Django messages framework
8. `XFrameOptionsMiddleware` — Clickjacking protection
9. `HtmxMiddleware` — Deteksi request HTMX (`request.htmx`)
10. `AccountMiddleware` — django-allauth account handling

### Context Processors Global

Tersedia di semua template tanpa perlu pass manual dari view:

| Variable | Sumber | Isi |
|---|---|---|
| `unread_notifications_count` | `core.context_processors` | Jumlah notif belum dibaca (0 jika guest) |
| `latest_notifications` | `core.context_processors` | 5 notif terbaru user |
| `nav_categories` | `core.context_processors` | Semua kategori produk (untuk navbar) |
| `nav_brands` | `core.context_processors` | Semua brand (untuk navbar) |
| `request` | Django bawaan | Request object |
| `user` | Django auth | User yang login |
| `messages` | Django bawaan | Flash messages |

---

## 7. Model Data & Relasi

### App: `userauths`

#### `User` (extends AbstractUser)
| Field | Tipe | Keterangan |
|---|---|---|
| `id` | BigAutoField PK | — |
| `email` | EmailField unique | Login identifier utama |
| `username` | CharField | Display name |
| `phone_number` | CharField null | Nomor HP (bisa jadi login identifier) |
| `address` | TextField null | Alamat teks |
| `avatar` | ImageField null | Foto profil |
| `role` | CharField choices | `customer` / `admin_toko` / `owner` |
| `is_staff` | BooleanField | Akses Django Admin |
| `is_superuser` | BooleanField | Superuser penuh |

#### `UserProfile`
| Field | Tipe | Keterangan |
|---|---|---|
| `user` | OneToOne → User | Profil tambahan |
| `created_at` | DateTimeField auto | — |
| `updated_at` | DateTimeField auto | — |

---

### App: `products`

#### `Category`
| Field | Tipe | Keterangan |
|---|---|---|
| `name` | CharField | Nama kategori |
| `slug` | SlugField unique | URL-friendly name |
| `icon` | ImageField null | Ikon kategori |
| `order` | PositiveIntegerField | Urutan tampil |

#### `Brand`
| Field | Tipe | Keterangan |
|---|---|---|
| `name` | CharField | Nama brand (Nike, Adidas, dll.) |
| `slug` | SlugField unique | URL-friendly |
| `logo` | ImageField null | Logo brand |

#### `Product`
| Field | Tipe | Keterangan |
|---|---|---|
| `name` | CharField | Nama produk |
| `slug` | SlugField unique | URL produk (auto-generate) |
| `brand` | FK → Brand | Brand produk |
| `category` | FK → Category null | Kategori produk |
| `color` | CharField choices | Warna utama (9 pilihan) |
| `color_secondary` | CharField null | Warna sekunder opsional |
| `description` | TextField | Deskripsi produk |
| `condition` | CharField choices | `new` / `second` |
| `price` | DecimalField | Harga jual |
| `crossed_price` | DecimalField null | Harga coret (diskon) |
| `is_active` | BooleanField | Aktif/nonaktif di katalog |
| `is_featured` | BooleanField | Tampil di section "Koleksi Terpilih" |
| `created_at` | DateTimeField auto | Waktu input |

**Properties computed:**
- `average_rating` — rata-rata rating dari semua review
- `review_count` — total review
- `total_stock` — total stok semua ukuran
- `is_new` — True jika dibuat < 7 hari lalu
- `is_hot` — True jika rating ≥ 4.0 dan review ≥ 3

#### `ProductImage`
| Field | Tipe | Keterangan |
|---|---|---|
| `product` | FK → Product | Produk pemilik |
| `image` | ImageField | File foto |
| `is_primary` | BooleanField | Foto utama (tampil pertama) |
| `order` | PositiveIntegerField | Urutan galeri |

#### `ProductSize`
| Field | Tipe | Keterangan |
|---|---|---|
| `product` | FK → Product | Produk pemilik |
| `size` | CharField | Ukuran (35, 40, 42.5, dll.) |
| `stock` | PositiveIntegerField | Stok tersedia |

**Unique together:** `(product, size)` — tidak bisa duplikat ukuran per produk

**Side effect on save:** Jika total stok ≤ 2, kirim notifikasi in-app ke semua user yang mewishlist produk tersebut.

#### `Banner`
| Field | Tipe | Keterangan |
|---|---|---|
| `title` | CharField | Judul banner |
| `subtitle` | CharField null | Subjudul |
| `image` | ImageField | Gambar banner |
| `link` | URLField null | URL tujuan klik |
| `order` | PositiveIntegerField | Urutan slideshow |
| `is_active` | BooleanField | Aktif/nonaktif |

#### `Review`
| Field | Tipe | Keterangan |
|---|---|---|
| `product` | FK → Product | Produk yang diulas |
| `user` | FK → User | Penulis ulasan |
| `order_item` | OneToOne → OrderItem null | Item order terkait (untuk verifikasi) |
| `rating` | SmallIntegerField 1–5 | Bintang ulasan |
| `comment` | TextField | Teks ulasan |
| `image`, `image2`, `image3` | ImageField null | Foto bukti (max 3) |
| `is_visible` | BooleanField | Admin bisa sembunyikan |
| `created_at` | DateTimeField auto | — |

---

### App: `orders`

#### `Voucher`
| Field | Tipe | Keterangan |
|---|---|---|
| `code` | CharField unique | Kode voucher |
| `discount_type` | CharField choices | `percentage` / `nominal` |
| `discount_value` | DecimalField | Nilai diskon |
| `min_purchase` | DecimalField | Minimum belanja |
| `valid_from`, `valid_to` | DateTimeField | Masa berlaku |
| `is_active` | BooleanField | Status aktif |

#### `Wishlist`
| Field | Tipe | Keterangan |
|---|---|---|
| `user` | FK → User | Pemilik wishlist |
| `product` | FK → Product | Produk yang disimpan |
| `created_at` | DateTimeField auto | — |

**Unique together:** `(user, product)` — tidak bisa duplikat

#### `Cart`
| Field | Tipe | Keterangan |
|---|---|---|
| `user` | OneToOne → User null | Keranjang user login |
| `session_key` | CharField null | Keranjang guest (session-based) |
| `created_at`, `updated_at` | DateTimeField | — |

**Method:** `get_total_price()` — sum semua item cost

#### `CartItem`
| Field | Tipe | Keterangan |
|---|---|---|
| `cart` | FK → Cart | Cart pemilik |
| `product` | FK → Product | Produk |
| `size` | FK → ProductSize | Ukuran dipilih |
| `quantity` | PositiveIntegerField | Jumlah |

**Unique together:** `(cart, product, size)`

#### `Order`
| Field | Tipe | Keterangan |
|---|---|---|
| `user` | FK → User null | Pembeli |
| `order_number` | CharField unique | Format: `ZTP-XXXXXXXXXX` |
| `status` | CharField choices | `pending` / `paid` / `processing` / `shipped` / `delivered` / `cancelled` |
| `midtrans_transaction_id` | CharField null | Snap token Midtrans |
| `courier` | CharField | Nama ekspedisi (JNE, POS, TIKI) |
| `shipping_service` | CharField | Layanan (REG, YES, dll.) |
| `shipping_cost` | DecimalField | Ongkos kirim |
| `tracking_number` | CharField null | Nomor resi |
| `voucher` | FK → Voucher null | Voucher dipakai |
| `discount_amount` | DecimalField | Jumlah diskon |
| `subtotal` | DecimalField | Total harga item |
| `total` | DecimalField | subtotal - diskon + ongkir |

#### `OrderItem`
| Field | Tipe | Keterangan |
|---|---|---|
| `order` | FK → Order | Order induk |
| `product` | FK → Product null | Produk (bisa null jika produk dihapus) |
| `size_str` | CharField | Ukuran disimpan sebagai string (snapshot) |
| `product_name` | CharField | Nama produk saat dibeli (snapshot) |
| `price` | DecimalField | Harga saat dibeli (snapshot) |
| `quantity` | PositiveIntegerField | Jumlah |

#### `ShippingAddress`
| Field | Tipe | Keterangan |
|---|---|---|
| `order` | OneToOne → Order | Order terkait |
| `recipient_name` | CharField | Nama penerima |
| `phone_number` | CharField | No. HP penerima |
| `province_id`, `province_name` | CharField | Provinsi |
| `city_id`, `city_name` | CharField | Kota |
| `district_name` | CharField | Kecamatan |
| `postal_code` | CharField | Kode pos |
| `full_address` | TextField | Alamat lengkap |

#### `WarrantyClaim`
| Field | Tipe | Keterangan |
|---|---|---|
| `order_item` | OneToOne → OrderItem | Item yang diklaim |
| `user` | FK → User | Pengaju klaim |
| `kategori` | CharField choices | `cacat_produk` / `salah_ukuran` / `tidak_sesuai_foto` / `lainnya` |
| `reason` | TextField | Penjelasan masalah |
| `evidence_image` | ImageField | Foto bukti (wajib) |
| `status` | CharField choices | `pending` / `approved` / `rejected` / `resolved` |
| `admin_notes` | TextField null | Catatan admin |

---

### App: `core`

#### `Notification`
| Field | Tipe | Keterangan |
|---|---|---|
| `user` | FK → User | Penerima notifikasi |
| `title` | CharField | Judul notif |
| `message` | TextField | Isi notif |
| `link` | CharField null | URL tujuan saat diklik |
| `is_read` | BooleanField | Status baca |
| `created_at` | DateTimeField auto | — |

#### `FooterIcon`
| Field | Tipe | Keterangan |
|---|---|---|
| `title` | CharField | Label ikon |
| `image` | ImageField | File ikon |
| `order` | IntegerField | Urutan tampil |

---

## 8. Role & Hak Akses Pengguna

| Role | Login Via | URL Akses | Mekanisme Akses |
|---|---|---|---|
| **Guest (Pengunjung)** | — | `/` | Akses publik, tanpa login |
| **Customer (Konsumen)** | `/user/auth/` atau `/accounts/` | `/` | `is_authenticated = True`, `role = customer` |
| **Admin Toko** | `/admintoko/login/` | `/admintoko/` | User harus masuk group Django `AdminToko` |
| **Owner** | `/admin/` (Jazzmin) | `/admin/` + `/jasmine/` | `is_staff = True` dan/atau `is_superuser = True` |

### Matriks Fitur per Role

| Fitur | Guest | Customer | Admin Toko | Owner |
|---|:---:|:---:|:---:|:---:|
| Lihat beranda & katalog | ✅ | ✅ | ✅ | ✅ |
| Live search produk | ✅ | ✅ | ✅ | ✅ |
| Detail produk + ulasan | ✅ | ✅ | ✅ | ✅ |
| Daftar / Login | ✅ | — | — | — |
| Google OAuth | ✅ | — | — | — |
| Wishlist | ❌ | ✅ | — | — |
| Keranjang (guest) | ✅ | — | — | — |
| Keranjang (login) | — | ✅ | — | — |
| Checkout & bayar | ❌ | ✅ | — | — |
| Riwayat pesanan | ❌ | ✅ | — | — |
| Cetak invoice | ❌ | ✅ | — | — |
| Konfirmasi terima | ❌ | ✅ | — | — |
| Tulis ulasan | ❌ | ✅ (order selesai) | — | — |
| Klaim garansi | ❌ | ✅ (7 hari) | — | — |
| Notifikasi in-app | ❌ | ✅ | — | — |
| Edit profil | ❌ | ✅ | — | — |
| Dashboard admin | — | — | ✅ | ✅ |
| Kelola produk | — | — | ✅ | ✅ |
| Kelola pesanan | — | — | ✅ | ✅ |
| Kelola garansi | — | — | ✅ | ✅ |
| Moderasi ulasan | — | — | ✅ | ✅ |
| Lihat data pelanggan | — | — | ✅ (read-only) | ✅ |
| Dashboard analytics | — | — | — | ✅ |
| Export laporan Excel | — | — | — | ✅ |
| Kelola akun admin | — | — | — | ✅ |
| Django Admin penuh | — | — | — | ✅ |

---

## 9. Peta URL Lengkap

### Storefront (App: `storefront`)
| URL | View | Nama | Keterangan |
|---|---|---|---|
| `/` | `home_view` | `storefront:home` | Beranda |
| `/katalog/` | `catalog_view` | `storefront:catalog` | Katalog produk |
| `/produk/<slug>/` | `product_detail_view` | `storefront:product_detail` | Detail produk |
| `/live-search/` | `live_search_view` | `storefront:live_search` | HTMX live search partial |

### Auth & Profil (App: `userauths`)
| URL | View | Nama | Keterangan |
|---|---|---|---|
| `/user/auth/` | `auth_main` | `userauths:auth_main` | Halaman login/register |
| `/user/auth-check/` | `auth_check` | — | HTMX: cek email/HP → arah ke login/register |
| `/user/login/` | `auth_login` | `userauths:auth_login` | HTMX: POST login |
| `/user/register/` | `auth_register` | `userauths:auth_register` | HTMX: POST register |
| `/user/logout/` | `auth_logout` | `userauths:auth_logout` | Logout |
| `/user/profile/` | `auth_profile` | `userauths:profile` | Profil customer |
| `/accounts/...` | allauth URLs | — | Google OAuth, password reset |

### Pesanan & Transaksi (App: `orders`, prefix `/pesanan/`)
| URL | View | Nama | Keterangan |
|---|---|---|---|
| `/pesanan/wishlist/` | `wishlist_view` | `orders:wishlist` | Halaman wishlist |
| `/pesanan/wishlist/toggle/<id>/` | `toggle_wishlist` | `orders:toggle_wishlist` | HTMX: toggle wishlist |
| `/pesanan/cart/` | `cart_view` | `orders:cart_page` | Halaman keranjang |
| `/pesanan/cart/add/<id>/` | `add_to_cart` | `orders:add_to_cart` | HTMX: tambah ke cart |
| `/pesanan/cart/update/<id>/` | `update_cart_item` | `orders:update_cart_item` | HTMX: update qty |
| `/pesanan/cart/remove/<id>/` | `remove_cart_item` | `orders:remove_cart_item` | HTMX: hapus item |
| `/pesanan/cart/drawer/` | `cart_drawer` | `orders:cart_drawer` | HTMX: buka cart drawer |
| `/pesanan/cart/count/` | `cart_count` | `orders:cart_count` | HTMX: badge count cart |
| `/pesanan/checkout/` | `checkout_view` | `orders:checkout` | Halaman checkout |
| `/pesanan/api/provinces/` | `get_provinces_options` | `orders:get_provinces_options` | HTMX: dropdown provinsi |
| `/pesanan/api/cities/` | `get_cities` | `orders:get_cities` | HTMX: dropdown kota |
| `/pesanan/api/shipping-cost/` | `get_shipping_cost` | `orders:get_shipping_cost` | HTMX: opsi ongkir |
| `/pesanan/api/update-total/` | `update_total` | `orders:update_total` | HTMX: update total harga |
| `/pesanan/api/apply-voucher/` | `apply_voucher` | — | HTMX: terapkan voucher |
| `/pesanan/checkout/success/<order_number>/` | `checkout_success` | `orders:checkout_success` | Halaman sukses bayar |
| `/pesanan/midtrans/webhook/` | `midtrans_webhook` | `orders:midtrans_webhook` | Webhook Midtrans (no CSRF) |
| `/pesanan/history/<order_number>/` | `order_detail_view` | `orders:order_detail` | Detail pesanan |
| `/pesanan/history/<order_number>/check-status/` | `manual_check_payment_status` | `orders:check_payment_status` | Cek status ke Midtrans |
| `/pesanan/history/<order_number>/invoice/` | `print_invoice` | `orders:print_invoice` | Cetak invoice |
| `/pesanan/history/<order_number>/complete/` | `complete_order` | `orders:complete_order` | Konfirmasi terima pesanan |
| `/pesanan/item/<id>/review/` | `create_review` | `orders:create_review` | Form tulis ulasan |
| `/pesanan/item/<id>/warranty/` | `create_warranty_claim` | `orders:create_warranty_claim` | Form klaim garansi |
| `/pesanan/garansi/<claim_id>/` | `warranty_tracking` | `orders:warranty_tracking` | Tracking klaim garansi |

### Core (App: `core`, prefix `/core/`)
| URL | View | Keterangan |
|---|---|---|
| `/core/notifications/` | `all_notifications` | Semua notifikasi user |
| `/core/notifications/mark-read/` | `mark_notifications_read` | Tandai semua dibaca |
| `/core/notifications/count/` | `notification_count` | HTMX: badge count notif |

### Admin Toko (App: `admintoko`, prefix `/admintoko/`)
| URL | View | Keterangan |
|---|---|---|
| `/admintoko/login/` | `login_view` | Login admin toko |
| `/admintoko/` | `dashboard_view` | Dashboard admin |
| `/admintoko/products/` | `products_view` | Daftar produk |
| `/admintoko/products/add/` | `product_create_view` | Tambah produk |
| `/admintoko/products/<id>/edit/` | `product_edit_view` | Edit produk |
| `/admintoko/products/<id>/toggle/` | `product_toggle_view` | Aktif/nonaktif produk |
| `/admintoko/category/add/` | `category_create_view` | Tambah kategori |
| `/admintoko/brand/add/` | `brand_create_view` | Tambah brand |
| `/admintoko/categories/` | `categories_view` | Daftar kategori |
| `/admintoko/brands/` | `brands_view` | Daftar brand |
| `/admintoko/orders/` | `orders_view` | Daftar pesanan |
| `/admintoko/orders/<id>/update/` | `order_update_status` | Update status pesanan |
| `/admintoko/warranty/` | `warranty_view` | Daftar klaim garansi |
| `/admintoko/warranty/<id>/update/` | `warranty_update_status` | Update status klaim |
| `/admintoko/reviews/` | `reviews_view` | Daftar ulasan |
| `/admintoko/reviews/<id>/toggle/` | `review_toggle_view` | Tampil/sembunyikan ulasan |
| `/admintoko/customers/` | `customers_view` | Daftar pelanggan |

### Django Admin & Owner
| URL | Keterangan |
|---|---|
| `/admin/` | Django Admin (Jazzmin UI) — superuser |
| `/admin/export-excel/` | Export laporan Excel |
| `/admin/analytics/` | API analytics JSON untuk dashboard Jazzmin |

---

## 10. Fitur & Halaman Storefront

### 10.1 Beranda — `GET /`

**Template:** `storefront/home.html`

**Data yang dikirim view:**
- `banners` — Banner aktif, urut by `order`
- `bestseller_products` — 10 produk dengan total penjualan tertinggi (annotate Sum)
- `new_products` — 10 produk terbaru
- `hot_items` — 8 produk dengan average rating ≥ 4.5
- `brands` — Semua brand untuk strip
- `categories` — Semua kategori
- `wishlist_product_ids` — ID produk yang di-wishlist user (jika login)

**Komponen UI:**
1. **Hero Carousel** — Slideshow full-width, auto-slide 5 detik, overlay gelap, tombol CTA "Lihat Koleksi", numbered bullet navigation
2. **Trust Badge Strip** — Banner horizontal: Garansi Puas · 7 Hari Return · Free Ongkir · 100% Authentic · Koleksi Terlengkap
3. **Brand Scroll Strip** — Logo brand dengan horizontal scroll
4. **Section "KOLEKSI TERPILIH"** — Produk `is_featured=True`
5. **Section "TERLARIS"** — `bestseller_products` (annotate total sold)
6. **Section "HOT ITEMS"** — Produk rating ≥ 4.5
7. **Section "BARU MASUK"** — `new_products` ordered by `-created_at`
8. **Footer** — Info toko, links, ikon payment/ekspedisi

---

### 10.2 Katalog Produk — `GET /katalog/`

**Template:** `storefront/katalog.html` / `storefront/partials/product_grid.html` (HTMX)

**Filter yang didukung (query params):**
| Param | Contoh | Keterangan |
|---|---|---|
| `q` | `?q=nike` | Full-text search nama produk |
| `brand` | `?brand=1` | Filter by brand ID |
| `category` | `?category=2` | Filter by kategori ID atau nama |
| `color` | `?color=black,white` | Filter warna (multi, comma-separated) |
| `size` | `?size=40,41` | Filter ukuran (multi, comma-separated) |
| `condition` | `?condition=new` | Filter kondisi: `new` / `second` |
| `sort` | `?sort=newest` | Sort: `newest`, `hot`, `featured`, `price`, `-price`, `-created_at` |
| `page` | `?page=2` | Pagination (12 item/halaman) |

**Komponen UI:**
- Filter sidebar: brand (checkbox), ukuran (pill toggle), kondisi (radio), warna (swatch), tombol reset filter
- Search bar HTMX live dengan debounce 300ms → partial reload `product_grid.html`
- Sort dropdown
- Grid produk: 4 kolom desktop / 2 kolom mobile
- Product card: foto, badge NEW/HOT/SOLD OUT, nama, harga coret + harga, brand, tombol wishlist (HTMX)
- Infinite scroll via HTMX `hx-trigger="revealed"` pada sentinel element

---

### 10.3 Detail Produk — `GET /produk/<slug>/`

**Template:** `storefront/detail.html`

**Data yang dikirim:**
- `product` — objek produk lengkap dengan relasi images, sizes, reviews
- `related_products` — 4 produk brand sama, bukan produk ini
- `rating_distribution` — dict `{5: 60%, 4: 20%, ...}` (dalam persentase)
- `wishlist_product_ids` — untuk state ikon heart

**Komponen UI:**
- Galeri foto: foto utama besar + row thumbnail (klik ganti foto utama via JS)
- Info produk: brand badge, nama (h1), rata-rata rating bintang + count, harga coret + harga aktif
- Pilih ukuran: tombol per ukuran, stok tampil per ukuran, disabled jika stok 0
- Tombol "Tambah ke Keranjang" (POST HTMX, size required) + toast notifikasi
- Tombol "Simpan ke Wishlist" (HTMX toggle, ikon berubah merah)
- Tab: **Deskripsi** | **Ulasan (n)** | **Garansi & Return**
- Tab Ulasan: distribusi rating bar, list review dengan foto, rating bintang, nama user (disamarkan), tanggal
- Section produk terkait: 4 card brand sama

---

### 10.4 Live Search — `GET /live-search/`

**Template:** `storefront/partials/search_results.html`

- Dipanggil via HTMX dari navbar saat user mengetik (debounce 300ms)
- Mengembalikan max 5 produk dalam dropdown
- Kosong jika query < 1 karakter

---

### 10.5 Autentikasi — `GET /user/auth/`

**Template:** `userauths/auth_main.html`

**Alur progresif (HTMX-driven):**
1. User masukkan email atau nomor HP → POST `/user/auth-check/`
2. Sistem cek: user exist? → arahkan ke form **password** (login) atau form **detail registrasi**
3. Login: POST `/user/login/` → `HX-Redirect: /`
4. Register: POST `/user/register/` → otomatis login → `HX-Redirect: /`

**Fitur tambahan:**
- Login dengan Google OAuth via `django-allauth` → `/accounts/google/login/`
- Lupa password: allauth forgot password flow → `/accounts/password/reset/`
- Setelah login: guest cart otomatis di-merge ke user cart (`merge_guest_cart`)

---

### 10.6 Profil — `GET /user/profile/`

**Template:** `userauths/profile.html`

**Fitur:**
- Edit: username, phone_number, address, avatar (upload foto)
- Riwayat pesanan singkat (semua order user)
- Ganti password via link ke allauth

---

### 10.7 Wishlist — `GET /pesanan/wishlist/`

**Template:** `orders/wishlist.html`

- Grid produk yang di-wishlist user
- Hapus dari wishlist: HTMX toggle → item hilang dari DOM tanpa reload
- Notifikasi stok menipis jika total stok produk ≤ 2

---

### 10.8 Keranjang — `GET /pesanan/cart/`

**Template:** `orders/cart.html`

**Fitur:**
- Keranjang persisten: user → DB; guest → session key
- List item: foto mini, nama, ukuran, harga satuan, qty, total per item
- Update qty: +/- HTMX (min 1, max sesuai stok) → `HX-Trigger: cartUpdated`
- Hapus item: HTMX DELETE → refresh cart
- Cart drawer: slide-in panel dari kanan (HTMX load `/pesanan/cart/drawer/`)
- Badge count di navbar: auto-update via `hx-trigger="cartUpdated from:body"`
- Ringkasan: subtotal, tombol checkout

---

### 10.9 Checkout — `GET/POST /pesanan/checkout/`

**Template:** `orders/checkout.html`

**Alur multi-step (satu halaman, step toggle JS):**

**Step 1 — Alamat:**
- Input: nama penerima, nomor telepon
- Dropdown chained via HTMX: Provinsi → `/api/provinces/` → Kota → `/api/cities/?province_id=X`
- Input: nama kecamatan, kode pos, alamat detail lengkap

**Step 2 — Pengiriman:**
- Trigger HTMX ke `/api/shipping-cost/?city_id=X` saat kota dipilih
- Loading spinner selama kalkulasi RajaOngkir
- List radio button per opsi ekspedisi: nama kurir, layanan, estimasi hari, harga
- Pilih opsi → HTMX ke `/api/update-total/` → update ringkasan total

**Step 3 — Pembayaran:**
- Input kode voucher: HTMX POST → `/api/apply-voucher/` → tampil pesan diskon
- Ringkasan: item list, subtotal, diskon (jika ada), ongkir, total akhir
- Tombol "Bayar Sekarang" → trigger Midtrans Snap popup (JS)

**Saat POST checkout berhasil:**
1. Validasi stok tersedia untuk semua item
2. Buat `Order` dengan status `pending`
3. Buat `OrderItem` per item + kurangi stok (booking stock)
4. Buat `ShippingAddress`
5. Generate Midtrans Snap token
6. Clear cart + hapus voucher dari session
7. Redirect ke `/pesanan/checkout/success/<order_number>/`

---

### 10.10 Sukses Pembayaran — `/pesanan/checkout/success/<order_number>/`

**Template:** `orders/checkout_success.html`

- Tampil ringkasan pesanan
- Tombol "Bayar Sekarang" jika status masih `pending` (trigger Snap popup ulang)
- Midtrans Snap popup via JavaScript SDK

---

### 10.11 Riwayat Pesanan (dari Profil)

Akses melalui `/user/profile/` — list pesanan user di halaman profil.

**Detail Pesanan — `/pesanan/history/<order_number>/`**

**Template:** `orders/detail.html`

**Komponen:**
- Timeline horizontal status: Dibayar → Diproses → Dikirim → Selesai (dengan warna/ikon per step)
- Info pengiriman: nama, alamat, ekspedisi, nomor resi
- Daftar item yang dibeli (nama snapshot, ukuran snapshot, harga snapshot)
- Ringkasan biaya: subtotal, diskon, ongkir, total
- Tombol kondisional berdasarkan status:
  - `pending` → "Bayar Sekarang" (Midtrans Snap) + "Cek Status Pembayaran"
  - `shipped` → "Pesanan Sudah Diterima" (POST `/complete/`)
  - `completed` (tiap item belum direview) → "Tulis Ulasan"
  - `completed` (garansi masih berlaku ≤ 7 hari) → "Laporkan Masalah"
- Tombol "Cetak Invoice"

---

### 10.12 Form Ulasan — `/pesanan/item/<id>/review/`

**Template:** `orders/review_form.html`

**Guard:**
- Order harus berstatus `completed`
- Item belum pernah direview (OneToOne `order_item`)

**Form:**
- Rating bintang interaktif (klik 1–5, radio button tersembunyi)
- Textarea komentar
- Upload foto: image, image2, image3 (optional, validasi `validate_image_file`)

---

### 10.13 Form Klaim Garansi — `/pesanan/item/<id>/warranty/`

**Template:** `orders/warranty_form.html`

**Guard:**
- Order berstatus `completed`
- Dalam 7 hari sejak order selesai (`order.updated_at`)
- Belum pernah klaim (OneToOne `order_item`)

**Form:**
- Dropdown kategori masalah: Cacat Produk / Salah Ukuran / Tidak Sesuai Foto / Lainnya
- Textarea alasan/deskripsi masalah
- Upload foto bukti (wajib, 1 file, validasi image)

---

### 10.14 Tracking Garansi — `/pesanan/garansi/<claim_id>/`

**Template:** `orders/warranty_tracking.html`

- Tampil status klaim: Menunggu → Disetujui/Ditolak → Selesai
- Catatan dari admin jika ada
- Tombol "Chat dengan CS" (buka Crisp widget)

---

### 10.15 Halaman Informasi Statis

| URL (perlu dikonfigurasi) | Template | Isi |
|---|---|---|
| `/tentang/` | `pages/about.html` | Tentang ZTP Sneakers |
| `/kontak/` | `pages/contact.html` | Form kontak + peta |
| `/faq/` | `pages/faq.html` | FAQ accordion |
| `/keaslian/` | `pages/authenticity.html` | Jaminan keaslian produk |
| `/privasi/` | `pages/privacy.html` | Kebijakan privasi |
| `/return/` | `pages/return_policy.html` | Kebijakan pengembalian |

---

## 11. Fitur & Halaman Admin Toko

**Base URL:** `/admintoko/`
**Akses:** User harus masuk Django Group `AdminToko`
**Guard function:** `is_admin_toko(user)` — decorator `@user_passes_test`

### 11.1 Login Admin — `/admintoko/login/`

**Template:** `admintoko/login.html`

- Form email + password
- Fallback auth: cek `email` field karena AUTH_USER_MODEL menggunakan email
- Redirect ke dashboard jika sudah login

---

### 11.2 Dashboard Admin — `/admintoko/`

**Template:** `admintoko/dashboard.html`

**KPI yang ditampilkan:**
- Total pesanan hari ini
- Pesanan `pending` hari ini (belum dibayar)
- Pesanan `paid` hari ini (sudah bayar, perlu diproses)
- Klaim garansi baru (`status=pending`)
- Daftar `ProductSize` dengan stok ≤ 2 (stok menipis)

---

### 11.3 Manajemen Produk — `/admintoko/products/`

**Template:** `admintoko/products.html`

- Tabel semua produk: foto, nama, brand, harga, stok total, status aktif
- Tombol Tambah, Edit, Aktif/Nonaktifkan

**Tambah/Edit Produk — `/admintoko/products/add/` | `.../<id>/edit/`**

**Template:** `admintoko/product_form.html`

- Form: nama, brand (dropdown), kategori (dropdown), harga, deskripsi, kondisi
- Stok per ukuran: tambah/hapus baris dinamis (JS)
- Edit: size yang tidak dikirim di-set stok 0 (tidak dihapus)

**Toggle Aktif — POST `/admintoko/products/<id>/toggle/`**
- Flip `is_active` — produk nonaktif tidak tampil di katalog

---

### 11.4 Kategori & Brand

| URL | Template | Fungsi |
|---|---|---|
| `/admintoko/categories/` | `admintoko/categories.html` | List kategori |
| `/admintoko/category/add/` | `admintoko/category_form.html` | Tambah kategori |
| `/admintoko/brands/` | `admintoko/brands.html` | List brand |
| `/admintoko/brand/add/` | `admintoko/brand_form.html` | Tambah brand |

---

### 11.5 Manajemen Pesanan — `/admintoko/orders/`

**Template:** `admintoko/orders.html`

- Filter status: `all` / `pending` / `paid` / `processing` / `shipped` / `delivered` / `cancelled`
- Tabel pesanan: nomor order, customer, tanggal, total, status, aksi

**Update Status Pesanan — POST `/admintoko/orders/<id>/update/`**
- Input: `status` (dropdown) + `tracking_number` (opsional, wajib saat `shipped`)
- Perubahan status otomatis trigger `order_status_changed` signal → kirim notifikasi in-app ke customer

---

### 11.6 Klaim Garansi — `/admintoko/warranty/`

**Template:** `admintoko/warranty.html`

- Daftar semua klaim: item, customer, kategori, status, tanggal
- Lihat foto bukti

**Update Status Garansi — POST `/admintoko/warranty/<id>/update/`**
- Input: `status` baru + `admin_notes`
- Otomatis kirim notifikasi ke customer via signal

---

### 11.7 Moderasi Ulasan — `/admintoko/reviews/`

**Template:** `admintoko/reviews.html`

- Daftar semua ulasan: produk, customer, rating, komentar, foto, status visibilitas

**Toggle Visibilitas — POST `/admintoko/reviews/<id>/toggle/`**
- Flip `is_visible` — ulasan tersembunyi tidak tampil di halaman detail produk

---

### 11.8 Data Pelanggan — `/admintoko/customers/`

**Template:** `admintoko/customers.html`

- Daftar user dengan `is_staff=False` dan `is_superuser=False` (customer saja)
- Data: nama, email, nomor HP, tanggal daftar
- Read-only — tidak ada aksi edit/hapus dari panel ini

---

## 12. Fitur & Halaman Owner / Jasmine

**Akses:** Via Django Admin (`/admin/`) dengan akun `is_staff=True` atau `is_superuser=True`

**Dashboard Jazzmin** menggunakan template kustom (`templates/admin/index.html`) yang memuat widget analytics melalui AJAX call ke `/admin/analytics/`.

### 12.1 Dashboard Analytics — `/admin/analytics/` (JSON API)

**View:** `orders.admin_views.dashboard_analytics_api`

**Data yang dikembalikan (JSON):**

```json
{
  "kpis": {
    "total_revenue_month": 15000000,
    "total_orders": 234,
    "new_customers": 12,
    "top_products": [{"name": "Nike Air Max", "sold": 45}]
  },
  "chart": {
    "labels": ["10 Jun - 16 Jun", "17 Jun - 23 Jun"],
    "data": [5.2, 8.7]
  },
  "heatmap": [{"x": "Mon", "y": "14:00", "v": 3}],
  "recent_orders": [{"order_number": "ZTP-ABC", "user": "...", "total": 500000}]
}
```

**Visualisasi di dashboard:**
- 4 KPI cards: Revenue Bulan Ini, Total Pesanan, Customer Baru, Produk Terlaris
- Grafik penjualan Chart.js: data 4 minggu terakhir (dalam juta Rp)
- Heatmap pesanan: hari × jam
- Tabel penjualan terbaru (10 terakhir)

### 12.2 Export Laporan Excel — `/admin/export-excel/`

**View:** `orders.admin_export.export_excel_admin_view`

- Filter: bulan + tahun
- Generate file `.xlsx` menggunakan `openpyxl`
- Data: nomor order, customer, produk, total, status, tanggal
- Download langsung dari browser

---

## 13. Alur Bisnis Utama

### 13.1 Alur Pembelian (Happy Path)

```
Guest / Customer
      │
      ▼
[Beranda / Katalog]
      │ Klik produk
      ▼
[Detail Produk]
      │ Pilih ukuran → klik "Tambah ke Keranjang"
      │ (Guest: simpan ke session; Login: simpan ke DB)
      ▼
[Keranjang]
      │ Review item → klik "Checkout"
      │ (Redirect ke /user/auth/ jika belum login)
      ▼
[Checkout — Step 1: Alamat]
      │ Isi nama, HP, pilih provinsi → kota (HTMX chained)
      ▼
[Checkout — Step 2: Pengiriman]
      │ HTMX load ongkir dari RajaOngkir → pilih opsi
      ▼
[Checkout — Step 3: Pembayaran]
      │ (Opsional: pakai voucher)
      │ Total otomatis diupdate → klik "Bayar Sekarang"
      ▼
[Midtrans Snap Popup]
      │ Pilih metode bayar (VA BCA/Mandiri/BNI, DANA, OVO, GoPay)
      │ Bayar
      ▼
[Midtrans Webhook → POST /pesanan/midtrans/webhook/]
      │ Verifikasi signature hash SHA-512
      │ status=settlement → Order.status = 'paid'
      │ Signal: Notification "Pembayaran Berhasil" → customer
      ▼
[Admin Toko proses pesanan]
      │ Admin ubah status → 'processing' → Signal notif customer
      │ Admin input resi → ubah status → 'shipped' → Signal notif customer
      ▼
[Customer konfirmasi terima]
      │ Klik "Pesanan Sudah Diterima" di detail pesanan
      │ Order.status = 'completed'
      │ Signal: Notification "Pesanan Selesai" + ajak tulis ulasan
      ▼
[Pasca Pembelian — Opsional]
      ├── Tulis ulasan (jika belum, dalam waktu kapan saja)
      └── Klaim garansi (dalam 7 hari sejak completed)
```

---

### 13.2 Alur Pembatalan & Rollback Stok

```
Midtrans Webhook
      │ status = 'deny' / 'cancel' / 'expire'
      ▼
Order.status = 'cancelled'
      │
      ▼
Loop OrderItem → ProductSize.stock += item.quantity
(Stok dikembalikan)
      │
      ▼
Signal: Notification "Pesanan Dibatalkan" → customer
```

---

### 13.3 Alur Klaim Garansi

```
Customer
      │ Buka detail pesanan (status: completed, ≤ 7 hari)
      │ Klik "Laporkan Masalah" pada item
      ▼
[Form Klaim Garansi]
      │ Pilih kategori, isi alasan, upload foto bukti
      │ POST → buat WarrantyClaim (status: pending)
      ▼
Signal: post_save → Notification "Klaim Diterima" → customer
      │
      ▼
[Admin Toko: /admintoko/warranty/]
      │ Review klaim + foto bukti
      │ Ubah status: approved / rejected
      │ Isi admin_notes
      ▼
Signal: pre_save status changed
      → Notification ke customer (Disetujui / Ditolak)
      │
      ▼
(Jika approved) Admin proses → ubah status: resolved
      │
      ▼
Signal → Notification "Selesai" → customer
```

---

### 13.4 Alur Notifikasi Stok Menipis (Wishlist)

```
Admin simpan ProductSize (stok update)
      │
ProductSize.save() override
      │ Hitung total_stock semua ukuran produk
      │
      ▼
Jika total_stock ≤ 2:
      │ Query semua Wishlist entry untuk produk ini
      │ Untuk tiap user:
      │   Cek tidak ada notif "Stok Hampir Habis!" yang belum dibaca
      │   Buat Notification baru → user
```

---

### 13.5 Alur Merge Cart Guest → User

**Dipicu:** Signal `user_logged_in` dari `django.contrib.auth`

```
User berhasil login
      │
Signal: user_logged_in → merge_guest_cart(request, user)
      │
      ▼
Cari Cart dengan session_key = request.session.session_key, user=None
      │ Tidak ada guest cart → return
      │
      ▼
Ambil atau buat Cart untuk user yang login
      │
Loop guest CartItem:
      │ Cek apakah item (product+size) sudah ada di user cart
      │   Ya → tambah qty (max = stok tersedia)
      │   Tidak → pindahkan item
      │
Delete guest CartItem + guest Cart
```

---

## 14. Integrasi Pihak Ketiga

### 14.1 Midtrans Payment Gateway

**Library:** `midtransclient==1.4.2`

**Konfigurasi:**
```python
MIDTRANS_SERVER_KEY = os.getenv('MIDTRANS_SERVER_KEY')
MIDTRANS_CLIENT_KEY = os.getenv('MIDTRANS_CLIENT_KEY')
MIDTRANS_IS_PRODUCTION = False  # True di production
```

**Alur:**
1. Saat checkout → `generate_midtrans_snap_token(order)` → return Snap token
2. Token disimpan di `order.midtrans_transaction_id`
3. Frontend: `window.snap.pay(token)` → popup pembayaran
4. Midtrans kirim webhook ke `/pesanan/midtrans/webhook/`
5. Verifikasi: `SHA-512(order_id + status_code + gross_amount + server_key)` == `signature_key`
6. Update `order.status` berdasarkan `transaction_status`

**Metode pembayaran tersedia (Midtrans Sandbox):**
- Virtual Account: BCA, Mandiri, BNI, BRI
- E-Wallet: DANA, OVO, GoPay, ShopeePay
- QRIS
- Alfamart / Indomaret (convenience store)

**Fallback:** Jika token gagal dibuat saat checkout, user tetap bisa generate ulang token di halaman detail pesanan (`order_detail_view`).

---

### 14.2 RajaOngkir (Komerce API v1)

**Base URL:** `https://rajaongkir.komerce.id/api/v1/`

**Konfigurasi:**
```python
RAJAONGKIR_API_KEY = os.getenv('RAJAONGKIR_API_KEY')
```

**Endpoint yang digunakan:**
| Endpoint | Method | Fungsi |
|---|---|---|
| `/destination/province` | GET | Daftar semua provinsi |
| `/destination/city/{province_id}` | GET | Daftar kota per provinsi |
| `/calculate/domestic-cost` | POST | Kalkulasi ongkir |

**Caching:** Data provinsi dan kota di-cache di Django cache framework (24 jam) untuk mengurangi API calls.

**Fallback:** Jika API gagal (timeout/error), sistem mengembalikan list hardcoded kota-kota utama Jawa.

**Origin kota pengiriman:** Jakarta Pusat (ID: `152`) — default hardcoded.

**Ekspedisi yang didukung:** JNE, POS, TIKI

---

### 14.3 Google OAuth (django-allauth)

**Konfigurasi:**
```python
INSTALLED_APPS = ['allauth', 'allauth.account', 'allauth.socialaccount', 'allauth.socialaccount.providers.google']
ACCOUNT_LOGIN_METHODS = {'email'}
ACCOUNT_SIGNUP_FIELDS = ['email*', 'password1*', 'password2*']
ACCOUNT_EMAIL_VERIFICATION = 'none'
```

**Alur:**
1. User klik "Login dengan Google" → `/accounts/google/login/`
2. Redirect ke Google consent screen
3. Callback → allauth buat atau ambil user → login
4. Signal `user_logged_in` → merge guest cart

---

### 14.4 Crisp Live Chat

Widget JavaScript embed di semua halaman storefront. Token dikonfigurasi via variabel template atau hardcode di `base.html`.

---

## 15. Sistem Notifikasi & Signal

### 15.1 Django Signals (`orders/signals.py`)

#### Signal 1: `order_status_changed` (pre_save Order)

Dipicu setiap kali `Order.status` berubah.

| Status Baru | Judul Notif | Isi |
|---|---|---|
| `paid` | Pembayaran Berhasil | Pembayaran untuk pesanan {number} telah berhasil. |
| `processing` | Pesanan Diproses | Pesanan {number} sedang kami siapkan. |
| `shipped` | Pesanan Dikirim 📦 | Dikirim via {kurir}. No Resi: {resi} |
| `completed` | Pesanan Selesai ⭐ | Terima kasih! Yuk, berikan ulasanmu! |
| `cancelled` | Pesanan Dibatalkan | Pesanan {number} telah dibatalkan. |

Link notif → detail pesanan `/pesanan/history/{order_number}/`

#### Signal 2: `warranty_status_changed` (pre_save WarrantyClaim)

| Status Baru | Judul Notif |
|---|---|
| `approved` | Klaim Garansi Disetujui ✅ |
| `rejected` | Klaim Garansi Ditolak |
| `resolved` | Klaim Garansi Selesai ✅ |

#### Signal 3: `warranty_created` (post_save WarrantyClaim, `created=True`)

Dikirim ke customer saat klaim pertama dibuat:
- Judul: "Klaim Garansi Diterima 🛡️"
- Link → tracking garansi

#### Signal 4: `merge_cart_on_login` (user_logged_in)

Trigger `merge_guest_cart(request, user)` otomatis saat login.

### 15.2 Notifikasi dari ProductSize.save()

Notifikasi stok menipis dikirim ke semua user yang mewishlist produk jika total stok ≤ 2.
Duplikasi dicegah: cek apakah sudah ada notif dengan judul & pesan sama yang belum dibaca.

### 15.3 HTMX Notification Badge

- URL: `/core/notifications/count/`
- Di-polling via `hx-trigger="every 30s"` di navbar
- Mengembalikan HTML badge animasi jika ada notif belum dibaca

---

## 16. Konfigurasi & Environment

### File `.env` (dari `.env.example`)

```env
# ── Django Core ──────────────────────────────────────
SECRET_KEY=your-django-secret-key
DEBUG=True

# ── Database PostgreSQL ───────────────────────────────
DB_NAME=db_ztpsneakers
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

# ── Midtrans Payment Gateway ──────────────────────────
MIDTRANS_SERVER_KEY=Mid-server-xxxxxxxxxxxxxxxxxxxx
MIDTRANS_CLIENT_KEY=Mid-client-xxxxxxxxxxxxxxxxxxxx
MIDTRANS_IS_PRODUCTION=False

# ── RajaOngkir API ────────────────────────────────────
RAJAONGKIR_API_KEY=your_rajaongkir_api_key
```

### Django Settings Penting

| Setting | Nilai | Keterangan |
|---|---|---|
| `AUTH_USER_MODEL` | `userauths.User` | Custom user model |
| `LOGIN_URL` | `/auth/` | Redirect jika belum login |
| `LOGIN_REDIRECT_URL` | `/` | Setelah login |
| `LOGOUT_REDIRECT_URL` | `/` | Setelah logout |
| `SITE_ID` | `1` | Django Sites framework (allauth) |
| `ACCOUNT_LOGIN_METHODS` | `{'email'}` | Login pakai email |
| `ACCOUNT_EMAIL_VERIFICATION` | `'none'` | Tidak perlu verifikasi email |
| `ACCOUNT_LOGOUT_ON_GET` | `True` | Logout langsung via GET |
| `ALLOWED_HOSTS` | `['*']` | Perlu dikunci di production |
| `TIME_ZONE` | `'UTC'` | Timezone server |
| `LANGUAGE_CODE` | `'en-us'` | Default language |

### Jazzmin Admin Customization

```python
JAZZMIN_SETTINGS = {
    "site_title": "ZTP Sneakers Admin",
    "site_header": "ZTP Sneakers Dashboard",
    "site_brand": "ZTP Sneakers",
    "site_logo": "assets/images/ztppng.png",
    "theme": "flatly",
    "custom_css": "assets/css/jazzmin-custom.css",
}
```

### Static & Media Files

| Konfigurasi | Nilai | Keterangan |
|---|---|---|
| `STATIC_URL` | `/static/` | URL static files |
| `STATICFILES_DIRS` | `[BASE_DIR / 'static']` | Sumber static |
| `STATIC_ROOT` | `BASE_DIR / 'staticfiles'` | Output `collectstatic` |
| `MEDIA_URL` | `/media/` | URL file upload |
| `MEDIA_ROOT` | `BASE_DIR / 'media'` | Penyimpanan upload |

WhiteNoise melayani static files tanpa web server tambahan (cocok untuk cPanel).

### Perintah Management Penting

```bash
# Migrasi database
python manage.py migrate

# Isi data awal (kategori, brand, produk sample, user demo)
python seed.py

# Buat superuser
python manage.py createsuperuser

# Kumpulkan static files (production)
python manage.py collectstatic

# Django shell
python manage.py shell
```

---

## Ringkasan Relasi Antar Entitas

| Dari | Ke | Tipe | Keterangan |
|---|---|---|---|
| User | UserProfile | 1:1 | Profil tambahan |
| Brand | Product | 1:N | Satu brand → banyak produk |
| Category | Product | 1:N | Satu kategori → banyak produk |
| Product | ProductImage | 1:N | Satu produk → banyak foto |
| Product | ProductSize | 1:N | Satu produk → banyak ukuran+stok |
| Product | Review | 1:N | Satu produk → banyak ulasan |
| User | Review | 1:N | Satu user → banyak ulasan |
| OrderItem | Review | 1:1 | Satu item → maks. 1 ulasan |
| User | Cart | 1:1 | Satu user → satu keranjang |
| Cart | CartItem | 1:N | Satu cart → banyak item |
| User | Wishlist | 1:N | Satu user → banyak wishlist |
| User | Order | 1:N | Satu user → banyak order |
| Voucher | Order | 1:N | Satu voucher → banyak order |
| Order | OrderItem | 1:N | Satu order → banyak item |
| Order | ShippingAddress | 1:1 | Satu order → satu alamat kirim |
| OrderItem | WarrantyClaim | 1:1 | Satu item → maks. 1 klaim garansi |
| User | Notification | 1:N | Satu user → banyak notifikasi |

---

*Dokumen ini digenerate dari analisis kode sumber project ZTP Sneakers B2C.*
*Diperbarui: Juni 2026*
