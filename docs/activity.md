# Activity Diagram — ZTP Sneakers B2C Platform

> **Versi:** 1.0  
> **Tanggal:** 2026  
> **Author:** Wahyu Ahmad Cahyadi (221103805)  
> **Deskripsi:** Activity diagram untuk semua proses bisnis pada platform ZTP Sneakers B2C

---

## Daftar Proses

1. [Registrasi Akun](#1-registrasi-akun)
2. [Login Akun](#2-login-akun)
3. [Login dengan Google OAuth](#3-login-dengan-google-oauth)
4. [Lupa Password (OTP Email)](#4-lupa-password-otp-email)
5. [Melihat Katalog & Filter Produk](#5-melihat-katalog--filter-produk)
6. [Melihat Detail Produk](#6-melihat-detail-produk)
7. [Tambah ke Keranjang](#7-tambah-ke-keranjang)
8. [Kelola Wishlist](#8-kelola-wishlist)
9. [Checkout & Pembayaran (Midtrans)](#9-checkout--pembayaran-midtrans)
10. [Tracking Status Pesanan](#10-tracking-status-pesanan)
11. [Tulis Ulasan Produk](#11-tulis-ulasan-produk)
12. [Laporan Garansi / Kendala Produk](#12-laporan-garansi--kendala-produk)
13. [Admin Toko — Kelola Produk](#13-admin-toko--kelola-produk)
14. [Admin Toko — Proses Pesanan & Input Resi](#14-admin-toko--proses-pesanan--input-resi)
15. [Admin Toko — Moderasi Ulasan](#15-admin-toko--moderasi-ulasan)
16. [Admin Toko — Tinjau Laporan Garansi](#16-admin-toko--tinjau-laporan-garansi)
17. [Jasmine (Owner) — Kelola Produk Lengkap](#17-jasmine-owner--kelola-produk-lengkap)
18. [Jasmine (Owner) — Export Laporan Penjualan](#18-jasmine-owner--export-laporan-penjualan)
19. [Jasmine (Owner) — Kelola Admin Toko](#19-jasmine-owner--kelola-admin-toko)
20. [Notifikasi Email Otomatis](#20-notifikasi-email-otomatis)

---

## 1. Registrasi Akun

**Aktor:** Customer (Pengunjung)  
**Swimlane:** Pengunjung | Sistem

```mermaid
flowchart TD
    A([Mulai]) --> B[Pengunjung membuka halaman /auth/]
    B --> C[Sistem menampilkan halaman Auth dengan tab Login/Daftar]
    C --> D[Pengunjung klik tab 'Daftar']
    D --> E[Sistem menampilkan form pendaftaran via HTMX]
    E --> F[Pengunjung mengisi Nama, Email, No. HP, Password, Konfirmasi Password]
    F --> G[Pengunjung klik tombol 'Daftar']
    G --> H{Sistem memvalidasi input}
    H -- "Password tidak cocok" --> I[Sistem menampilkan error: Password tidak cocok]
    I --> F
    H -- "Email/HP kosong" --> J[Sistem menampilkan error: Email dan No. HP wajib diisi]
    J --> F
    H -- "No. HP < 10 digit" --> K[Sistem menampilkan error: No. HP minimal 10 digit]
    K --> F
    H -- "Email/HP sudah terdaftar" --> L[Sistem menampilkan error: Email/No HP sudah terdaftar]
    L --> F
    H -- "Data valid" --> M[Sistem membuat akun baru]
    M --> N[Sistem login otomatis]
    N --> O[Sistem menggabungkan guest cart dengan user cart]
    O --> P[Sistem redirect ke Halaman Utama /]
    P --> Q([Selesai])
```

---

## 2. Login Akun

**Aktor:** Customer (Member Terdaftar)  
**Swimlane:** Customer | Sistem

```mermaid
flowchart TD
    A([Mulai]) --> B[Customer membuka halaman /auth/]
    B --> C[Sistem menampilkan halaman Auth tab Login]
    C --> D[Customer memasukkan Email atau No. HP]
    D --> E[Customer klik 'Lanjut' / submit identifier]
    E --> F{Sistem mengecek identifier}
    F -- "Identifier kosong" --> G[Sistem menampilkan error validasi]
    G --> D
    F -- "User ditemukan" --> H[Sistem menampilkan form input password]
    F -- "User tidak ditemukan" --> I[Sistem menampilkan form pendaftaran]
    I --> J([Alur Registrasi])
    H --> K[Customer memasukkan Password]
    K --> L[Customer klik 'Masuk']
    L --> M{Sistem memverifikasi password}
    M -- "Password salah" --> N[Sistem menampilkan error: Password salah]
    N --> K
    M -- "Password benar" --> O[Sistem membuat sesi login]
    O --> P[Sistem menggabungkan guest cart dengan user cart]
    P --> Q[Sistem redirect ke Halaman Utama /]
    Q --> R([Selesai])
```

---

## 3. Login dengan Google OAuth

**Aktor:** Customer  
**Swimlane:** Customer | Sistem | Google

```mermaid
flowchart TD
    A([Mulai]) --> B[Customer klik tombol 'Masuk dengan Google']
    B --> C[Sistem redirect ke Google OAuth]
    C --> D[Google menampilkan halaman otorisasi]
    D --> E{Customer memberikan izin?}
    E -- "Tolak" --> F[Google redirect balik ke /auth/ dengan error]
    F --> G([Selesai - Gagal])
    E -- "Izinkan" --> H[Google mengirim token ke Sistem via django-allauth]
    H --> I{Sistem mengecek apakah email sudah terdaftar}
    I -- "Belum terdaftar" --> J[Sistem membuat akun baru otomatis]
    J --> K[Sistem login otomatis]
    I -- "Sudah terdaftar" --> K
    K --> L[Sistem redirect ke Halaman Utama /]
    L --> M([Selesai])
```

---

## 4. Lupa Password (OTP Email)

**Aktor:** Customer  
**Swimlane:** Customer | Sistem | Email

```mermaid
flowchart TD
    A([Mulai]) --> B[Customer klik 'Lupa Password?' di form login]
    B --> C[Sistem menampilkan form input email]
    C --> D[Customer memasukkan email terdaftar]
    D --> E[Customer klik 'Kirim OTP']
    E --> F{Sistem mengecek email}
    F -- "Email tidak terdaftar" --> G[Sistem menampilkan error: Email tidak ditemukan]
    G --> D
    F -- "Email valid" --> H[Sistem membuat kode OTP sementara]
    H --> I[Sistem mengirim email berisi OTP ke Customer]
    I --> J[Customer membuka email dan menyalin kode OTP]
    J --> K[Customer memasukkan kode OTP di form]
    K --> L{Sistem memverifikasi OTP}
    L -- "OTP salah / expired" --> M[Sistem menampilkan error: Kode OTP tidak valid]
    M --> K
    L -- "OTP valid" --> N[Sistem menampilkan form reset password]
    N --> O[Customer mengisi password baru dan konfirmasi]
    O --> P{Sistem memvalidasi password baru}
    P -- "Password tidak cocok" --> Q[Sistem menampilkan error]
    Q --> O
    P -- "Valid" --> R[Sistem mengupdate password]
    R --> S[Sistem redirect ke halaman Login]
    S --> T([Selesai])
```

---

## 5. Melihat Katalog & Filter Produk

**Aktor:** Pengunjung / Customer  
**Swimlane:** Pengunjung | Sistem

```mermaid
flowchart TD
    A([Mulai]) --> B[Pengunjung membuka /katalog/]
    B --> C[Sistem menampilkan semua produk aktif dalam grid 4 kolom]
    C --> D{Pengunjung melakukan aksi?}
    D -- "Ketik di search bar" --> E[HTMX kirim request ke /katalog/search/ dengan debounce 300ms]
    E --> F[Sistem memfilter produk berdasarkan query]
    F --> G[Sistem update grid produk tanpa reload]
    G --> D
    D -- "Pilih filter Brand/Ukuran/Kondisi/Harga" --> H[HTMX kirim request ke /katalog/ dengan parameter filter]
    H --> I[Sistem memfilter produk sesuai kriteria]
    I --> G
    D -- "Pilih urutan sort" --> J[HTMX kirim request dengan parameter sort]
    J --> K[Sistem mengurutkan produk]
    K --> G
    D -- "Scroll ke bawah / infinite scroll" --> L[HTMX trigger revealed - kirim request page berikutnya]
    L --> M[Sistem mengirim produk halaman berikutnya]
    M --> N[Sistem append produk baru ke grid]
    N --> D
    D -- "Klik produk" --> O[Sistem redirect ke /produk/slug/]
    O --> P([Alur Detail Produk])
    D -- "Reset Filter" --> Q[Sistem menghapus semua parameter filter]
    Q --> C
```

---

## 6. Melihat Detail Produk

**Aktor:** Pengunjung / Customer  
**Swimlane:** Pengunjung | Sistem

```mermaid
flowchart TD
    A([Mulai]) --> B[Pengunjung membuka /produk/slug/]
    B --> C[Sistem menampilkan halaman detail produk]
    C --> D[Sistem menampilkan galeri foto, info produk, pilih ukuran, stok]
    D --> E{Pengunjung melakukan aksi?}
    E -- "Klik thumbnail foto" --> F[HTMX swap foto utama dengan thumbnail dipilih]
    F --> E
    E -- "Klik ukuran" --> G[Sistem highlight ukuran dipilih dan tampilkan stok tersisa]
    G --> E
    E -- "Klik tab Ulasan" --> H[HTMX load tab ulasan dari /produk/slug/tab/ulasan/]
    H --> I[Sistem menampilkan rating summary dan daftar ulasan]
    I --> E
    E -- "Klik tab Garansi & Return" --> J[HTMX load tab kebijakan garansi]
    J --> K[Sistem menampilkan teks kebijakan garansi]
    K --> E
    E -- "Klik Tambah ke Keranjang" --> L([Alur Tambah ke Keranjang])
    E -- "Klik Simpan ke Wishlist" --> M([Alur Kelola Wishlist])
    E -- "Klik Produk Terkait" --> N[Sistem redirect ke halaman detail produk lain]
    N --> B
```

---

## 7. Tambah ke Keranjang

**Aktor:** Pengunjung / Customer  
**Swimlane:** Pengunjung | Sistem

```mermaid
flowchart TD
    A([Mulai]) --> B{Pengunjung sudah pilih ukuran?}
    B -- "Belum" --> C[Sistem menampilkan peringatan: Pilih ukuran terlebih dahulu]
    C --> B
    B -- "Sudah" --> D[Pengunjung klik tombol 'Tambah ke Keranjang']
    D --> E{Stok tersedia?}
    E -- "Tidak" --> F[Sistem menampilkan pesan: Stok habis]
    F --> G([Selesai])
    E -- "Ya" --> H{Pengunjung sudah login?}
    H -- "Belum login" --> I[Sistem simpan ke keranjang session guest]
    H -- "Sudah login" --> J[Sistem simpan ke keranjang database user]
    I --> K[HTMX update badge counter keranjang di navbar]
    J --> K
    K --> L{Item sudah ada di keranjang?}
    L -- "Sudah ada" --> M[Sistem menambah quantity item yang ada]
    M --> N[Sistem menampilkan notifikasi: Keranjang diperbarui]
    L -- "Belum ada" --> O[Sistem menambah item baru ke keranjang]
    O --> P[Sistem menampilkan notifikasi: Produk ditambahkan ke keranjang]
    N --> Q([Selesai])
    P --> Q
```

---

## 8. Kelola Wishlist

**Aktor:** Customer (harus login)  
**Swimlane:** Customer | Sistem

```mermaid
flowchart TD
    A([Mulai]) --> B[Customer klik ikon Wishlist / Simpan ke Wishlist]
    B --> C{Customer sudah login?}
    C -- "Belum" --> D[Sistem redirect ke /auth/]
    D --> E([Alur Login])
    C -- "Sudah" --> F{Produk sudah ada di wishlist?}
    F -- "Sudah ada" --> G[HTMX POST ke /wishlist/toggle/id/]
    G --> H[Sistem menghapus produk dari wishlist]
    H --> I[HTMX swap ikon jadi 'belum disimpan']
    I --> J([Selesai - Dihapus])
    F -- "Belum ada" --> K[HTMX POST ke /wishlist/toggle/id/]
    K --> L[Sistem menambahkan produk ke wishlist]
    L --> M[HTMX swap ikon jadi 'tersimpan']
    M --> N[Sistem mengecek stok produk di wishlist]
    N --> O{Stok ≤ 3?}
    O -- "Ya" --> P[Sistem kirim notifikasi: Produk hampir habis]
    O -- "Tidak" --> Q([Selesai - Ditambahkan])
    P --> Q
```

---

## 9. Checkout & Pembayaran (Midtrans)

**Aktor:** Customer  
**Swimlane:** Customer | Sistem | RajaOngkir | Midtrans

```mermaid
flowchart TD
    A([Mulai]) --> B[Customer membuka halaman keranjang /cart/]
    B --> C[Sistem menampilkan daftar item di keranjang]
    C --> D{Customer mengubah keranjang?}
    D -- "Update quantity" --> E[HTMX update qty via /cart/update/]
    E --> F[Sistem recalculate subtotal]
    F --> G[HTMX update tampilan total]
    G --> D
    D -- "Hapus item" --> H[HTMX hapus item via /cart/remove/]
    H --> I[Sistem hapus item dari keranjang]
    I --> G
    D -- "Lanjut ke Checkout" --> J{Customer sudah login?}
    J -- "Belum" --> K[Sistem redirect ke /auth/]
    K --> L([Alur Login])
    J -- "Sudah" --> M[Step 1: Sistem menampilkan form Alamat]
    M --> N[Customer mengisi nama penerima, no. HP, Provinsi, Kota, Kecamatan, alamat detail]
    N --> O[Customer klik 'Lanjut ke Pengiriman']
    O --> P[Sistem validasi form alamat]
    P --> Q[Sistem kirim request ke RajaOngkir API server-side]
    Q --> R[RajaOngkir mengembalikan daftar opsi ekspedisi dan tarif]
    R --> S[Step 2: Sistem menampilkan opsi ekspedisi JNE/POS/TIKI]
    S --> T[Customer memilih layanan ekspedisi]
    T --> U[Customer klik 'Lanjut ke Pembayaran']
    U --> V[Step 3: Sistem menampilkan ringkasan order - subtotal + ongkir + total]
    V --> W[Customer klik 'Bayar Sekarang']
    W --> X[Sistem membuat order di database dengan status pending]
    X --> Y[Sistem mengirim request ke Midtrans Snap API]
    Y --> Z[Midtrans Snap popup/modal muncul di browser Customer]
    Z --> AA{Customer menyelesaikan pembayaran?}
    AA -- "Batal / Tutup" --> AB[Sistem mempertahankan order dengan status pending]
    AB --> AC([Selesai - Belum Bayar])
    AA -- "Bayar via VA/DANA/OVO/GoPay" --> AD[Midtrans memproses transaksi]
    AD --> AE{Pembayaran berhasil?}
    AE -- "Gagal / Expired" --> AF[Midtrans menampilkan error]
    AF --> AG[Sistem update order status - cancelled jika expired]
    AG --> AH([Selesai - Gagal])
    AE -- "Berhasil" --> AI[Midtrans kirim notifikasi webhook ke Sistem]
    AI --> AJ[Sistem update order status: pending → paid]
    AJ --> AK[Sistem kosongkan keranjang Customer]
    AK --> AL[Sistem kirim email konfirmasi pesanan ke Customer]
    AL --> AM[Sistem redirect Customer ke /orders/id/ dengan banner sukses]
    AM --> AN([Selesai - Sukses])
```

---

## 10. Tracking Status Pesanan

**Aktor:** Customer  
**Swimlane:** Customer | Sistem

```mermaid
flowchart TD
    A([Mulai]) --> B[Customer membuka /orders/]
    B --> C{Customer sudah login?}
    C -- "Belum" --> D[Sistem redirect ke /auth/]
    D --> E([Alur Login])
    C -- "Sudah" --> F[Sistem menampilkan daftar semua pesanan Customer]
    F --> G{Customer memfilter pesanan?}
    G -- "Pilih tab status" --> H[Sistem menampilkan pesanan sesuai status yang dipilih]
    H --> G
    G -- "Klik 'Lihat Detail'" --> I[Sistem menampilkan /orders/id/]
    I --> J[Sistem menampilkan timeline status pesanan]
    J --> K[Sistem menampilkan info pengiriman, resi, ekspedisi]
    K --> L{Status pesanan saat ini?}
    L -- "Menunggu Pembayaran" --> M[Sistem tampilkan tombol 'Bayar Sekarang']
    M --> N[Customer klik 'Bayar Sekarang']
    N --> O([Alur Pembayaran Midtrans])
    L -- "Dikirim" --> P[Sistem tampilkan tombol 'Pesanan Diterima']
    P --> Q{Customer mengkonfirmasi penerimaan?}
    Q -- "Ya, klik Pesanan Diterima" --> R[Sistem update status: shipped → completed]
    R --> S[Sistem kirim email konfirmasi penyelesaian]
    S --> T[Sistem kirim email undangan ulasan 1 hari kemudian]
    T --> U([Selesai - Completed])
    L -- "Selesai" --> V[Sistem tampilkan tombol 'Tulis Ulasan' dan 'Laporkan Masalah']
    V --> W{Customer pilih aksi?}
    W -- "Tulis Ulasan" --> X([Alur Tulis Ulasan])
    W -- "Laporkan Masalah" --> Y([Alur Laporan Garansi])
    W -- "Tidak ada" --> Z([Selesai])
```

---

## 11. Tulis Ulasan Produk

**Aktor:** Customer  
**Swimlane:** Customer | Sistem

```mermaid
flowchart TD
    A([Mulai]) --> B{Trigger ulasan}
    B -- "Klik link di email undangan ulasan" --> C[Sistem membuka halaman form ulasan]
    B -- "Klik 'Tulis Ulasan' di detail pesanan" --> C
    C --> D{Validasi akses ulasan}
    D -- "Order belum Selesai" --> E[Sistem menampilkan error: Ulasan hanya untuk pesanan selesai]
    E --> F([Selesai - Ditolak])
    D -- "Sudah pernah review item ini" --> G[Sistem menampilkan error: Kamu sudah memberikan ulasan]
    G --> F
    D -- "Akses valid" --> H[Sistem menampilkan form ulasan]
    H --> I[Customer memilih rating bintang 1–5]
    I --> J[Customer menulis komentar]
    J --> K{Customer ingin upload foto?}
    K -- "Ya" --> L[Customer memilih foto maks 3 foto]
    L --> M[Sistem menampilkan preview thumbnail foto]
    M --> N[Customer klik 'Kirim Ulasan']
    K -- "Tidak" --> N
    N --> O{Sistem validasi form}
    O -- "Rating belum dipilih" --> P[Sistem menampilkan error: Pilih rating terlebih dahulu]
    P --> I
    O -- "Komentar terlalu pendek" --> Q[Sistem menampilkan error: Komentar terlalu singkat]
    Q --> J
    O -- "Valid" --> R[Sistem menyimpan ulasan dengan is_visible=True]
    R --> S[Sistem menampilkan konfirmasi: Ulasan berhasil dikirim]
    S --> T[Ulasan tampil di halaman detail produk]
    T --> U[Sistem mengupdate rata-rata rating produk]
    U --> V([Selesai])
```

---

## 12. Laporan Garansi / Kendala Produk

**Aktor:** Customer  
**Swimlane:** Customer | Sistem | Admin/Jasmine

```mermaid
flowchart TD
    A([Mulai]) --> B[Customer klik 'Laporkan Masalah' di detail pesanan]
    B --> C{Validasi akses laporan}
    C -- "Order belum Selesai" --> D[Sistem menampilkan error: Laporan hanya untuk pesanan selesai]
    D --> E([Selesai - Ditolak])
    C -- "Sudah lebih 7 hari sejak Selesai" --> F[Sistem menampilkan error: Batas waktu laporan telah habis]
    F --> E
    C -- "Sudah ada laporan aktif" --> G[Sistem menampilkan error: Laporan sedang diproses]
    G --> E
    C -- "Akses valid" --> H[Sistem menampilkan form laporan garansi]
    H --> I[Customer memilih item bermasalah dari dropdown]
    I --> J[Customer memilih kategori masalah: Cacat Produk / Salah Ukuran / Tidak Sesuai Foto / Lainnya]
    J --> K[Customer mengisi deskripsi masalah min 50 karakter]
    K --> L[Customer mengupload foto bukti min 1, maks 5]
    L --> M[Customer klik 'Kirim Laporan']
    M --> N{Sistem memvalidasi form}
    N -- "Deskripsi terlalu pendek" --> O[Sistem menampilkan error validasi]
    O --> K
    N -- "Tidak ada foto bukti" --> P[Sistem menampilkan error: Upload minimal 1 foto bukti]
    P --> L
    N -- "Valid" --> Q[Sistem menyimpan laporan dengan status: Diterima]
    Q --> R[Sistem mengirim email notifikasi ke Customer: Laporan diterima]
    R --> S[Admin/Jasmine menerima notifikasi laporan baru]
    S --> T[Admin/Jasmine membuka laporan di panel admin]
    T --> U[Admin/Jasmine mengubah status: Diterima → Ditinjau]
    U --> V[Sistem mengirim email ke Customer: Laporan sedang ditinjau]
    V --> W{Admin/Jasmine membuat keputusan}
    W -- "Diselesaikan" --> X[Admin/Jasmine menulis catatan resolusi]
    X --> Y[Sistem update status: Diselesaikan]
    Y --> Z[Sistem mengirim email ke Customer: Laporan diselesaikan + catatan resolusi]
    Z --> AA([Selesai - Diselesaikan])
    W -- "Ditolak" --> AB[Admin/Jasmine menulis alasan penolakan]
    AB --> AC[Sistem update status: Ditolak]
    AC --> AD[Sistem mengirim email ke Customer: Laporan ditolak + alasan]
    AD --> AE([Selesai - Ditolak])
```

---

## 13. Admin Toko — Kelola Produk

**Aktor:** Admin Toko  
**Swimlane:** Admin Toko | Sistem

```mermaid
flowchart TD
    A([Mulai]) --> B[Admin Toko login ke /admin-toko/]
    B --> C{Login berhasil dan memiliki permission AdminToko?}
    C -- "Tidak" --> D[Sistem menampilkan error: Akses ditolak]
    D --> E([Selesai - Ditolak])
    C -- "Ya" --> F[Sistem menampilkan dashboard Admin Toko]
    F --> G[Admin Toko klik menu 'Produk']
    G --> H[Sistem menampilkan daftar semua produk]
    H --> I{Admin Toko memilih aksi?}
    I -- "Tambah Produk" --> J[Sistem menampilkan form tambah produk]
    J --> K[Admin Toko mengisi: nama, brand, kategori, harga, kondisi, deskripsi, foto]
    K --> L[Admin Toko mengatur stok per ukuran]
    L --> M[Admin Toko klik 'Simpan']
    M --> N{Sistem memvalidasi data produk}
    N -- "Ada field wajib kosong" --> O[Sistem menampilkan error validasi]
    O --> K
    N -- "Valid" --> P[Sistem menyimpan produk baru]
    P --> Q[Produk tampil di katalog storefront]
    Q --> R([Selesai - Produk Ditambahkan])
    I -- "Edit Produk" --> S[Sistem menampilkan form edit produk yang dipilih]
    S --> T[Admin Toko mengubah data produk]
    T --> U[Admin Toko klik 'Simpan Perubahan']
    U --> V[Sistem menyimpan perubahan]
    V --> W([Selesai - Produk Diupdate])
    I -- "Nonaktifkan Produk" --> X[Sistem menampilkan konfirmasi nonaktifkan]
    X --> Y[Admin Toko konfirmasi]
    Y --> Z[Sistem set is_active=False]
    Z --> AA[Produk tidak tampil di katalog]
    AA --> AB([Selesai - Produk Dinonaktifkan])
    I -- "Update Stok" --> AC[Sistem menampilkan form update stok per ukuran]
    AC --> AD[Admin Toko mengubah jumlah stok]
    AD --> AE[Sistem menyimpan perubahan stok]
    AE --> AF([Selesai - Stok Diupdate])
```

---

## 14. Admin Toko — Proses Pesanan & Input Resi

**Aktor:** Admin Toko  
**Swimlane:** Admin Toko | Sistem | Customer

```mermaid
flowchart TD
    A([Mulai]) --> B[Admin Toko membuka menu 'Pesanan' di panel admin]
    B --> C[Sistem menampilkan daftar semua pesanan]
    C --> D[Admin Toko memilih pesanan dengan status 'Dibayar']
    D --> E[Sistem menampilkan detail pesanan]
    E --> F[Admin Toko klik 'Proses Pesanan']
    F --> G[Sistem update status: paid → processing]
    G --> H[Sistem kirim email notifikasi ke Customer: Pesanan sedang diproses]
    H --> I[Admin Toko mempersiapkan barang]
    I --> J[Admin Toko mengemas dan menyerahkan ke ekspedisi]
    J --> K[Admin Toko mendapatkan nomor resi dari ekspedisi]
    K --> L[Admin Toko klik 'Input Nomor Resi']
    L --> M[Sistem menampilkan form input resi]
    M --> N[Admin Toko memasukkan nomor resi dan ekspedisi]
    N --> O[Admin Toko klik 'Simpan Resi & Tandai Dikirim']
    O --> P{Sistem validasi resi}
    P -- "Resi kosong" --> Q[Sistem menampilkan error: Nomor resi wajib diisi]
    Q --> N
    P -- "Valid" --> R[Sistem menyimpan resi di database]
    R --> S[Sistem update status: processing → shipped]
    S --> T[Sistem kirim email ke Customer: Pesanan sudah dikirim + no. resi]
    T --> U[Admin Toko dapat memantau konfirmasi penerimaan dari Customer]
    U --> V([Selesai])
```

---

## 15. Admin Toko — Moderasi Ulasan

**Aktor:** Admin Toko  
**Swimlane:** Admin Toko | Sistem

```mermaid
flowchart TD
    A([Mulai]) --> B[Admin Toko membuka menu 'Ulasan' di panel admin]
    B --> C[Sistem menampilkan daftar semua ulasan produk]
    C --> D[Admin Toko meninjau ulasan satu per satu]
    D --> E{Admin Toko menilai ulasan?}
    E -- "Ulasan pantas ditampilkan" --> F[Admin Toko membiarkan is_visible=True]
    F --> G[Ulasan tetap tampil di halaman produk]
    G --> D
    E -- "Ulasan tidak pantas / spam" --> H[Admin Toko klik 'Sembunyikan Ulasan']
    H --> I[Sistem menampilkan konfirmasi]
    I --> J[Admin Toko konfirmasi]
    J --> K[Sistem update is_visible=False]
    K --> L[Ulasan tidak lagi tampil di halaman produk]
    L --> M[Sistem mencatat log moderasi]
    M --> D
    E -- "Selesai moderasi" --> N([Selesai])
```

---

## 16. Admin Toko — Tinjau Laporan Garansi

**Aktor:** Admin Toko  
**Swimlane:** Admin Toko | Sistem | Customer

```mermaid
flowchart TD
    A([Mulai]) --> B[Admin Toko membuka menu 'Laporan Garansi' di panel admin]
    B --> C[Sistem menampilkan daftar laporan garansi]
    C --> D[Admin Toko memilih laporan dengan status 'Diterima']
    D --> E[Sistem menampilkan detail laporan: item, kategori, deskripsi, foto bukti]
    E --> F[Admin Toko mengubah status ke 'Ditinjau']
    F --> G[Sistem kirim email ke Customer: Laporan sedang ditinjau]
    G --> H[Admin Toko menganalisa laporan dan foto bukti]
    H --> I{Admin Toko mengambil keputusan}
    I -- "Klaim valid - Diselesaikan" --> J[Admin Toko menulis catatan resolusi untuk Customer]
    J --> K[Admin Toko klik 'Tandai Diselesaikan']
    K --> L[Sistem update status laporan: Diselesaikan]
    L --> M[Sistem kirim email ke Customer: Resolusi + catatan admin]
    M --> N([Selesai - Diselesaikan])
    I -- "Klaim tidak valid - Ditolak" --> O[Admin Toko menulis alasan penolakan]
    O --> P[Admin Toko klik 'Tolak Laporan']
    P --> Q[Sistem update status laporan: Ditolak]
    Q --> R[Sistem kirim email ke Customer: Laporan ditolak + alasan]
    R --> S([Selesai - Ditolak])
    I -- "Perlu info lebih" --> T[Admin Toko menggunakan Crisp Chat untuk menghubungi Customer]
    T --> U[Diskusi berlanjut via Live Chat]
    U --> H
```

---

## 17. Jasmine (Owner) — Kelola Produk Lengkap

**Aktor:** Jasmine (Owner)  
**Swimlane:** Jasmine | Sistem

```mermaid
flowchart TD
    A([Mulai]) --> B[Jasmine login ke /jasmine/]
    B --> C{Login berhasil dan is_staff=True + group Owner?}
    C -- "Tidak" --> D[Sistem menampilkan error: Akses ditolak]
    D --> E([Selesai - Ditolak])
    C -- "Ya" --> F[Sistem menampilkan dashboard Jasmine dengan KPI cards]
    F --> G[Jasmine klik menu 'Produk']
    G --> H{Jasmine memilih sub-menu}
    H -- "Semua Produk" --> I[Sistem menampilkan daftar semua produk]
    I --> J{Jasmine memilih aksi}
    J -- "Tambah Produk" --> K[Sistem menampilkan form tambah produk lengkap]
    K --> L[Jasmine mengisi semua detail produk termasuk is_featured toggle]
    L --> M[Jasmine klik 'Simpan Produk']
    M --> N[Sistem menyimpan produk]
    N --> O([Selesai - Produk Ditambahkan])
    J -- "Edit Produk" --> P[Sistem menampilkan form edit]
    P --> Q[Jasmine edit data produk]
    Q --> R[Jasmine klik 'Simpan']
    R --> S[Sistem menyimpan perubahan]
    S --> T([Selesai - Diupdate])
    J -- "Hapus Produk Permanen" --> U[Sistem menampilkan konfirmasi hapus permanen]
    U --> V[Jasmine konfirmasi]
    V --> W[Sistem hapus produk dari database]
    W --> X([Selesai - Dihapus])
    H -- "Kategori & Brand" --> Y[Sistem menampilkan daftar kategori dan brand]
    Y --> Z[Jasmine tambah/edit/hapus kategori atau brand]
    Z --> AA[Sistem menyimpan perubahan]
    AA --> AB([Selesai - Kategori/Brand Diupdate])
    H -- "Banner Homepage" --> AC[Sistem menampilkan daftar banner hero carousel]
    AC --> AD[Jasmine tambah/edit/hapus banner dan urutan slide]
    AD --> AE[Sistem menyimpan perubahan banner]
    AE --> AF([Selesai - Banner Diupdate])
```

---

## 18. Jasmine (Owner) — Export Laporan Penjualan

**Aktor:** Jasmine (Owner)  
**Swimlane:** Jasmine | Sistem

```mermaid
flowchart TD
    A([Mulai]) --> B[Jasmine membuka menu 'Laporan & Export' di dashboard Jasmine]
    B --> C[Sistem menampilkan halaman laporan dengan filter]
    C --> D[Jasmine memilih Bulan dan Tahun laporan]
    D --> E[Jasmine klik 'Tampilkan']
    E --> F[Sistem mengambil data pesanan sesuai periode yang dipilih]
    F --> G[Sistem menampilkan preview tabel laporan: No Order, Tanggal, Pelanggan, Produk, Ekspedisi, Total, Status]
    G --> H{Laporan yang ditampilkan sudah sesuai?}
    H -- "Tidak, ubah filter" --> D
    H -- "Ya" --> I[Jasmine klik 'Export ke Excel']
    I --> J[Sistem memproses data dengan openpyxl]
    J --> K[Sistem membuat file .xlsx dengan format terstruktur]
    K --> L[Sistem mengirim file ke browser untuk didownload]
    L --> M[Browser mendownload file laporan .xlsx]
    M --> N([Selesai])
```

---

## 19. Jasmine (Owner) — Kelola Admin Toko

**Aktor:** Jasmine (Owner)  
**Swimlane:** Jasmine | Sistem

```mermaid
flowchart TD
    A([Mulai]) --> B[Jasmine membuka menu 'Admin Toko' di dashboard Jasmine]
    B --> C[Sistem menampilkan daftar akun Admin Toko]
    C --> D{Jasmine memilih aksi?}
    D -- "Buat Admin Baru" --> E[Sistem menampilkan form buat akun Admin Toko]
    E --> F[Jasmine mengisi nama, email, password untuk Admin baru]
    F --> G[Jasmine mengatur permission yang diizinkan]
    G --> H[Jasmine klik 'Buat Akun']
    H --> I{Sistem memvalidasi data}
    I -- "Email sudah ada" --> J[Sistem menampilkan error]
    J --> F
    I -- "Valid" --> K[Sistem membuat akun Admin Toko baru]
    K --> L[Sistem menambahkan user ke group AdminToko]
    L --> M[Sistem kirim email kredensial ke Admin baru]
    M --> N([Selesai - Admin Dibuat])
    D -- "Suspend / Nonaktifkan Admin" --> O[Jasmine memilih akun Admin yang akan disuspend]
    O --> P[Jasmine klik 'Suspend Akun']
    P --> Q[Sistem menampilkan konfirmasi]
    Q --> R[Jasmine konfirmasi]
    R --> S[Sistem set is_active=False pada akun Admin]
    S --> T[Admin tidak dapat login lagi]
    T --> U([Selesai - Admin Disuspend])
    D -- "Atur Permission" --> V[Jasmine memilih akun Admin]
    V --> W[Sistem menampilkan daftar permission yang bisa diatur]
    W --> X[Jasmine centang/uncentang permission]
    X --> Y[Jasmine klik 'Simpan Permission']
    Y --> Z[Sistem mengupdate permission Admin]
    Z --> AA([Selesai - Permission Diupdate])
```

---

## 20. Notifikasi Email Otomatis

**Aktor:** Sistem (Background Job via django-apscheduler)  
**Swimlane:** Sistem | Email Server | Customer

```mermaid
flowchart TD
    A([Trigger: Perubahan Status]) --> B{Jenis event?}
    
    B -- "Pembayaran berhasil - paid" --> C[Sistem kirim email: Konfirmasi Pesanan + detail item + total]
    C --> D[Email terkirim ke Customer]
    
    B -- "Status → processing" --> E[Sistem kirim email: Pesanan sedang diproses]
    E --> D
    
    B -- "Status → shipped" --> F[Sistem kirim email: Pesanan dikirim + nomor resi + ekspedisi]
    F --> D
    
    B -- "Status → completed" --> G[Sistem kirim email: Pesanan selesai + tombol konfirmasi]
    G --> D
    G --> H[Sistem jadwalkan job: kirim undangan ulasan 1 hari kemudian]
    H --> I{1 hari kemudian, via apscheduler}
    I --> J[Sistem kirim email undangan ulasan: Bagaimana pengalamanmu?]
    J --> D
    
    B -- "Status → cancelled" --> K[Sistem kirim email: Pesanan dibatalkan]
    K --> D
    
    B -- "Laporan garansi status berubah" --> L{Status laporan baru?}
    L -- "Diterima" --> M[Sistem kirim email: Laporan garansi diterima]
    M --> D
    L -- "Ditinjau" --> N[Sistem kirim email: Laporan sedang ditinjau]
    N --> D
    L -- "Diselesaikan" --> O[Sistem kirim email: Laporan diselesaikan + catatan resolusi]
    O --> D
    L -- "Ditolak" --> P[Sistem kirim email: Laporan ditolak + alasan]
    P --> D
    
    D --> Q[Customer membaca email]
    Q --> R{Customer melakukan aksi lanjutan?}
    R -- "Klik link ulasan" --> S([Alur Tulis Ulasan])
    R -- "Klik cek status pesanan" --> T([Alur Tracking Pesanan])
    R -- "Tidak ada aksi" --> U([Selesai])
```

---

## Ringkasan Aktor & Proses

| No | Proses | Aktor Utama | Modul |
|---|---|---|---|
| 1 | Registrasi Akun | Pengunjung | userauths |
| 2 | Login Akun | Customer | userauths |
| 3 | Login Google OAuth | Customer | userauths / allauth |
| 4 | Lupa Password | Customer | userauths |
| 5 | Katalog & Filter Produk | Pengunjung / Customer | storefront / products |
| 6 | Detail Produk | Pengunjung / Customer | storefront / products |
| 7 | Tambah ke Keranjang | Pengunjung / Customer | orders (cart) |
| 8 | Kelola Wishlist | Customer | storefront |
| 9 | Checkout & Pembayaran | Customer | orders / Midtrans |
| 10 | Tracking Status Pesanan | Customer | orders |
| 11 | Tulis Ulasan Produk | Customer | aftersales |
| 12 | Laporan Garansi | Customer | aftersales |
| 13 | Kelola Produk | Admin Toko | admintoko / products |
| 14 | Proses Pesanan & Resi | Admin Toko | admintoko / orders |
| 15 | Moderasi Ulasan | Admin Toko | admintoko / aftersales |
| 16 | Tinjau Laporan Garansi | Admin Toko | admintoko / aftersales |
| 17 | Kelola Produk Lengkap | Jasmine (Owner) | jasmine / products |
| 18 | Export Laporan Penjualan | Jasmine (Owner) | jasmine / reports |
| 19 | Kelola Admin Toko | Jasmine (Owner) | jasmine / userauths |
| 20 | Notifikasi Email Otomatis | Sistem | core / signals |
