# UIUX FLOW — ZTP Sneakers B2C Platform

> Referensi visual: **807garage.com** — dark, premium, street culture  
> Wajib dibaca bersama `PRD.md` dan `TASK.md` sebelum membuat tampilan apapun

---

## 1. Design System

### Palet Warna

```
/* === BASE (Storefront & Admin Toko) === */
--bg-base:        #FFFFFF;    /* background utama */
--bg-surface:     #F9F9F9;    /* card, modal, sidebar */
--bg-elevated:    #F0F0F0;    /* hover, dropdown */
--border-subtle:  #E5E5E5;    /* border default */
--border-active:  #CCCCCC;    /* border hover */

--text-primary:   #000000;    /* teks utama */
--text-secondary: #666666;    /* teks muted */
--text-hint:      #999999;    /* placeholder, hint */

--accent-black:   #000000;    /* CTA utama — minimalis/premium */
--accent-red:     #E53935;    /* flash sale, error, sold out */
--success:        #2E7D32;
--warning:        #F57C00;
--info:           #1565C0;

/* === JASMINE (Owner Dashboard) === */
--jasmine-bg:     #F5F5F5;    
--jasmine-gold:   #D4AF37;    /* aksen emas/premium */
--jasmine-surface:#FFFFFF;
```

### Tipografi

```
Font Display (heading): 'Space Grotesk', sans-serif
Font Body:              'Inter', sans-serif

/* Import via Google Fonts di base.html */

Hierarki:
  h1: 48–64px, weight 700 (hero)
  h2: 32–40px, weight 700 (section title)
  h3: 24px, weight 600
  h4: 18–20px, weight 600
  body: 14–16px, weight 400
  caption/badge: 12px, weight 500
```

### Komponen Dasar

```
/* Button Utama (CTA) */
.btn-primary {
  background: #000000;
  color: #FFFFFF;
  font-weight: 600;
  border-radius: 4px;
  padding: 12px 24px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

/* Button Sekunder */
.btn-secondary {
  background: transparent;
  border: 1px solid #E5E5E5;
  color: #000000;
  border-radius: 4px;
}

/* Card Produk */
.card-product {
  background: #FFFFFF;
  border: 1px solid #E5E5E5;
  border-radius: 4px;
  overflow: hidden;
  transition: transform 0.2s, box-shadow 0.2s;
}
.card-product:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

/* Badge */
.badge-new    { background: #000000; color: #FFFFFF; }
.badge-sold   { background: #E53935; color: #fff; }
.badge-status { /* per status warna berbeda */ }
```

---

## 2. Struktur Halaman & Layout

### 2.1 Navbar Storefront (Sticky)

```
[LOGO ZTP]    [Katalog]  [Brand]  [Tentang]    [🔍] [🛒 2] [Avatar ▾]
```
- Posisi: sticky top, `z-50`
- Background: `rgba(255,255,255,0.95)` + backdrop-blur
- Mobile: hamburger menu → drawer kiri
- Cart icon: badge counter update via HTMX

### 2.2 Footer Storefront

```
[Logo + tagline]    [Navigasi]    [Layanan]    [Sosial Media]
                    [Copyright ZTP Sneakers 2026]
```

---

## 3. Flow Halaman — Storefront Customer

### 3.1 Landing Page

```
NAVBAR
│
├── HERO CAROUSEL (full-width)
│   ├── Foto produk/lifestyle + dark overlay
│   ├── Teks: headline besar + subtext + CTA "Lihat Koleksi"
│   └── Numbered bullets: 1 2 3 4 (auto-slide 5 detik)
│
├── TRUST BADGE STRIP
│   └── [🛡 Garansi Puas] [↩ 7 Hari Return] [🚚 Free Ongkir] [✓ 100% Authentic] [👟 Koleksi Terlengkap]
│
├── SECTION: PRODUK FEATURED (is_featured=True)
│   ├── Label: "KOLEKSI TERPILIH"
│   └── Grid 4 kolom → card produk
│
└── SECTION: PILIHAN UNTUKMU (rating tertinggi)
    ├── Label: "PILIHAN UNTUKMU"
    └── Grid 4 kolom → card produk
```

### 3.2 Halaman Katalog (`/katalog/`)

