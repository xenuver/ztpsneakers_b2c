# AGENT.md — ZTP Sneakers Development Agent

> **File ini adalah instruksi wajib untuk setiap agent/AI yang mengerjakan project ZTP Sneakers.**  
> Baca dan pahami seluruh isi file ini beserta dokumen yang direferensikan sebelum mengeksekusi task apapun.

---
## The 3-Tier Workflow

Sebagai AI agent untuk proyek ZTP Sneakers (Wahyu), kamu beroperasi dalam 3 lapisan:

**Tier 1: The Blueprint (Directives)**
- `PRD.md`, `UIUX_FLOW.md`, dan file ini (`AGENT.md`) adalah blueprint utama — arsitektur, flow UI/UX, aturan coding, dan batasan skripsi.
- `docs/TASK.md` berisi roadmap dan urutan pengerjaan per sprint.
- Treat these as clear, natural-language instructions from a human manager.

**Tier 2: The Brain (Orchestration)**
- Peranmu: baca blueprint, delegate ke tool yang tepat, manage error, minta input jika stuck.
- Jangan langsung eksekusi task kompleks — parse dulu `PRD.md` dan `UIUX_FLOW.md`, rencanakan struktur model/view/template, baru eksekusi.
- Jika ada instruksi yang bertentangan dengan batasan sistem (shared hosting, MySQL, HTMX), ikuti aturan di `AGENT.md`.

**Tier 3: The Muscle (Execution)**
- Django Views di `views.py` / `htmx_views.py` → logika bisnis dan interaksi HTMX.
- Django ORM di `models.py` → definisi schema dan interaksi database.
- Tailwind CSS & HTMX di `templates/` → presentasi UI.
- Selalu cek apakah fungsi/model sudah ada di `apps/` sebelum membuat yang baru.

*Filosofi: AI untuk "thinking", kode deterministik untuk "doing". 90% accuracy × 5 langkah = 59% success. Minimalkan langkah AI dengan pola Django/HTMX yang handal.*

---

## Core Rules of Engagement

**1. Search Before You Build**
- Cek `apps/` untuk model atau view yang sudah ada sebelum membuat aplikasi baru.
- Cek `templates/` dan `UIUX_FLOW.md` untuk desain komponen sebelum membuat styling Tailwind baru.
- Cek `models.py` di aplikasi terkait untuk tabel yang sudah ada sebelum menambahkan schema baru.

**2. The Auto-Correction Protocol**
- Jika ada error (Django traceback/HTMX error), analisa stack trace dan response network langsung.
- Perbaiki dan test ulang (selalu pastikan Django server berjalan normal).
- Jika ada constraint (misal terkait environment shared hosting), adaptasi dan dokumentasikan solusinya.

**3. Evolve the Blueprints**
- Blueprint adalah living documents. Update `PRD.md` atau `UIUX_FLOW.md` jika ada keputusan teknis/arsitektur baru setelah diskusi dengan user.
- Jangan hapus atau overwrite section yang sudah ada tanpa izin eksplisit.
- Tambahkan keputusan baru di bagian yang relevan.

**4. Update docs/TASK.md Setiap Selesai Perubahan** ⚠️
- Setiap kali selesai mengimplementasikan sebuah fitur atau memperbaiki bug, **WAJIB** update `docs/TASK.md`
- Tandai task yang selesai: `- [ ]` → `- [x]`
- Tandai task yang sedang dikerjakan: `- [ ]` → `- [/]`
- Jika membuat fitur/file baru yang belum ada di TASK.md, tambahkan sebagai task baru lalu langsung tandai `- [x]`
- Jika menemukan bug yang diperbaiki, tambahkan ke section "Bug yang Sudah Diperbaiki" (jika ada) atau jadikan task baru.
- **Jangan anggap task selesai sebelum TASK.md diperbarui**

---


## IDENTITAS PROJECT

- **Nama:** ZTP Sneakers B2C Platform  
- **Jenis:** E-commerce B2C — penjual sepatu second UMKM Pontianak  
- **Stack:** Django 5.x · HTMX 2.x · Tailwind CSS 3.x · MySQL · Shared Hosting  
- **Visual Referensi:** 807garage.com — dark, premium, street culture  
- **Tiga Area Utama:** Storefront (customer) · Admin Toko (staf) · Jasmine (owner)

---

## LANGKAH WAJIB SEBELUM EKSEKUSI TASK