```
NAVBAR
│
├── HEADER: "SEMUA PRODUK" + jumlah produk
│
├── LAYOUT: [FILTER SIDEBAR] + [PRODUK GRID]
│
│   Filter Sidebar (desktop kiri, mobile drawer):
│   ├── Brand (checkbox list + logo)
│   ├── Ukuran (pill toggle: 38 39 40 41 42 43 44)
│   ├── Kondisi (New / Second)
│   ├── Harga (range slider: Rp0 – Rp5.000.000)
│   └── Tombol "Reset Filter"
│
│   Sort & Search:
│   ├── Search bar HTMX live (debounce 300ms)
│   └── Sort: [Terbaru ▾] [Terlaris] [Harga ↑] [Harga ↓]
│
│   Produk Grid (4 kolom desktop, 2 mobile):
│   └── Card: foto → nama → harga (+harga coret jika diskon) → badge
│
└── PAGINATION: infinite scroll via HTMX `hx-trigger="revealed"`
```

**HTMX Pattern Katalog:**
```html
<!-- Filter form -->
<form hx-get="/katalog/" hx-target="#produk-grid" hx-trigger="change">

<!-- Search bar -->
<input hx-get="/katalog/" hx-target="#produk-grid" hx-trigger="keyup changed delay:300ms">

<!-- Infinite scroll sentinel -->
<div hx-get="/katalog/?page=2" hx-trigger="revealed" hx-swap="beforeend" hx-target="#produk-grid">
```

### 3.3 Halaman Detail Produk (`/produk/[slug]/`)

```
NAVBAR
│
├── BREADCRUMB: Home > Katalog > Nike > [nama produk]
│
├── LAYOUT: [GALERI FOTO] | [INFO PRODUK]
│
│   Galeri Foto (kiri):
│   ├── Foto utama besar
│   └── Thumbnail row (klik ganti foto utama, HTMX swap)
│
│   Info Produk (kanan):
│   ├── Brand badge + nama produk (h1 bold)
│   ├── Rating: ⭐ 4.8 (23 ulasan)
│   ├── Harga: Rp850.000 (harga coret jika ada)
│   ├── Pilih Ukuran: [38] [39] [40✓] [41] [42 HABIS]
│   ├── Stok: "Tersisa 2" (jika ≤ 3)
│   ├── [+ Tambah ke Keranjang] ← HTMX, update cart badge
│   └── [♡ Simpan ke Wishlist] ← HTMX toggle
│
├── TAB: [Deskripsi] [Ulasan (23)] [Garansi & Return]
│
│   Tab Deskripsi:
│   └── Teks deskripsi produk, kondisi, detail ukuran
│
│   Tab Ulasan:
│   ├── Summary: rata-rata bintang + progress bar per bintang
│   └── List ulasan: foto customer (avatar), nama, tanggal, bintang, komentar, foto bukti
│
│   Tab Garansi & Return:
│   └── Teks kebijakan: 7 hari laporan, proses komunikasi, kontak CS
│
└── SECTION: PRODUK TERKAIT (brand sama, 4 card)
```

### 4.4 Auth Page (`/auth/`)

```
LAYOUT: Split screen
├── KIRI: foto lifestyle sneakers (dark overlay)
└── KANAN: form area (dark card)
    ├── Logo ZTP Sneakers
    ├── TAB: [Masuk] [Daftar]
    │
    │   Tab Masuk:
    │   ├── Email + Password
    │   ├── [Masuk] CTA button
    │   ├── "Lupa Password?"
    │   └── [G] Masuk dengan Google
    │
    └── Tab Daftar:
        ├── Nama Lengkap, Email, Password, Konfirmasi Password
        ├── Checkbox: Saya setuju syarat & ketentuan
        └── [Daftar] CTA button
```

### 3.5 Checkout Flow

```
PROGRESS BAR: [1 Alamat] → [2 Pengiriman] → [3 Pembayaran]

Step 1 — Alamat:
├── Nama penerima, No. telepon
├── Dropdown: Provinsi → Kota → Kecamatan (HTMX chained select)
├── Alamat detail, kode pos
└── [Lanjut ke Pengiriman →]

Step 2 — Pengiriman:
├── Loading spinner saat kalkulasi RajaOngkir
├── List opsi ekspedisi: [JNE REG — Rp18.000 — 2-3 hari]
│                        [JNE YES — Rp35.000 — 1-2 hari]
│                        [POS Reguler — Rp15.000 — 4-5 hari]
└── [← Kembali] [Lanjut ke Pembayaran →]

Step 3 — Pembayaran:
├── Ringkasan order (item, subtotal, ongkir, total)
├── [Bayar Sekarang — Rp868.000] ← trigger Midtrans Snap
└── Midtrans Snap popup muncul (modal overlay)

Post-payment:
└── Redirect ke /orders/[id]/ dengan banner sukses "Pesanan Terkonfirmasi! 🎉"
```

### 3.6 Riwayat Pesanan (`/orders/`)