> ⚠️ JANGAN SKIP LANGKAH INI. Agent yang langsung mengerjakan task tanpa membaca dokumen akan menghasilkan output yang tidak konsisten dengan desain sistem.

### Langkah 1 — Baca PRD.md
```
Baca file: PRD.md
Pahami:
- Tujuan platform dan konteks UMKM ZTP Sneakers
- Seluruh modul dan fitur (Storefront, Admin Toko, Jasmine)
- Layanan Purna Jual (Seksi 5) — ulasan, garansi, live chat
- Catatan hosting shared hosting (MySQL, Passenger WSGI, no Celery)
- Design system (warna, tipografi, komponen)
- Batasan sistem sesuai skripsi
```

### Langkah 2 — Baca TASK.md
```
Baca file: TASK.md
Pahami:
- Struktur sprint dan urutan pengerjaan
- Breakdown task per sprint (Sprint 0–8)
- Task mana yang sedang dikerjakan sekarang
- Dependencies antar task
- Prioritas fitur (🔴 Wajib / 🟠 Penting / 🟡 Penting / 🟢 Bonus)
```

### Langkah 3 — Baca UIUX_FLOW.md
```
Baca file: UIUX_FLOW.md
Pahami:
- Design system lengkap (palet warna, tipografi, komponen CSS)
- Layout dan struktur setiap halaman
- Flow lengkap setiap modul (customer, admin, jasmine)
- HTMX patterns yang digunakan
- Responsive breakpoints
- Empty state dan loading state
- Warna badge status pesanan dan garansi
```

### Langkah 4 — Load Skill uiuxpromax
```
Gunakan skill: uiuxpromax
Skill ini memberikan panduan untuk:
- Membuat tampilan berkualitas production-grade
- Menghindari tampilan generic/AI-default
- Dark theme yang konsisten dengan 807garage.com
- Komponen Tailwind yang tepat untuk setiap elemen
```

### Langkah 5 — Konfirmasi task yang akan dikerjakan
Sebelum mulai, nyatakan:
1. Task apa yang sedang dikerjakan (nomor sprint + nama task)
2. File apa yang akan dibuat/dimodifikasi
3. Komponen apa yang dibutuhkan dari UIUX_FLOW.md
4. Apakah ada dependency yang belum selesai

---

## ATURAN PENGERJAAN

### Aturan Umum
- Selalu gunakan **MySQL** (bukan PostgreSQL) — project di shared hosting
- Selalu gunakan **HTMX** untuk interaksi dinamis (bukan JavaScript vanilla atau fetch API)
- Selalu gunakan **Tailwind CSS** — tidak boleh menulis CSS custom kecuali yang ada di UIUX_FLOW.md Design System
- Semua template Django harus extend dari `base.html` atau `base_admin.html` atau `base_jasmine.html`
- Gunakan **django-apscheduler** untuk scheduled task (bukan Celery)
- RajaOngkir API harus dipanggil dari **backend** (bukan frontend), API key di `.env`

### Aturan Tampilan
- Background utama: `#0D0D0D` (storefront), `#0A0A0A` (Jasmine)
- Accent color: `#E8FF00` (kuning neon) untuk CTA utama
- Semua teks pada background gelap: `#F5F5F5` (primer) atau `#A0A0A0` (sekunder)
- Produk card: hover `scale(1.02)` + border aksen kuning
- Tombol CTA: background `#E8FF00`, teks hitam bold, uppercase
- Loading state: Tailwind `animate-pulse` untuk skeleton, spinner untuk HTMX

### Aturan Fitur Purna Jual
- Tombol "Tulis Ulasan" hanya muncul jika `order.status == 'completed'` AND belum ada ulasan untuk item tersebut
- Tombol "Laporkan Masalah" hanya muncul dalam **7 hari** setelah `completed_at`
- Form laporan garansi: foto bukti wajib minimum 1
- Email after-sales dikirim **1 hari** setelah status `completed` via apscheduler

### Aturan Permission
```python
# Admin Toko — cek di setiap view admin_toko
class AdminTokoRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='AdminToko').exists():
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

# Jasmine Owner — cek di setiap view jasmine
class OwnerRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Owner').exists():
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
```

### Aturan HTMX
- Selalu tambahkan `hx-indicator` untuk loading state
- Response partial view harus mengembalikan hanya fragment HTML, bukan full page
- Gunakan `HX-Redirect` header untuk redirect setelah POST
- CSRF token wajib di semua form: `hx-headers='{"X-CSRFToken": "{{ csrf_token }}"}'`

---

## STRUKTUR PROJECT

```
ztpsneakers/
├── config/
│   ├── settings/
│   │   ├── base.py
│   │   ├── development.py
│   │   └── production.py        # Shared hosting settings
│   ├── urls.py
│   └── passenger_wsgi.py        # Deploy shared hosting
│
├── apps/
│   ├── accounts/                # Custom User, Auth, Profile
│   ├── products/                # Product, Category, Brand, Banner, Stock
│   ├── orders/                  # Cart, Order, Checkout, Shipping
│   ├── aftersales/              # Review, GaransiLaporan, Notifikasi
│   ├── storefront/              # Views untuk customer-facing
│   ├── admin_toko/              # Views untuk staf
│   └── jasmine/                 # Views untuk owner
│
├── templates/
│   ├── base.html                # Base storefront (dark theme)
│   ├── base_admin.html          # Base admin toko
│   ├── base_jasmine.html        # Base jasmine (ultra-dark + gold)
│   ├── storefront/
│   ├── admin_toko/
│   ├── jasmine/
│   └── emails/                  # HTML email templates
│
├── static/
│   ├── css/
│   ├── js/
│   └── img/
│
├── media/                       # Upload files (produk, ulasan, garansi)
├── requirements.txt
├── .env.example
├── manage.py
└── README.md
```

---

## CONTOH WORKFLOW AGENT

### Contoh: Agent diminta membuat halaman detail produk

```
1. Baca PRD.md → Seksi 4.1 Detail Produk
   - Cek fitur: galeri, pilih ukuran, stok, add to cart, wishlist, tab ulasan/garansi

2. Baca TASK.md → Sprint 2: "Detail produk: galeri, pilih ukuran, stok real-time"
   - Cek apakah models Product, ProductImage, ProductSize sudah dibuat

3. Baca UIUX_FLOW.md → Seksi 3.3 Halaman Detail Produk
   - Ambil struktur layout: [GALERI FOTO] | [INFO PRODUK]
   - Ambil HTMX pattern: tab switch, add to cart, wishlist toggle
   - Ambil warna dan komponen dari Design System (Seksi 1)

4. Load skill uiuxpromax
   - Terapkan prinsip premium dark UI
   - Pastikan tidak ada tampilan generic

5. Buat file:
   - templates/storefront/produk_detail.html (extend base.html)
   - apps/storefront/views.py → ProductDetailView
   - apps/storefront/urls.py → path('produk/<slug:slug>/', ...)
   - apps/storefront/htmx_views.py → add_to_cart, toggle_wishlist, tab_content

6. Verifikasi:
   - Apakah dark theme konsisten?
   - Apakah HTMX berjalan tanpa reload?
   - Apakah tab Ulasan menampilkan data dari model Review?
   - Apakah Tab Garansi ada teks kebijakan?
```

---

## CHECKLIST SETIAP OUTPUT

Sebelum menyelesaikan task, pastikan:

- [ ] Template extend base yang benar (base.html / base_admin.html / base_jasmine.html)
- [ ] Warna background dan teks sesuai Design System di UIUX_FLOW.md
- [ ] Tidak ada hardcoded warna di luar yang ada di UIUX_FLOW.md
- [ ] Semua form punya CSRF token
- [ ] Semua HTMX request punya indicator loading
- [ ] Permission mixin digunakan di view admin/jasmine
- [ ] MySQL-compatible (tidak ada PostgreSQL-specific syntax)
- [ ] Responsive: cek mobile dan desktop breakpoint
- [ ] Empty state dan error state tersedia
- [ ] Sesuai dengan batasan sistem di PRD.md (tidak implementasi fitur di luar scope)

---

## KONTAK & REFERENSI

- **Skripsi:** Perancangan B2C pada UMKM ZTP Sneakers — Wahyu Ahmad Cahyadi (221103805)
- **Institusi:** STMIK Pontianak, Program Studi Sistem Informasi, Peminatan E-Business Technology
- **Visual Referensi:** https://807garage.com
- **Dokumen PRD:** `PRD.md`
- **Dokumen Task:** `TASK.md`
- **Dokumen UI/UX:** `UIUX_FLOW.md`
- **Skill UI:** `uiuxpromax`