```
HEADER: "Pesanan Saya"
│
├── Filter tab: [Semua] [Menunggu Bayar] [Diproses] [Dikirim] [Selesai]
│
└── List pesanan (card per order):
    ├── Nomor order + tanggal
    ├── Thumbnail foto produk (3 pertama + "+N lagi")
    ├── Total harga
    ├── Status badge berwarna
    └── [Lihat Detail] [Bayar Sekarang jika pending]
```

### 3.7 Detail Pesanan (`/orders/[id]/`)

```
HEADER: Order #ZTP-20260601-001

├── STATUS TIMELINE (horizontal):
│   paid ●──── processing ●──── shipped ●──── completed ○
│
├── INFO PENGIRIMAN:
│   ├── Nama penerima, alamat
│   └── Ekspedisi: JNE REG | No. Resi: JD0123456789 (link cek resi)
│
├── DAFTAR ITEM:
│   └── [foto] Nama Produk | Ukuran 40 | Rp850.000 × 1
│
├── RINGKASAN BIAYA:
│   Subtotal: Rp850.000
│   Ongkir (JNE REG): Rp18.000
│   Total: Rp868.000
│
├── TOMBOL AKSI (kondisional):
│   ├── [✓ Pesanan Diterima] — jika status shipped (customer konfirmasi)
│   ├── [⭐ Tulis Ulasan] — jika status completed, belum review
│   └── [⚠ Laporkan Masalah] — jika completed, dalam 7 hari, belum lapor
│
└── CHAT CRISP WIDGET (pojok kanan bawah, selalu tampil)
```

---

## 4. Flow Purna Jual (After-Sales)

### 4.1 Flow Ulasan

```
Order status: COMPLETED
        │
        ▼ (1 hari kemudian, via apscheduler)
Email: "Bagaimana pengalamanmu dengan [produk]?"
        │
        ▼ klik tombol di email ATAU dari halaman detail order
Halaman Tulis Ulasan:
├── Rating bintang (klik 1–5, interaktif)
├── Textarea komentar
├── Upload foto (drag & drop, max 3, preview thumbnail)
└── [Kirim Ulasan]
        │
        ▼
Ulasan tersimpan (is_visible=True default)
Tampil di halaman detail produk
```

### 4.2 Flow Laporan Garansi

```
Order status: COMPLETED (dalam 7 hari sejak completed)
        │
        ▼ dari detail pesanan
Form Laporan Garansi:
├── Pilih item bermasalah (dropdown dari order items)
├── Kategori: [Cacat Produk ▾] [Salah Ukuran] [Tidak Sesuai Foto] [Lainnya]
├── Deskripsi masalah (textarea min 50 karakter)
├── Upload foto bukti (max 5, wajib min 1)
└── [Kirim Laporan]
        │
        ▼
Status: DITERIMA
Email notifikasi → customer
        │
        ▼ Admin/Jasmine tinjau
Status: DITINJAU → Email ke customer
        │
        ├── [DISELESAIKAN] → Admin tulis catatan resolusi → Email ke customer
        └── [DITOLAK] → Admin tulis alasan → Email ke customer

Halaman tracking laporan (/orders/garansi/[id]/):
├── Status badge + tanggal setiap perubahan
├── Catatan resolusi dari admin (jika ada)
└── Tombol "Chat dengan CS" (buka Crisp)
```

---

## 5. Flow Admin Toko Panel

### 5.1 Layout Admin Toko

```
SIDEBAR (kiri, 240px):
├── Logo ZTP [Admin Panel]
├── Dashboard
├── Produk ▾
│   ├── Daftar Produk
│   └── Tambah Produk
├── Pesanan
├── Pelanggan
├── Ulasan
├── Laporan Garansi
└── Laporan Penjualan

TOPBAR:
[≡ Menu]  ______________________  [🔔 notifikasi] [Nama Admin ▾]

CONTENT AREA: card-based, border ringan
```

### 5.2 Dashboard Admin Toko

```
ROW KPI:
[Pesanan Hari Ini: 5]  [Stok Menipis: 3 produk]  [Garansi Baru: 1]

TABLE PESANAN TERBARU:
No | Pelanggan | Produk | Total | Status | Aksi
001 | Budi S.  | Nike Air | 850K | DIPROSES | [Proses] [Detail]
```

---

## 6. Flow Jasmine Owner Dashboard

### 6.1 Layout Jasmine

```
SIDEBAR (kiri, 260px) — Ultra dark, border emas:
├── Logo ZTP Sneakers
├── "JASMINE" label kecil emas
├── Avatar + "Selamat pagi, [nama]"
├── ─────────────────
├── Dashboard
├── Analytics
├── Produk ▾
│   ├── Semua Produk
│   ├── Kategori & Brand
│   └── Banner Homepage
├── Pesanan
├── Pelanggan
├── Laporan Garansi
├── Laporan & Export
├── Admin Toko
└── Pengaturan

TOPBAR: transparan, border bawah subtle
[≡]  ZTP Sneakers — Jasmine        [🔔] [Wahyu ▾]
```

### 6.2 Dashboard Jasmine

```
GREETING SECTION:
"Selamat pagi, Wahyu 👋" | Rabu, 1 Juni 2026

KPI CARDS ROW (4 kartu):
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│ REVENUE BULAN   │  │ TOTAL PESANAN   │  │ CUSTOMER BARU   │  │ PRODUK TERLARIS │
│ Rp 12.450.000   │  │ 47 pesanan      │  │ 12 customer     │  │ Nike Air Max    │
│ ▲ 18% vs bulan  │  │ ▲ 8% vs bulan   │  │ bulan ini       │  │ 8 terjual       │
│ [sparkline]     │  │ [sparkline]     │  │ [sparkline]     │  │ [bar mini]      │
└─────────────────┘  └─────────────────┘  └─────────────────┘  └─────────────────┘

GRAFIK PENJUALAN (full width):
Toggle: [Harian ✓] [Bulanan] [Tahunan]
Chart.js line chart — aksen emas pada line

TABEL PRODUK TERLARIS:
# | Foto | Nama | Terjual | Revenue | Stok
1 | 🖼  | Nike Air Max 90 | 8 | Rp 6.8jt | 3
```

### 6.3 Export Laporan

```
FILTER PANEL:
Bulan: [Juni ▾]  Tahun: [2026 ▾]  [Tampilkan]
        │
        ▼
TABEL LAPORAN (preview):
No | Tanggal | No. Order | Pelanggan | Produk | Ekspedisi | Total | Status

[Export ke Excel]  ← download langsung file .xlsx
```

---

## 7. Responsive Breakpoints

```
Mobile:  < 768px
  - Navbar: hamburger → drawer
  - Grid produk: 2 kolom
  - Filter: drawer bawah (bottom sheet)
  - Checkout: full-width form

Tablet:  768px – 1024px
  - Grid produk: 3 kolom
  - Filter: collapsed sidebar

Desktop: > 1024px
  - Grid produk: 4 kolom
  - Filter: sticky sidebar kiri
  - Jasmine: sidebar tetap tampil
```

---

## 8. HTMX Patterns yang Digunakan

```
Live Search:
hx-get="/katalog/search/" hx-trigger="keyup changed delay:300ms" hx-target="#produk-grid"

Add to Cart (tanpa reload):
hx-post="/cart/add/" hx-target="#cart-count" hx-swap="innerHTML"

Wishlist Toggle:
hx-post="/wishlist/toggle/[id]/" hx-swap="outerHTML"

Filter Produk:
hx-get="/katalog/" hx-trigger="change" hx-target="#produk-grid" hx-include="closest form"

Chained Select (Kota berdasarkan Provinsi):
hx-get="/api/kota/?provinsi_id=[id]" hx-target="#kota-select"

Tab Switch (Detail Produk):
hx-get="/produk/[slug]/tab/ulasan/" hx-target="#tab-content" hx-push-url="false"

Infinite Scroll:
hx-get="/katalog/?page=N" hx-trigger="revealed" hx-swap="beforeend" hx-target="#produk-grid"
```

---

## 9. Halaman Kosong & Loading States

```
Empty State:
- Keranjang kosong: ilustrasi sepatu + "Keranjang kamu kosong" + [Mulai Belanja]
- Wishlist kosong: ilustrasi hati + "Belum ada produk tersimpan"
- Hasil pencarian kosong: "Produk tidak ditemukan untuk '[query]'"
- Riwayat pesanan kosong: "Belum ada pesanan"

Loading State:
- Skeleton card produk (pulse animation Tailwind)
- Spinner untuk HTMX request
- Progress bar untuk checkout step
- Tombol disabled + "Memuat..." saat submit form
```

---

## 10. Warna Status Pesanan

```
pending:    bg-yellow-900  text-yellow-300   "Menunggu Pembayaran"
paid:       bg-blue-900    text-blue-300     "Dibayar"
processing: bg-purple-900  text-purple-300   "Sedang Diproses"
shipped:    bg-indigo-900  text-indigo-300   "Dikirim"
completed:  bg-green-900   text-green-300    "Selesai"
cancelled:  bg-red-900     text-red-300      "Dibatalkan"

Garansi:
diterima:     bg-blue-900    text-blue-300
ditinjau:     bg-yellow-900  text-yellow-300
diselesaikan: bg-green-900   text-green-300
ditolak:      bg-red-900     text-red-300
```
