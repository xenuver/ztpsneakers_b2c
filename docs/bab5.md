# BAB 5
# HASIL PENELITIAN

## 5.1 Perancangan dan Pengembangan

Perancangan dan pengembangan platform ZTP Sneakers B2C dilaksanakan menggunakan metodologi Rapid Application Development (RAD). Metodologi ini dipilih karena mampu mengakomodasi proses pengembangan yang bersifat iteratif dan berorientasi pada keterlibatan pengguna secara langsung, sehingga sesuai dengan kebutuhan UMKM yang memerlukan sistem fungsional dalam waktu yang relatif singkat. Proses pengembangan dibagi ke dalam empat fase utama, yaitu Requirements Planning, User Design, Rapid Construction, dan Cutover. Bab ini memaparkan hasil dari seluruh fase tersebut secara sistematis berdasarkan implementasi yang telah dilaksanakan.

---

## 5.1.1 Fase Requirements Planning

Fase Requirements Planning merupakan tahapan awal dalam metodologi RAD yang bertujuan untuk mengidentifikasi serta memprioritaskan kebutuhan fungsional dan non-fungsional sistem. Tahapan ini dilaksanakan melalui observasi langsung terhadap proses operasional UMKM ZTP Sneakers yang sebelumnya mengandalkan media sosial Instagram dan transaksi tatap muka sebagai saluran penjualan utama. Dari hasil observasi tersebut, ditemukan sejumlah hambatan operasional yang signifikan, di antaranya ketidakmampuan sistem lama dalam menampilkan ketersediaan stok secara real-time, tidak adanya mekanisme pelacakan pesanan bagi pelanggan, serta terbatasnya jangkauan pasar pada wilayah lokal Pontianak.

Hasil identifikasi kebutuhan menekankan pada pentingnya perluasan jangkauan pasar melalui platform B2C berbasis web yang mampu menyajikan informasi produk secara transparan, seperti ketersediaan stok per ukuran, harga terkini, kondisi barang, dan galeri foto yang lengkap. Fokus pengembangan diarahkan pula pada penyediaan proses transaksi yang terdigitalisasi secara menyeluruh, mulai dari pemilihan produk, penghitungan ongkos kirim otomatis, pembayaran digital, hingga layanan purna jual yang mencakup ulasan produk dan pengajuan klaim garansi secara daring. Dirumuskan juga kebutuhan akan panel pengelolaan yang efisien bagi staf dan pemilik toko guna memantau seluruh aktivitas transaksi dan mengelola data produk secara terpusat. Kesepakatan yang dicapai dalam fase perencanaan ini menjadi landasan utama untuk memastikan bahwa sistem yang dirancang dapat mengatasi hambatan operasional yang ada dan meningkatkan daya saing toko di pasar digital.

---

### 5.1.1.1 Kebutuhan Fungsional

Kebutuhan fungsional mencakup berbagai layanan atau fungsi yang harus disediakan oleh sistem agar dapat berjalan sesuai dengan tujuan pengembangan. Sistem B2C UMKM ZTP Sneakers ini memiliki spesifikasi fungsional yang terbagi menjadi dua bagian utama sebagai berikut:

a. Halaman Admin

Staf dan pemilik toko memiliki akses ke panel pengelolaan dengan dua tingkat kewenangan yang berbeda. Berikut adalah rincian fungsi yang tersedia pada sisi pengelolaan:

1. Staf dapat melakukan pengelolaan data produk yang mencakup penambahan, pembaruan, hingga penonaktifan informasi detail seperti nama produk, merek, kategori, harga, kondisi barang, dan ketersediaan stok per ukuran.

2. Staf memiliki fungsi untuk memantau serta memproses setiap pesanan dan transaksi yang dilakukan oleh konsumen secara terpusat melalui dasbor, termasuk mengubah status pesanan dan memasukkan nomor resi pengiriman.

3. Staf dapat melihat data pelanggan yang terdaftar untuk memastikan akurasi informasi kontak dan mendukung kebutuhan komunikasi terkait pengiriman maupun penanganan keluhan.

4. Staf menyediakan layanan penanganan klaim garansi terhadap kendala produk yang dilaporkan pelanggan, mencakup penelaahan bukti, penetapan keputusan, dan penulisan catatan resolusi untuk disampaikan kepada pelanggan.

5. Pemilik toko dapat memantau laporan penjualan digital melalui dasbor analitik untuk menganalisis tren permintaan, performa operasional toko, serta mengunduh laporan dalam format Excel secara berkala.

6. Pemilik toko dapat mengelola konten promosi berupa banner halaman utama, kode voucher diskon, serta akun staf operasional melalui panel administrasi yang dilindungi hak akses khusus.

b. Halaman Konsumen

Konsumen terdiri dari dua kelompok, yaitu pengunjung yang belum memiliki akun dan pelanggan yang telah terdaftar. Berikut adalah rincian fungsi yang tersedia pada sisi konsumen:

1. Pengunjung dapat melihat seluruh katalog produk beserta detail lengkapnya, melakukan pencarian produk secara langsung tanpa perlu memuat ulang halaman, serta memfilter dan mengurutkan produk berdasarkan merek, kategori, ukuran, warna, kondisi, dan harga.

2. Pengunjung dapat melakukan pendaftaran akun baru menggunakan alamat surel dan nomor telepon, masuk ke akun yang sudah ada, serta menggunakan akun Google sebagai alternatif proses masuk.

3. Pelanggan dapat mengelola keranjang belanja secara langsung, menyimpan produk ke dalam daftar keinginan, dan menerima notifikasi otomatis apabila stok produk yang diminati tersisa sangat sedikit.

4. Pelanggan dapat melakukan proses pembelian secara menyeluruh melalui tahapan pengisian alamat pengiriman, pemilihan layanan ekspedisi dengan kalkulasi ongkos kirim otomatis, penggunaan voucher diskon secara opsional, dan penyelesaian pembayaran melalui berbagai metode digital yang tersedia.

5. Pelanggan dapat memantau seluruh riwayat pesanan beserta linimasa status terkini, mengonfirmasi penerimaan barang, mencetak bukti pembayaran, memberikan ulasan produk setelah pesanan selesai, serta mengajukan klaim garansi dalam batas waktu yang ditentukan.

6. Pelanggan menerima notifikasi di dalam aplikasi secara otomatis untuk setiap perubahan status pesanan maupun status penanganan klaim garansi, serta dapat memperbarui data profil akun kapan saja.

---

### 5.1.1.2 Kebutuhan Non-Fungsional

Kebutuhan non-fungsional mendefinisikan properti sistem dan batasan teknis yang harus dipenuhi agar sistem dapat beroperasi secara optimal dan memberikan pengalaman pengguna yang baik, di antaranya sebagai berikut:

a. Pengembangan Platform B2C

Platform dibangun menggunakan bahasa pemrograman Python dalam membuat fungsi back-end. Bahasa lainnya yang digunakan yaitu HTML, CSS, dan JavaScript untuk membangun fungsi front-end. Library HTMX digunakan sebagai pendukung dalam merancang interaktivitas antarmuka tanpa perlu memuat ulang halaman pada platform B2C. Pengelolaan data menggunakan sistem manajemen basis data PostgreSQL 16.

b. Kebutuhan Perangkat Lunak

Perangkat lunak merupakan sebuah hal yang penting dalam mendukung pengembangan dan pengoperasian sistem. Berikut adalah perangkat lunak yang digunakan dalam pengembangan platform ZTP Sneakers:

1. Python 3.12 sebagai bahasa pemrograman utama pada sisi back-end.
2. Django 5.2 sebagai kerangka kerja web yang menangani routing, ORM basis data, autentikasi pengguna, dan logika bisnis.
3. HTMX 2.x sebagai pustaka front-end untuk pembaruan konten halaman secara parsial tanpa muat ulang penuh.
4. Tailwind CSS 3.x sebagai kerangka kerja CSS untuk menyusun antarmuka yang responsif.
5. PostgreSQL 16 sebagai sistem manajemen basis data relasional.
6. Git sebagai sistem kendali versi dalam proses pengembangan.
7. Visual Studio Code sebagai editor kode utama selama proses pengembangan.

c. Kebutuhan Perangkat Keras

Pengembangan dan pengoperasian sistem memerlukan spesifikasi perangkat keras yang memadai. Spesifikasi minimum perangkat yang digunakan dalam proses pengembangan adalah sebagai berikut:

1. Prosesor dengan kecepatan minimal 2.0 GHz dan dukungan multi-core.
2. Memori RAM minimal 8 GB untuk mendukung proses pengembangan dan pengujian secara bersamaan.
3. Ruang penyimpanan minimal 20 GB untuk menampung berkas proyek, basis data, dan dependensi sistem.
4. Koneksi internet yang stabil untuk mengakses layanan API eksternal seperti Midtrans dan RajaOngkir selama pengembangan dan pengujian.

d. Keamanan Sistem

Sistem dirancang dengan memperhatikan aspek keamanan pada setiap lapisan. Seluruh masukan dari pengguna divalidasi di sisi peladen sebelum diproses untuk mencegah masukan yang berbahaya. Perlindungan terhadap serangan pemalsuan permintaan lintas situs aktif pada semua formulir. Kata sandi disimpan dalam bentuk yang telah melalui proses enkripsi satu arah menggunakan algoritma PBKDF2. Pemberitahuan pembayaran dari Midtrans diverifikasi keasliannya menggunakan tanda tangan digital SHA-512 untuk mencegah manipulasi data transaksi. Akses ke panel pengelolaan dilindungi oleh mekanisme autentikasi berbasis grup pengguna sehingga hanya pihak yang berwenang yang dapat mengakses fungsi administrasi.

---

## 5.1.2 Fase User Design

Fase User Design merupakan tahap perancangan sistem yang dilaksanakan setelah seluruh kebutuhan berhasil diidentifikasi. Pada fase ini, rancangan konkret sistem diwujudkan berdasarkan kebutuhan yang telah dirumuskan, mencakup arsitektur platform, rancangan basis data, diagram hubungan antara entitas, dan pemodelan perilaku sistem.

---

### 5.1.2.1 Arsitektur Platform B2C

Platform ZTP Sneakers dibangun di atas kerangka kerja Django menggunakan pola arsitektur Model-View-Template (MVT). Pola ini memisahkan tanggung jawab sistem ke dalam tiga lapisan: lapisan Model yang menangani struktur dan logika basis data, lapisan View yang memproses permintaan dari pengguna dan menyiapkan data untuk ditampilkan, serta lapisan Template yang mengatur penyajian antarmuka kepada pengguna akhir.

Pendekatan modular diterapkan dengan memisahkan setiap domain bisnis ke dalam aplikasi Django tersendiri. Modul userauths menangani autentikasi dan profil pengguna, modul products mengelola data katalog, modul orders menangani seluruh proses transaksi mulai dari keranjang hingga garansi, modul storefront menyajikan antarmuka publik bagi pengunjung dan pelanggan, modul admintoko menyediakan panel pengelolaan bagi staf, serta modul core menyediakan komponen bersama seperti sistem notifikasi dan pengolah konteks global.

Tabel 5.1 menyajikan komponen teknologi yang digunakan pada setiap lapisan sistem.

Tabel 5.1 Komponen Teknologi Platform ZTP Sneakers

| Komponen | Teknologi | Fungsi dalam Sistem |
|---|---|---|
| Kerangka Kerja Utama | Django 5.2 | Pengelolaan routing URL, ORM basis data, autentikasi, dan logika bisnis |
| Interaktivitas Frontend | HTMX 2.x | Pembaruan konten halaman secara parsial tanpa muat ulang penuh |
| Penyusunan Tampilan | Tailwind CSS 3.x | Antarmuka responsif berbasis utilitas |
| Basis Data | PostgreSQL 16 | Penyimpanan data relasional |
| Gerbang Pembayaran | Midtrans Snap | Pemrosesan pembayaran digital berbagai metode |
| Layanan Ongkos Kirim | RajaOngkir Komerce v1 | Penghitungan ongkos kirim nasional secara otomatis |
| Autentikasi Pihak Ketiga | django-allauth | Login menggunakan surel dan akun Google OAuth |
| Antarmuka Admin | Jazzmin | Kustomisasi tampilan panel Django Admin |
| Penyajian Berkas Statis | WhiteNoise | Melayani aset statis langsung dari aplikasi |
| Penerapan Sistem | cPanel + Passenger WSGI | Hosting pada shared hosting berbasis cPanel |

---

### 5.1.2.2 Rancangan Basis Data

Rancangan basis data platform ZTP Sneakers disusun melalui proses normalisasi yang bertahap dari bentuk data mentah yang belum terstruktur hingga mencapai Bentuk Normal Ketiga (3NF). Proses normalisasi ini bertujuan untuk menghilangkan redundansi data, meminimalkan anomali dalam operasi penyisipan, perubahan, dan penghapusan data, serta memastikan bahwa setiap atribut dalam basis data hanya menyimpan satu jenis informasi yang tepat.

---

#### a. Normalisasi Basis Data

Normalisasi basis data adalah proses pengorganisasian struktur tabel dalam basis data relasional untuk mengurangi redundansi dan ketergantungan data yang tidak diinginkan. Proses ini dilaksanakan secara bertahap melalui empat tahap berikut.

Unnormalized Form (UNF): Pada UNF, seluruh atribut akan dimasukkan dalam satu entitas tanpa pemisahan yang terstruktur. UNF tidak mewajibkan atribut yang dimasukkan harus sesuai dengan format tertentu. UNF memungkinkan adanya data berulang yang dapat menjadi masalah saat dilakukan manipulasi data, dan hal ini biasa dikenal dengan anomali data.

First Normal Form (1NF): 1NF mewajibkan setiap kolom memiliki nilai yang unik dan tidak ada kelompok data yang berulang dalam satu barisnya. Pada 1NF akan dilakukan pengelompokan beberapa tipe data yang sejenis sehingga dapat mengatasi anomali data.

Second Normal Form (2NF): 2NF mewajibkan setiap kolom dalam tabel hanya bergantung pada satu kunci primer dan tidak bergantung pada kolom lain dalam tabel. 2NF akan mewajibkan setiap tabel yang sudah dipisahkan memiliki kunci primer tersendiri.

Third Normal Form (3NF): 3NF mewajibkan setiap kolom dalam tabel hanya bergantung pada kunci primer dan tidak bergantung pada kolom lain yang bukan kunci dalam tabel. 3NF akan memisahkan atribut yang tidak bergantung langsung dengan kunci primer, tetapi bergantung pada atribut non-key lainnya.

Berikut adalah hasil penerapan normalisasi pada basis data platform ZTP Sneakers.

UNF (Unnormalized Form)

Seluruh atribut dari semua entitas dikumpulkan dalam satu tabel besar sebelum distrukturkan:

tb_ztpsneakers = id_user + username + email + password + last_login + is_superuser + is_active + is_staff + date_joined + full_name + phone_number + address_line1 + address_line2 + city + avatar + role + id_userprofile + userprofile_created_at + userprofile_updated_at + id_notification + notification_title + notification_message + notification_link + notification_is_read + notification_created_at + id_category + category_name + category_slug + category_icon + category_order + id_brand + brand_name + brand_slug + brand_logo + id_product + product_name + product_color + product_color_secondary + product_slug + product_description + product_condition + product_price + product_crossed_price + product_is_active + product_is_featured + product_created_at + id_product_image + product_image_file + product_image_is_primary + product_image_order + id_product_size + product_size + product_size_stock + id_banner + banner_title + banner_subtitle + banner_image + banner_link + banner_order + banner_is_active + id_review + review_rating + review_comment + review_image1 + review_image2 + review_image3 + review_is_visible + review_created_at + id_voucher + voucher_code + voucher_discount_type + voucher_discount_value + voucher_min_purchase + voucher_valid_from + voucher_valid_to + voucher_is_active + id_wishlist + wishlist_created_at + id_cart + cart_session_key + cart_created_at + cart_updated_at + id_cart_item + cart_item_quantity + id_order + order_number + order_status + order_midtrans_transaction_id + order_courier + order_shipping_service + order_shipping_cost + order_tracking_number + order_discount_amount + order_subtotal + order_total + order_created_at + order_updated_at + id_order_item + order_item_size_str + order_item_product_name + order_item_price + order_item_quantity + id_shipping_address + shipping_recipient_name + shipping_phone_number + shipping_province_id + shipping_province_name + shipping_city_id + shipping_city_name + shipping_district_name + shipping_postal_code + shipping_full_address + id_warranty_claim + warranty_kategori + warranty_reason + warranty_evidence_image + warranty_status + warranty_admin_notes + warranty_created_at + warranty_updated_at + id_footer_icon + footer_icon_title + footer_icon_image + footer_icon_order

1NF (Bentuk Normal Pertama)

Setiap entitas dipisahkan ke dalam tabel tersendiri dengan atribut yang bersifat atomik dan masing-masing memiliki kunci utama:

```
tb_user             = id_user + username + email + password + last_login +
                      is_superuser + is_active + is_staff + date_joined +
                      full_name + phone_number + address_line1 +
                      address_line2 + city + avatar + role

tb_userprofile      = id_userprofile + id_user + created_at + updated_at

tb_notification     = id_notification + id_user + title + message +
                      link + is_read + created_at

tb_category         = id_category + name + slug + icon + order

tb_brand            = id_brand + name + slug + logo

tb_product          = id_product + id_brand + id_category + name +
                      color + color_secondary + slug + description +
                      condition + price + crossed_price + is_active +
                      is_featured + created_at

tb_product_image    = id_product_image + id_product + image +
                      is_primary + order

tb_product_size     = id_product_size + id_product + size + stock

tb_banner           = id_banner + title + subtitle + image + link +
                      order + is_active

tb_review           = id_review + id_product + id_user + id_order_item +
                      rating + comment + image1 + image2 + image3 +
                      is_visible + created_at

tb_voucher          = id_voucher + code + discount_type + discount_value +
                      min_purchase + valid_from + valid_to + is_active

tb_wishlist         = id_wishlist + id_user + id_product + created_at

tb_cart             = id_cart + id_user + session_key +
                      created_at + updated_at

tb_cart_item        = id_cart_item + id_cart + id_product +
                      id_product_size + quantity

tb_order            = id_order + id_user + id_voucher + order_number +
                      status + midtrans_transaction_id + courier +
                      shipping_service + shipping_cost + tracking_number +
                      discount_amount + subtotal + total +
                      created_at + updated_at

tb_order_item       = id_order_item + id_order + id_product +
                      size_str + product_name + price + quantity

tb_shipping_address = id_shipping_address + id_order + recipient_name +
                      phone_number + province_id + province_name +
                      city_id + city_name + district_name +
                      postal_code + full_address

tb_warranty_claim   = id_warranty_claim + id_order_item + id_user +
                      kategori + reason + evidence_image + status +
                      admin_notes + created_at + updated_at

tb_footer_icon      = id_footer_icon + title + image + order
```

2NF (Bentuk Normal Kedua)

Setiap tabel menggunakan kunci utama pengganti (surrogate key) berupa identifikasi numerik tunggal sehingga seluruh atribut non-kunci bergantung penuh pada kunci utama masing-masing tabel. Struktur tabel pada 2NF sama dengan 1NF karena tidak ada ketergantungan parsial yang ditemukan. Adapun penjelasan khusus: pada tb_order_item, atribut product_name dan price merupakan salinan historis data saat transaksi berlangsung, bukan ketergantungan parsial, sehingga struktur ini tetap valid dan dipertahankan.

```
tb_user             = id_user + username + email + password + last_login +
                      is_superuser + is_active + is_staff + date_joined +
                      full_name + phone_number + address_line1 +
                      address_line2 + city + avatar + role

tb_userprofile      = id_userprofile + id_user + created_at + updated_at

tb_notification     = id_notification + id_user + title + message +
                      link + is_read + created_at

tb_category         = id_category + name + slug + icon + order

tb_brand            = id_brand + name + slug + logo

tb_product          = id_product + id_brand + id_category + name +
                      color + color_secondary + slug + description +
                      condition + price + crossed_price + is_active +
                      is_featured + created_at

tb_product_image    = id_product_image + id_product + image +
                      is_primary + order

tb_product_size     = id_product_size + id_product + size + stock

tb_banner           = id_banner + title + subtitle + image + link +
                      order + is_active

tb_review           = id_review + id_product + id_user + id_order_item +
                      rating + comment + image1 + image2 + image3 +
                      is_visible + created_at

tb_voucher          = id_voucher + code + discount_type + discount_value +
                      min_purchase + valid_from + valid_to + is_active

tb_wishlist         = id_wishlist + id_user + id_product + created_at

tb_cart             = id_cart + id_user + session_key +
                      created_at + updated_at

tb_cart_item        = id_cart_item + id_cart + id_product +
                      id_product_size + quantity

tb_order            = id_order + id_user + id_voucher + order_number +
                      status + midtrans_transaction_id + courier +
                      shipping_service + shipping_cost + tracking_number +
                      discount_amount + subtotal + total +
                      created_at + updated_at

tb_order_item       = id_order_item + id_order + id_product +
                      size_str + product_name + price + quantity

tb_shipping_address = id_shipping_address + id_order + recipient_name +
                      phone_number + province_id + province_name +
                      city_id + city_name + district_name +
                      postal_code + full_address

tb_warranty_claim   = id_warranty_claim + id_order_item + id_user +
                      kategori + reason + evidence_image + status +
                      admin_notes + created_at + updated_at

tb_footer_icon      = id_footer_icon + title + image + order
```

3NF (Bentuk Normal Ketiga)

Kunci utama ditandai dengan simbol @ (primary key) dan kunci asing ditandai dengan simbol @@ (foreign key). Tidak ditemukan ketergantungan transitif pada seluruh tabel sehingga struktur telah memenuhi syarat 3NF:

```
tb_user             = @id_user + username + email + password + last_login +
                      is_superuser + is_active + is_staff + date_joined +
                      full_name + phone_number + address_line1 +
                      address_line2 + city + avatar + role

tb_userprofile      = @id_userprofile + @@id_user + created_at + updated_at

tb_notification     = @id_notification + @@id_user + title + message +
                      link + is_read + created_at

tb_category         = @id_category + name + slug + icon + order

tb_brand            = @id_brand + name + slug + logo

tb_product          = @id_product + @@id_brand + @@id_category + name +
                      color + color_secondary + slug + description +
                      condition + price + crossed_price + is_active +
                      is_featured + created_at

tb_product_image    = @id_product_image + @@id_product + image +
                      is_primary + order

tb_product_size     = @id_product_size + @@id_product + size + stock

tb_banner           = @id_banner + title + subtitle + image + link +
                      order + is_active

tb_review           = @id_review + @@id_product + @@id_user +
                      @@id_order_item + rating + comment +
                      image1 + image2 + image3 + is_visible + created_at

tb_voucher          = @id_voucher + code + discount_type + discount_value +
                      min_purchase + valid_from + valid_to + is_active

tb_wishlist         = @id_wishlist + @@id_user + @@id_product + created_at

tb_cart             = @id_cart + @@id_user + session_key +
                      created_at + updated_at

tb_cart_item        = @id_cart_item + @@id_cart + @@id_product +
                      @@id_product_size + quantity

tb_order            = @id_order + @@id_user + @@id_voucher + order_number +
                      status + midtrans_transaction_id + courier +
                      shipping_service + shipping_cost + tracking_number +
                      discount_amount + subtotal + total +
                      created_at + updated_at

tb_order_item       = @id_order_item + @@id_order + @@id_product +
                      size_str + product_name + price + quantity

tb_shipping_address = @id_shipping_address + @@id_order + recipient_name +
                      phone_number + province_id + province_name +
                      city_id + city_name + district_name +
                      postal_code + full_address

tb_warranty_claim   = @id_warranty_claim + @@id_order_item + @@id_user +
                      kategori + reason + evidence_image + status +
                      admin_notes + created_at + updated_at

tb_footer_icon      = @id_footer_icon + title + image + order
```

---


#### b. Spesifikasi Tabel Database

Spesifikasi tabel database bertujuan untuk memberikan gambaran teknis mengenai bagaimana data disimpan dan diorganisir dalam sistem basis data. Berikut adalah tabel-tabel utama yang terdapat dalam basis data platform B2C ZTP Sneakers:

1. Tabel Pengguna

Arsitektur data pengguna pada platform ZTP Sneakers memisahkan data kredensial keamanan dengan informasi profil pengguna. Pemisahan ini dilakukan dengan menerapkan relasi satu ke satu antara tabel tb_user dan tb_userprofile. Pendekatan ini bertujuan untuk meningkatkan aspek keamanan sistem serta menjaga agar proses pemuatan sesi masuk tetap ringan tanpa harus memproses data profil yang bersifat opsional.

Tabel 5.2 Tabel tb_user

| No | Nama Kolom | Tipe Data | Panjang | NULL / NOT NULL | Default |
|---|---|---|---|---|---|
| 1 | id_user | INTEGER | - | NOT NULL | Auto Increment (PK) |
| 2 | username | VARCHAR | 150 | NOT NULL | - |
| 3 | email | VARCHAR | 254 | NOT NULL | - |
| 4 | password | VARCHAR | 128 | NOT NULL | - |
| 5 | last_login | DATETIME | - | NULL | NULL |
| 6 | is_superuser | BOOLEAN | - | NOT NULL | FALSE |
| 7 | is_staff | BOOLEAN | - | NOT NULL | FALSE |
| 8 | is_active | BOOLEAN | - | NOT NULL | TRUE |
| 9 | date_joined | DATETIME | - | NOT NULL | Now |
| 10 | full_name | VARCHAR | 150 | NULL | NULL |
| 11 | phone_number | VARCHAR | 20 | NULL | NULL |
| 12 | address_line1 | VARCHAR | 255 | NULL | NULL |
| 13 | address_line2 | VARCHAR | 255 | NULL | NULL |
| 14 | city | VARCHAR | 100 | NULL | NULL |
| 15 | avatar | VARCHAR | 100 | NULL | NULL |
| 16 | role | VARCHAR | 20 | NOT NULL | customer |

Tabel 5.3 Tabel tb_userprofile

| No | Nama Kolom | Tipe Data | Panjang | NULL / NOT NULL | Default |
|---|---|---|---|---|---|
| 1 | id_userprofile | INTEGER | - | NOT NULL | Auto Increment (PK) |
| 2 | id_user | INTEGER | - | NOT NULL | FK → tb_user |
| 3 | created_at | DATETIME | - | NOT NULL | Now |
| 4 | updated_at | DATETIME | - | NOT NULL | Now |

2. Tabel Notifikasi

Tabel tb_notification menyimpan seluruh pemberitahuan yang diterima oleh pengguna. Notifikasi dibuat secara otomatis oleh sistem setiap kali terjadi perubahan status pesanan atau klaim garansi.

Tabel 5.4 Tabel tb_notification

| No | Nama Kolom | Tipe Data | Panjang | NULL / NOT NULL | Default |
|---|---|---|---|---|---|
| 1 | id_notification | INTEGER | - | NOT NULL | Auto Increment (PK) |
| 2 | id_user | INTEGER | - | NOT NULL | FK → tb_user |
| 3 | title | VARCHAR | 255 | NOT NULL | - |
| 4 | message | TEXT | - | NOT NULL | - |
| 5 | link | VARCHAR | 255 | NULL | NULL |
| 6 | is_read | BOOLEAN | - | NOT NULL | FALSE |
| 7 | created_at | DATETIME | - | NOT NULL | Now |

3. Tabel Kategori

Tabel tb_category menyimpan data kategori produk yang digunakan untuk mengorganisir produk dalam katalog.

Tabel 5.5 Tabel tb_category

| No | Nama Kolom | Tipe Data | Panjang | NULL / NOT NULL | Default |
|---|---|---|---|---|---|
| 1 | id_category | INTEGER | - | NOT NULL | Auto Increment (PK) |
| 2 | name | VARCHAR | 100 | NOT NULL | - |
| 3 | slug | VARCHAR | 100 | NOT NULL | - |
| 4 | icon | VARCHAR | 100 | NULL | NULL |
| 5 | order | INTEGER | - | NOT NULL | 0 |

4. Tabel Merek

Tabel tb_brand menyimpan data merek produk sepatu yang tersedia di toko.

Tabel 5.6 Tabel tb_brand

| No | Nama Kolom | Tipe Data | Panjang | NULL / NOT NULL | Default |
|---|---|---|---|---|---|
| 1 | id_brand | INTEGER | - | NOT NULL | Auto Increment (PK) |
| 2 | name | VARCHAR | 100 | NOT NULL | - |
| 3 | slug | VARCHAR | 100 | NOT NULL | - |
| 4 | logo | VARCHAR | 100 | NULL | NULL |

5. Tabel Produk

Tabel tb_product merupakan tabel inti yang menyimpan seluruh informasi produk sepatu. Setiap produk terhubung ke satu merek dan satu kategori, serta dapat memiliki banyak gambar dan banyak varian ukuran.

Tabel 5.7 Tabel tb_product

| No | Nama Kolom | Tipe Data | Panjang | NULL / NOT NULL | Default |
|---|---|---|---|---|---|
| 1 | id_product | INTEGER | - | NOT NULL | Auto Increment (PK) |
| 2 | id_brand | INTEGER | - | NOT NULL | FK → tb_brand |
| 3 | id_category | INTEGER | - | NULL | FK → tb_category |
| 4 | name | VARCHAR | 200 | NOT NULL | - |
| 5 | color | VARCHAR | 20 | NOT NULL | multi |
| 6 | color_secondary | VARCHAR | 20 | NULL | NULL |
| 7 | slug | VARCHAR | 200 | NOT NULL | - |
| 8 | description | TEXT | - | NOT NULL | - |
| 9 | condition | VARCHAR | 20 | NOT NULL | new |
| 10 | price | DECIMAL | 12,2 | NOT NULL | - |
| 11 | crossed_price | DECIMAL | 12,2 | NULL | NULL |
| 12 | is_active | BOOLEAN | - | NOT NULL | TRUE |
| 13 | is_featured | BOOLEAN | - | NOT NULL | FALSE |
| 14 | created_at | DATETIME | - | NOT NULL | Now |

6. Tabel Gambar Produk

Tabel tb_product_image menyimpan data gambar yang dimiliki oleh setiap produk. Satu produk dapat memiliki lebih dari satu gambar, dengan satu gambar ditandai sebagai gambar utama.

Tabel 5.8 Tabel tb_product_image

| No | Nama Kolom | Tipe Data | Panjang | NULL / NOT NULL | Default |
|---|---|---|---|---|---|
| 1 | id_product_image | INTEGER | - | NOT NULL | Auto Increment (PK) |
| 2 | id_product | INTEGER | - | NOT NULL | FK → tb_product |
| 3 | image | VARCHAR | 100 | NOT NULL | - |
| 4 | is_primary | BOOLEAN | - | NOT NULL | FALSE |
| 5 | order | INTEGER | - | NOT NULL | 0 |

7. Tabel Ukuran Produk

Tabel tb_product_size menyimpan data varian ukuran beserta jumlah stok yang tersedia untuk setiap ukuran dari setiap produk.

Tabel 5.9 Tabel tb_product_size

| No | Nama Kolom | Tipe Data | Panjang | NULL / NOT NULL | Default |
|---|---|---|---|---|---|
| 1 | id_product_size | INTEGER | - | NOT NULL | Auto Increment (PK) |
| 2 | id_product | INTEGER | - | NOT NULL | FK → tb_product |
| 3 | size | VARCHAR | 10 | NOT NULL | - |
| 4 | stock | INTEGER | - | NOT NULL | 0 |

8. Tabel Banner

Tabel tb_banner menyimpan data gambar banner promosi yang ditampilkan pada halaman utama.

Tabel 5.10 Tabel tb_banner

| No | Nama Kolom | Tipe Data | Panjang | NULL / NOT NULL | Default |
|---|---|---|---|---|---|
| 1 | id_banner | INTEGER | - | NOT NULL | Auto Increment (PK) |
| 2 | title | VARCHAR | 200 | NOT NULL | - |
| 3 | subtitle | VARCHAR | 200 | NULL | NULL |
| 4 | image | VARCHAR | 100 | NOT NULL | - |
| 5 | link | VARCHAR | 200 | NULL | NULL |
| 6 | order | INTEGER | - | NOT NULL | 0 |
| 7 | is_active | BOOLEAN | - | NOT NULL | TRUE |


9. Tabel Ulasan Produk

Tabel tb_review menyimpan data ulasan yang diberikan oleh pelanggan setelah pesanan selesai. Setiap ulasan terhubung ke satu item pesanan untuk memastikan ulasan hanya dapat diberikan oleh pelanggan yang benar-benar telah membeli produk tersebut.

Tabel 5.11 Tabel tb_review

| No | Nama Kolom | Tipe Data | Panjang | NULL / NOT NULL | Default |
|---|---|---|---|---|---|
| 1 | id_review | INTEGER | - | NOT NULL | Auto Increment (PK) |
| 2 | id_product | INTEGER | - | NOT NULL | FK → tb_product |
| 3 | id_user | INTEGER | - | NOT NULL | FK → tb_user |
| 4 | id_order_item | INTEGER | - | NULL | FK → tb_order_item |
| 5 | rating | SMALLINT | - | NOT NULL | - |
| 6 | comment | TEXT | - | NOT NULL | - |
| 7 | image1 | VARCHAR | 100 | NULL | NULL |
| 8 | image2 | VARCHAR | 100 | NULL | NULL |
| 9 | image3 | VARCHAR | 100 | NULL | NULL |
| 10 | is_visible | BOOLEAN | - | NOT NULL | TRUE |
| 11 | created_at | DATETIME | - | NOT NULL | Now |

10. Tabel Voucher

Tabel tb_voucher menyimpan data kode voucher diskon yang dapat digunakan oleh pelanggan pada saat melakukan pembelian.

Tabel 5.12 Tabel tb_voucher

| No | Nama Kolom | Tipe Data | Panjang | NULL / NOT NULL | Default |
|---|---|---|---|---|---|
| 1 | id_voucher | INTEGER | - | NOT NULL | Auto Increment (PK) |
| 2 | code | VARCHAR | 20 | NOT NULL | - |
| 3 | discount_type | VARCHAR | 20 | NOT NULL | - |
| 4 | discount_value | DECIMAL | 10,2 | NOT NULL | - |
| 5 | min_purchase | DECIMAL | 12,2 | NOT NULL | 0 |
| 6 | valid_from | DATETIME | - | NOT NULL | - |
| 7 | valid_to | DATETIME | - | NOT NULL | - |
| 8 | is_active | BOOLEAN | - | NOT NULL | TRUE |

11. Tabel Daftar Keinginan

Tabel tb_wishlist menyimpan data produk yang disimpan ke dalam daftar keinginan oleh pelanggan. Setiap kombinasi pengguna dan produk hanya dapat disimpan satu kali.

Tabel 5.13 Tabel tb_wishlist

| No | Nama Kolom | Tipe Data | Panjang | NULL / NOT NULL | Default |
|---|---|---|---|---|---|
| 1 | id_wishlist | INTEGER | - | NOT NULL | Auto Increment (PK) |
| 2 | id_user | INTEGER | - | NOT NULL | FK → tb_user |
| 3 | id_product | INTEGER | - | NOT NULL | FK → tb_product |
| 4 | created_at | DATETIME | - | NOT NULL | Now |

12. Tabel Keranjang Belanja

Tabel tb_cart menyimpan data keranjang belanja. Sistem mendukung dua jenis keranjang: keranjang untuk pengguna yang telah masuk akun yang disimpan permanen di basis data, dan keranjang untuk pengunjung yang tersimpan berdasarkan kunci sesi browser.

Tabel 5.14 Tabel tb_cart

| No | Nama Kolom | Tipe Data | Panjang | NULL / NOT NULL | Default |
|---|---|---|---|---|---|
| 1 | id_cart | INTEGER | - | NOT NULL | Auto Increment (PK) |
| 2 | id_user | INTEGER | - | NULL | FK → tb_user |
| 3 | session_key | VARCHAR | 40 | NULL | NULL |
| 4 | created_at | DATETIME | - | NOT NULL | Now |
| 5 | updated_at | DATETIME | - | NOT NULL | Now |

13. Tabel Item Keranjang

Tabel tb_cart_item menyimpan detail setiap item yang ditambahkan ke dalam keranjang belanja, termasuk produk yang dipilih, ukuran yang dipilih, dan jumlahnya.

Tabel 5.15 Tabel tb_cart_item

| No | Nama Kolom | Tipe Data | Panjang | NULL / NOT NULL | Default |
|---|---|---|---|---|---|
| 1 | id_cart_item | INTEGER | - | NOT NULL | Auto Increment (PK) |
| 2 | id_cart | INTEGER | - | NOT NULL | FK → tb_cart |
| 3 | id_product | INTEGER | - | NOT NULL | FK → tb_product |
| 4 | id_product_size | INTEGER | - | NOT NULL | FK → tb_product_size |
| 5 | quantity | INTEGER | - | NOT NULL | 1 |

14. Tabel Pesanan

Tabel tb_order merupakan tabel utama yang menyimpan data kepala transaksi pembelian. Setiap pesanan memiliki satu nomor pesanan unik dan mencatat informasi pengiriman, pembayaran, serta status terkini.

Tabel 5.16 Tabel tb_order

| No | Nama Kolom | Tipe Data | Panjang | NULL / NOT NULL | Default |
|---|---|---|---|---|---|
| 1 | id_order | INTEGER | - | NOT NULL | Auto Increment (PK) |
| 2 | id_user | INTEGER | - | NULL | FK → tb_user |
| 3 | id_voucher | INTEGER | - | NULL | FK → tb_voucher |
| 4 | order_number | VARCHAR | 50 | NOT NULL | - |
| 5 | status | VARCHAR | 20 | NOT NULL | pending |
| 6 | midtrans_transaction_id | VARCHAR | 100 | NULL | NULL |
| 7 | courier | VARCHAR | 50 | NOT NULL | - |
| 8 | shipping_service | VARCHAR | 100 | NOT NULL | - |
| 9 | shipping_cost | DECIMAL | 10,2 | NOT NULL | 0 |
| 10 | tracking_number | VARCHAR | 100 | NULL | NULL |
| 11 | discount_amount | DECIMAL | 10,2 | NOT NULL | 0 |
| 12 | subtotal | DECIMAL | 12,2 | NOT NULL | - |
| 13 | total | DECIMAL | 12,2 | NOT NULL | - |
| 14 | created_at | DATETIME | - | NOT NULL | Now |
| 15 | updated_at | DATETIME | - | NOT NULL | Now |

15. Tabel Item Pesanan

Tabel tb_order_item menyimpan rincian setiap produk yang termasuk dalam satu pesanan. Nama produk dan harga disimpan sebagai salinan historis pada saat transaksi berlangsung agar catatan pembelian tetap akurat meskipun data produk asli berubah di kemudian hari.

Tabel 5.17 Tabel tb_order_item

| No | Nama Kolom | Tipe Data | Panjang | NULL / NOT NULL | Default |
|---|---|---|---|---|---|
| 1 | id_order_item | INTEGER | - | NOT NULL | Auto Increment (PK) |
| 2 | id_order | INTEGER | - | NOT NULL | FK → tb_order |
| 3 | id_product | INTEGER | - | NULL | FK → tb_product |
| 4 | size_str | VARCHAR | 10 | NOT NULL | - |
| 5 | product_name | VARCHAR | 200 | NOT NULL | - |
| 6 | price | DECIMAL | 12,2 | NOT NULL | - |
| 7 | quantity | INTEGER | - | NOT NULL | 1 |

16. Tabel Alamat Pengiriman

Tabel tb_shipping_address menyimpan data alamat tujuan pengiriman untuk setiap pesanan. Setiap pesanan memiliki tepat satu alamat pengiriman yang dicatat pada saat proses checkout berlangsung.

Tabel 5.18 Tabel tb_shipping_address

| No | Nama Kolom | Tipe Data | Panjang | NULL / NOT NULL | Default |
|---|---|---|---|---|---|
| 1 | id_shipping_address | INTEGER | - | NOT NULL | Auto Increment (PK) |
| 2 | id_order | INTEGER | - | NOT NULL | FK → tb_order |
| 3 | recipient_name | VARCHAR | 100 | NOT NULL | - |
| 4 | phone_number | VARCHAR | 20 | NOT NULL | - |
| 5 | province_id | VARCHAR | 50 | NOT NULL | - |
| 6 | province_name | VARCHAR | 100 | NOT NULL | - |
| 7 | city_id | VARCHAR | 50 | NOT NULL | - |
| 8 | city_name | VARCHAR | 100 | NOT NULL | - |
| 9 | district_name | VARCHAR | 100 | NOT NULL | - |
| 10 | postal_code | VARCHAR | 20 | NOT NULL | - |
| 11 | full_address | TEXT | - | NOT NULL | - |

17. Tabel Klaim Garansi

Tabel tb_warranty_claim menyimpan data pengajuan klaim garansi yang diajukan oleh pelanggan untuk item pada pesanan yang telah selesai. Setiap item pesanan hanya dapat memiliki satu klaim garansi.

Tabel 5.19 Tabel tb_warranty_claim

| No | Nama Kolom | Tipe Data | Panjang | NULL / NOT NULL | Default |
|---|---|---|---|---|---|
| 1 | id_warranty_claim | INTEGER | - | NOT NULL | Auto Increment (PK) |
| 2 | id_order_item | INTEGER | - | NOT NULL | FK → tb_order_item |
| 3 | id_user | INTEGER | - | NOT NULL | FK → tb_user |
| 4 | kategori | VARCHAR | 50 | NOT NULL | lainnya |
| 5 | reason | TEXT | - | NOT NULL | - |
| 6 | evidence_image | VARCHAR | 100 | NOT NULL | - |
| 7 | status | VARCHAR | 20 | NOT NULL | pending |
| 8 | admin_notes | TEXT | - | NULL | NULL |
| 9 | created_at | DATETIME | - | NOT NULL | Now |
| 10 | updated_at | DATETIME | - | NOT NULL | Now |

18. Tabel Ikon Footer

Tabel tb_footer_icon menyimpan data ikon-ikon yang ditampilkan pada bagian bawah halaman, seperti logo metode pembayaran dan layanan ekspedisi yang tersedia.

Tabel 5.20 Tabel tb_footer_icon

| No | Nama Kolom | Tipe Data | Panjang | NULL / NOT NULL | Default |
|---|---|---|---|---|---|
| 1 | id_footer_icon | INTEGER | - | NOT NULL | Auto Increment (PK) |
| 2 | title | VARCHAR | 50 | NOT NULL | - |
| 3 | image | VARCHAR | 100 | NOT NULL | - |
| 4 | order | INTEGER | - | NOT NULL | 0 |

---

### 5.1.2.3 Entity Relationship Diagram (ERD)

Entity Relationship Diagram (ERD) merupakan gambaran visual yang menunjukkan bagaimana data-data dalam sistem saling terhubung satu sama lain. Diagram ini digunakan sebagai panduan dalam membangun struktur basis data agar setiap hubungan antar data terdefinisi dengan jelas sebelum proses pembangunan sistem dimulai.

Pada platform ZTP Sneakers, terdapat 18 tabel data utama yang saling berelasi untuk mendukung seluruh proses operasional toko. Setiap pengguna yang terdaftar memiliki satu profil akun dan dapat menerima banyak notifikasi dari sistem. Data produk terhubung ke merek dan kategori masing-masing, di mana setiap produk dapat memiliki beberapa foto dan beberapa pilihan ukuran dengan stok tersendiri. Ulasan dari pelanggan juga terhubung langsung ke produk yang dibeli. Pada sisi transaksi, setiap pengguna memiliki satu keranjang belanja yang dapat menampung banyak item. Setiap pesanan memiliki satu alamat pengiriman dan dapat memuat beberapa item, di mana masing-masing item berpotensi mendapatkan satu ulasan dan satu klaim garansi. Voucher diskon dapat digunakan pada banyak pesanan, sementara fitur daftar keinginan menghubungkan pengguna dengan produk yang ingin mereka simpan.

(Gambar ERD akan disisipkan pada bagian ini)

---

### 5.1.2.4 Unified Modeling Language (UML)

Unified Modeling Language (UML) merupakan bahasa pemodelan standar yang digunakan untuk menggambarkan struktur dan perilaku sistem perangkat lunak secara visual. Pada perancangan platform ZTP Sneakers, UML digunakan untuk memperjelas interaksi antar aktor, alur proses bisnis, urutan komunikasi antar komponen, serta hubungan antar kelas dalam sistem. Pemodelan UML yang dihasilkan mencakup empat jenis diagram, yaitu use case diagram, activity diagram, sequence diagram, dan class diagram.

---

#### a. Use Case Diagram

Use case diagram menggambarkan fungsionalitas sistem dari sudut pandang pengguna. Diagram ini menunjukkan siapa saja yang berinteraksi dengan sistem dan apa yang dapat mereka lakukan. Pada platform ZTP Sneakers, terdapat empat aktor yang terlibat dalam sistem, yaitu Pengunjung, Konsumen, Owner, dan Admin Toko.

Pengunjung merupakan pengguna yang belum memiliki akun dan dapat mengakses fitur-fitur publik seperti melihat produk, mencari produk, mengakses live chat, melihat FAQ dan informasi toko, serta mendaftar akun baru. Konsumen merupakan pengguna yang telah masuk ke akun dan memiliki akses lebih luas, termasuk mengelola wishlist, mengelola profil, mengelola keranjang belanja, menggunakan kupon, melakukan transaksi pembelian, melihat riwayat pesanan, serta dapat mengajukan klaim garansi dan memberikan rating sebagai perluasan dari fitur transaksi. Owner merupakan pemilik toko yang setelah masuk dapat mengelola seluruh data operasional termasuk produk, pesanan, klaim garansi, banner, kategori, kupon, merek, dan data pelanggan. Admin Toko memiliki akses yang serupa dengan Owner namun terbatas pada fungsi-fungsi operasional harian.

(Gambar 5.3 Use Case Diagram pada ZTP Sneakers)

Berikut adalah deskripsi use case untuk setiap aktor dalam sistem:

1. Deskripsi Use Case Aktor Pengunjung

Pengunjung adalah pengguna yang mengakses platform tanpa melakukan proses masuk. Pengunjung dapat melihat produk yang tersedia, mencari produk menggunakan fitur pencarian, menggunakan layanan live chat, membaca FAQ dan informasi toko, serta mendaftarkan akun baru untuk menjadi konsumen terdaftar.

Tabel 5.21 Deskripsi Use Case Aktor Pengunjung

| Nama Use Case | Melihat Produk |
|---|---|
| Aktor | Pengunjung |
| Pre-kondisi | Pengunjung membuka halaman katalog atau beranda platform. |
| Flow of Event | 1. Sistem menampilkan daftar produk aktif dalam format grid. 2. Pengunjung dapat mengklik kartu produk untuk membuka halaman detail. 3. Sistem menampilkan foto, nama, kondisi, harga, pilihan ukuran, dan stok tersedia. |
| Post-kondisi | Pengunjung mendapatkan informasi lengkap mengenai produk yang diminati. |

| Nama Use Case | Mencari Produk |
|---|---|
| Aktor | Pengunjung |
| Pre-kondisi | Pengunjung berada di halaman mana saja yang memiliki kolom pencarian pada navbar. |
| Flow of Event | 1. Pengunjung mengetikkan kata kunci pada kolom pencarian. 2. Sistem secara otomatis mengirim permintaan pencarian tanpa memuat ulang halaman. 3. Sistem menampilkan hingga lima hasil produk yang relevan sebagai saran. 4. Pengunjung dapat mengklik salah satu hasil untuk membuka halaman detail produk. |
| Post-kondisi | Pengunjung menemukan produk yang dicari dan dapat melanjutkan ke halaman detail. |

| Nama Use Case | Live Chat |
|---|---|
| Aktor | Pengunjung |
| Pre-kondisi | Pengunjung berada di halaman mana saja pada platform. |
| Flow of Event | 1. Pengunjung mengklik ikon widget live chat yang tersedia di pojok halaman. 2. Sistem membuka jendela percakapan Crisp. 3. Pengunjung mengetikkan pesan dan mengirimkannya. 4. Staf toko menerima dan membalas pesan melalui dasbor Crisp. |
| Post-kondisi | Pengunjung mendapatkan respons dari staf toko melalui saluran live chat. |

| Nama Use Case | Melihat FAQ dan Info |
|---|---|
| Aktor | Pengunjung |
| Pre-kondisi | Pengunjung membuka halaman FAQ atau informasi toko. |
| Flow of Event | 1. Sistem menampilkan halaman informasi yang berisi pertanyaan umum, kebijakan pengembalian, dan informasi toko. 2. Pengunjung membaca informasi yang tersedia. |
| Post-kondisi | Pengunjung memperoleh informasi yang dibutuhkan terkait kebijakan dan layanan toko. |

| Nama Use Case | Mendaftar Akun |
|---|---|
| Aktor | Pengunjung |
| Pre-kondisi | Pengunjung belum memiliki akun dan membuka halaman autentikasi. |
| Flow of Event | 1. Sistem menampilkan formulir pendaftaran. 2. Pengunjung mengisi nama lengkap, alamat surel, nomor telepon, kata sandi, dan konfirmasi kata sandi. 3. Pengunjung mengklik tombol daftar. 4. Sistem memvalidasi seluruh data yang dimasukkan. 5. Jika terdapat kesalahan, sistem menampilkan pesan kesalahan yang sesuai. 6. Jika data valid, sistem membuat akun baru dan melakukan proses masuk secara otomatis. |
| Post-kondisi | Akun baru berhasil dibuat dan pengunjung masuk sebagai konsumen terdaftar. |

| Nama Use Case | Login |
|---|---|
| Aktor | Pengunjung |
| Pre-kondisi | Pengunjung sudah memiliki akun dan membuka halaman autentikasi. |
| Flow of Event | 1. Sistem menampilkan formulir masuk. 2. Pengunjung memasukkan alamat surel atau nomor telepon. 3. Sistem memeriksa keberadaan akun berdasarkan pengenal yang dimasukkan. 4. Sistem menampilkan formulir kata sandi. 5. Pengunjung memasukkan kata sandi dan mengklik masuk. 6. Sistem memverifikasi kata sandi dan membuat sesi masuk. |
| Post-kondisi | Pengunjung berhasil masuk dan menjadi konsumen yang terautentikasi. |

2. Deskripsi Use Case Aktor Konsumen

Konsumen adalah pengguna yang telah masuk ke akun dan dapat mengakses seluruh fitur transaksional platform. Selain dapat melakukan semua yang bisa dilakukan pengunjung, konsumen memiliki akses ke fitur wishlist, keranjang belanja, proses pembelian, riwayat pesanan, ulasan, dan klaim garansi.

Tabel 5.22 Deskripsi Use Case Aktor Konsumen

| Nama Use Case | Mengelola Wishlist |
|---|---|
| Aktor | Konsumen |
| Pre-kondisi | Konsumen sudah masuk ke akun dan berada di halaman katalog atau detail produk. |
| Flow of Event | 1. Konsumen mengklik ikon wishlist pada kartu produk atau halaman detail. 2. Sistem memeriksa apakah produk sudah ada di daftar keinginan. 3. Jika belum ada, sistem menambahkan produk dan mengubah ikon menjadi aktif. 4. Jika sudah ada, sistem menghapus produk dan mengubah ikon menjadi tidak aktif. |
| Post-kondisi | Status wishlist produk diperbarui sesuai tindakan konsumen. |

| Nama Use Case | Mengelola Profil |
|---|---|
| Aktor | Konsumen |
| Pre-kondisi | Konsumen sudah masuk ke akun dan membuka halaman profil. |
| Flow of Event | 1. Sistem menampilkan formulir data profil yang sudah terisi. 2. Konsumen mengubah data yang ingin diperbarui seperti nama, nomor telepon, alamat, atau foto profil. 3. Konsumen mengklik simpan. 4. Sistem memvalidasi dan menyimpan perubahan ke basis data. |
| Post-kondisi | Data profil konsumen berhasil diperbarui. |

| Nama Use Case | Lihat Riwayat Pesanan |
|---|---|
| Aktor | Konsumen |
| Pre-kondisi | Konsumen sudah masuk ke akun. |
| Flow of Event | 1. Sistem menampilkan daftar seluruh pesanan konsumen beserta status terkininya. 2. Konsumen dapat mengklik pesanan untuk membuka halaman detail. 3. Sistem menampilkan linimasa status, detail item, informasi pengiriman, nomor resi, dan ringkasan biaya. |
| Post-kondisi | Konsumen mendapatkan informasi lengkap mengenai riwayat dan status pesanannya. |

| Nama Use Case | Mengelola Keranjang |
|---|---|
| Aktor | Konsumen |
| Pre-kondisi | Konsumen telah menambahkan produk ke keranjang belanja. |
| Flow of Event | 1. Sistem menampilkan daftar item di keranjang beserta jumlah dan total harga. 2. Konsumen dapat mengubah jumlah item menggunakan tombol tambah atau kurang. 3. Konsumen dapat menghapus item dari keranjang. 4. Sistem memperbarui total harga secara otomatis setiap ada perubahan. |
| Post-kondisi | Keranjang belanja diperbarui sesuai keinginan konsumen dan siap untuk proses checkout. |

| Nama Use Case | Menggunakan Kupon |
|---|---|
| Aktor | Konsumen |
| Pre-kondisi | Konsumen sedang dalam proses checkout dan memiliki kode voucher yang valid. |
| Flow of Event | 1. Konsumen memasukkan kode voucher pada kolom yang tersedia. 2. Konsumen mengklik terapkan. 3. Sistem memvalidasi kode terhadap masa berlaku, status aktif, dan nilai minimum pembelian. 4. Jika valid, sistem menampilkan nilai diskon pada ringkasan pembayaran. 5. Jika tidak valid, sistem menampilkan pesan kesalahan. |
| Post-kondisi | Diskon voucher berhasil diterapkan pada total pembayaran. |

| Nama Use Case | Tambah ke Keranjang |
|---|---|
| Aktor | Konsumen |
| Pre-kondisi | Konsumen berada di halaman detail produk dan telah memilih ukuran. |
| Flow of Event | 1. Konsumen memilih ukuran yang diinginkan dari pilihan yang tersedia. 2. Konsumen mengklik tombol tambah ke keranjang. 3. Sistem memvalidasi ketersediaan stok untuk ukuran yang dipilih. 4. Sistem menambahkan item ke keranjang dan memperbarui badge jumlah item di navbar. 5. Sistem menampilkan notifikasi konfirmasi. |
| Post-kondisi | Item produk berhasil ditambahkan ke keranjang belanja konsumen. |

| Nama Use Case | Melakukan Transaksi |
|---|---|
| Aktor | Konsumen |
| Pre-kondisi | Konsumen memiliki item di keranjang belanja dan sudah masuk ke akun. |
| Flow of Event | 1. Konsumen membuka halaman checkout dari keranjang belanja. 2. Konsumen mengisi data alamat pengiriman termasuk provinsi, kota, dan alamat lengkap. 3. Sistem menampilkan pilihan layanan ekspedisi beserta tarifnya. 4. Konsumen memilih layanan pengiriman yang diinginkan. 5. Konsumen mengkonfirmasi pesanan dan mengklik bayar sekarang. 6. Sistem membuat data pesanan dan menampilkan jendela pembayaran Midtrans. 7. Konsumen menyelesaikan pembayaran melalui metode yang dipilih. |
| Post-kondisi | Pesanan berhasil dibuat dan pembayaran berhasil diproses. |

| Nama Use Case | Lihat Status Pesanan |
|---|---|
| Aktor | Konsumen |
| Pre-kondisi | Konsumen memiliki pesanan yang sudah dibuat dan masuk ke akun. |
| Flow of Event | 1. Konsumen membuka halaman detail pesanan. 2. Sistem menampilkan linimasa status pesanan dari pembayaran hingga penerimaan. 3. Sistem menampilkan nomor resi dan informasi ekspedisi jika pesanan sudah dikirim. |
| Post-kondisi | Konsumen mengetahui status terkini pesanannya. |

| Nama Use Case | Mengajukan Klaim Garansi |
|---|---|
| Aktor | Konsumen |
| Pre-kondisi | Pesanan berstatus selesai, masih dalam periode tujuh hari garansi, dan belum pernah diajukan. |
| Flow of Event | 1. Konsumen membuka halaman detail pesanan dan mengklik laporkan masalah pada item yang bermasalah. 2. Sistem menampilkan formulir klaim garansi. 3. Konsumen memilih kategori masalah, mengisi penjelasan, dan mengunggah foto bukti. 4. Konsumen mengklik kirim laporan. 5. Sistem memvalidasi formulir dan menyimpan klaim dengan status menunggu. 6. Sistem mengirimkan notifikasi konfirmasi kepada konsumen. |
| Post-kondisi | Klaim garansi berhasil diajukan dan menunggu penanganan dari staf. |

| Nama Use Case | Memberikan Rating |
|---|---|
| Aktor | Konsumen |
| Pre-kondisi | Pesanan berstatus selesai dan item yang bersangkutan belum pernah diulas. |
| Flow of Event | 1. Konsumen membuka formulir ulasan dari halaman detail pesanan. 2. Konsumen memilih rating bintang satu sampai lima. 3. Konsumen menulis komentar ulasan. 4. Konsumen mengunggah foto bukti secara opsional. 5. Konsumen mengklik kirim ulasan. 6. Sistem menyimpan ulasan dan memperbarui rata-rata penilaian produk. |
| Post-kondisi | Ulasan berhasil tersimpan dan tampil di halaman detail produk. |

3. Deskripsi Use Case Aktor Owner

Owner adalah pemilik toko yang memiliki akses penuh ke seluruh fungsi pengelolaan sistem setelah melakukan proses masuk.

Tabel 5.23 Deskripsi Use Case Aktor Owner

| Nama Use Case | Kelola Produk |
|---|---|
| Aktor | Owner |
| Pre-kondisi | Owner sudah masuk ke panel administrasi. |
| Flow of Event | 1. Sistem menampilkan daftar seluruh produk yang terdaftar. 2. Owner dapat menekan tambah produk, mengisi formulir data produk termasuk nama, merek, kategori, harga, kondisi, warna, deskripsi, dan stok per ukuran, lalu menyimpan. 3. Owner dapat menekan edit pada produk tertentu untuk memperbarui data, lalu menyimpan. 4. Owner dapat mengaktifkan atau menonaktifkan produk dari katalog publik. 5. Sistem menyimpan semua perubahan ke basis data. |
| Post-kondisi | Data produk berhasil dikelola dan perubahan tercermin di katalog publik. |

| Nama Use Case | Kelola Pesanan |
|---|---|
| Aktor | Owner |
| Pre-kondisi | Owner sudah masuk ke panel administrasi. |
| Flow of Event | 1. Sistem menampilkan daftar seluruh pesanan dengan kemampuan penyaringan berdasarkan status. 2. Owner dapat memilih pesanan dan mengubah statusnya sesuai perkembangan pengiriman. 3. Owner dapat memasukkan nomor resi saat mengubah status menjadi dikirim. 4. Sistem menyimpan perubahan dan mengirimkan notifikasi otomatis kepada pelanggan. |
| Post-kondisi | Status pesanan berhasil diperbarui dan pelanggan menerima notifikasi. |

| Nama Use Case | Kelola Klaim Garansi |
|---|---|
| Aktor | Owner |
| Pre-kondisi | Owner sudah masuk ke panel administrasi dan terdapat klaim garansi yang masuk. |
| Flow of Event | 1. Sistem menampilkan daftar klaim garansi yang masuk. 2. Owner membuka detail klaim dan menelaah kategori masalah, penjelasan, serta foto bukti. 3. Owner memperbarui status klaim dan menambahkan catatan penanganan. 4. Sistem menyimpan perubahan dan mengirimkan notifikasi kepada pelanggan. |
| Post-kondisi | Klaim garansi berhasil ditangani dan pelanggan menerima notifikasi hasil keputusan. |

| Nama Use Case | Kelola Banner |
|---|---|
| Aktor | Owner |
| Pre-kondisi | Owner sudah masuk ke panel administrasi. |
| Flow of Event | 1. Sistem menampilkan daftar banner yang aktif dan nonaktif. 2. Owner dapat menambah banner baru dengan mengisi judul, subjudul, gambar, dan tautan. 3. Owner dapat mengubah urutan tampil atau menonaktifkan banner yang sudah tidak digunakan. 4. Sistem menyimpan perubahan dan menerapkannya pada slideshow halaman utama. |
| Post-kondisi | Banner halaman utama berhasil diperbarui sesuai pengaturan Owner. |

| Nama Use Case | Kelola Kategori |
|---|---|
| Aktor | Owner |
| Pre-kondisi | Owner sudah masuk ke panel administrasi. |
| Flow of Event | 1. Sistem menampilkan daftar kategori produk yang ada. 2. Owner dapat menambahkan kategori baru dengan mengisi nama. 3. Owner dapat mengubah nama atau urutan tampil kategori yang sudah ada. 4. Sistem menyimpan perubahan ke basis data. |
| Post-kondisi | Daftar kategori produk berhasil diperbarui. |

| Nama Use Case | Kelola Kupon |
|---|---|
| Aktor | Owner |
| Pre-kondisi | Owner sudah masuk ke panel administrasi. |
| Flow of Event | 1. Sistem menampilkan daftar voucher yang terdaftar. 2. Owner dapat membuat voucher baru dengan mengisi kode, jenis diskon, nilai diskon, minimum pembelian, dan masa berlaku. 3. Owner dapat mengaktifkan atau menonaktifkan voucher yang ada. 4. Sistem menyimpan perubahan ke basis data. |
| Post-kondisi | Voucher diskon berhasil dibuat dan siap digunakan oleh pelanggan. |

| Nama Use Case | Kelola Merek |
|---|---|
| Aktor | Owner |
| Pre-kondisi | Owner sudah masuk ke panel administrasi. |
| Flow of Event | 1. Sistem menampilkan daftar merek yang terdaftar. 2. Owner dapat menambahkan merek baru dengan mengisi nama dan mengunggah logo. 3. Owner dapat mengubah data merek yang sudah ada. 4. Sistem menyimpan perubahan ke basis data. |
| Post-kondisi | Daftar merek produk berhasil diperbarui. |

| Nama Use Case | Data Pelanggan |
|---|---|
| Aktor | Owner |
| Pre-kondisi | Owner sudah masuk ke panel administrasi. |
| Flow of Event | 1. Sistem menampilkan daftar seluruh akun pelanggan yang terdaftar. 2. Owner dapat melihat data nama, surel, nomor telepon, dan tanggal pendaftaran. 3. Halaman ini hanya menampilkan data dan tidak dapat digunakan untuk mengubah informasi pelanggan. |
| Post-kondisi | Owner mendapatkan informasi mengenai pelanggan yang terdaftar. |

4. Deskripsi Use Case Aktor Admin Toko

Admin Toko adalah staf operasional yang memiliki akses ke fungsi-fungsi pengelolaan harian setelah melakukan proses masuk melalui panel khusus staf.

Tabel 5.24 Deskripsi Use Case Aktor Admin Toko

| Nama Use Case | Kelola Produk |
|---|---|
| Aktor | Admin Toko |
| Pre-kondisi | Admin Toko sudah masuk ke panel pengelolaan melalui halaman login khusus staf. |
| Flow of Event | 1. Sistem menampilkan daftar seluruh produk. 2. Admin Toko dapat menekan tambah produk, mengisi formulir data produk lengkap termasuk stok per ukuran, lalu menyimpan. 3. Admin Toko dapat menekan edit pada produk tertentu untuk memperbarui informasi atau stok, lalu menyimpan. 4. Admin Toko dapat mengaktifkan atau menonaktifkan produk dari katalog. 5. Sistem menyimpan semua perubahan ke basis data. |
| Post-kondisi | Data produk berhasil dikelola dan perubahan tercermin di katalog publik. |

| Nama Use Case | Kelola Pesanan |
|---|---|
| Aktor | Admin Toko |
| Pre-kondisi | Admin Toko sudah masuk ke panel pengelolaan. |
| Flow of Event | 1. Sistem menampilkan daftar pesanan dengan kemampuan penyaringan berdasarkan status. 2. Admin Toko memilih pesanan yang berstatus terbayar dan mengubahnya menjadi sedang diproses. 3. Setelah barang disiapkan dan diserahkan ke ekspedisi, Admin Toko memasukkan nomor resi dan mengubah status menjadi dikirim. 4. Sistem menyimpan perubahan dan mengirimkan notifikasi kepada pelanggan. |
| Post-kondisi | Pesanan berhasil diproses dan pelanggan menerima informasi terkini mengenai pengiriman. |

| Nama Use Case | Kelola Klaim Garansi |
|---|---|
| Aktor | Admin Toko |
| Pre-kondisi | Admin Toko sudah masuk ke panel pengelolaan dan terdapat klaim garansi yang masuk. |
| Flow of Event | 1. Sistem menampilkan daftar klaim garansi yang masuk. 2. Admin Toko membuka detail klaim untuk menelaah masalah dan foto bukti. 3. Admin Toko memperbarui status klaim dan menambahkan catatan penanganan. 4. Sistem menyimpan perubahan dan mengirimkan notifikasi kepada pelanggan. |
| Post-kondisi | Klaim garansi berhasil ditangani dan pelanggan mendapat informasi hasilnya. |

| Nama Use Case | Kelola Kategori |
|---|---|
| Aktor | Admin Toko |
| Pre-kondisi | Admin Toko sudah masuk ke panel pengelolaan. |
| Flow of Event | 1. Sistem menampilkan daftar kategori yang ada. 2. Admin Toko dapat menambahkan kategori baru dengan mengisi nama. 3. Sistem menyimpan perubahan ke basis data. |
| Post-kondisi | Kategori baru berhasil ditambahkan dan dapat digunakan saat penambahan produk. |

| Nama Use Case | Kelola Kupon |
|---|---|
| Aktor | Admin Toko |
| Pre-kondisi | Admin Toko sudah masuk ke panel pengelolaan. |
| Flow of Event | 1. Sistem menampilkan daftar voucher yang terdaftar. 2. Admin Toko dapat membuat voucher baru atau mengubah status voucher yang ada. 3. Sistem menyimpan perubahan ke basis data. |
| Post-kondisi | Voucher berhasil dikelola dan siap digunakan sesuai konfigurasi. |

| Nama Use Case | Kelola Merek |
|---|---|
| Aktor | Admin Toko |
| Pre-kondisi | Admin Toko sudah masuk ke panel pengelolaan. |
| Flow of Event | 1. Sistem menampilkan daftar merek yang terdaftar. 2. Admin Toko dapat menambahkan merek baru atau mengubah data merek yang ada. 3. Sistem menyimpan perubahan ke basis data. |
| Post-kondisi | Daftar merek berhasil diperbarui. |

| Nama Use Case | Data Pelanggan |
|---|---|
| Aktor | Admin Toko |
| Pre-kondisi | Admin Toko sudah masuk ke panel pengelolaan. |
| Flow of Event | 1. Sistem menampilkan daftar pelanggan terdaftar beserta informasi kontak dan tanggal pendaftaran. 2. Admin Toko dapat melihat data pelanggan untuk keperluan verifikasi pesanan atau komunikasi. 3. Halaman ini bersifat hanya tampil. |
| Post-kondisi | Admin Toko mendapatkan informasi yang dibutuhkan mengenai pelanggan. |

---

#### b. Activity Diagram

Activity diagram menggambarkan alur aktivitas dalam suatu proses bisnis dari awal hingga akhir. Diagram ini digunakan untuk memperlihatkan urutan langkah-langkah yang dilakukan oleh aktor dan sistem dalam menyelesaikan sebuah skenario tertentu. Pada platform ZTP Sneakers, activity diagram disusun untuk sebelas proses utama yang mencakup alur konsumen maupun pengelolaan oleh staf.

1. Activity Diagram Pendaftaran

Diagram ini menggambarkan alur proses pendaftaran akun baru oleh pengunjung. Proses dimulai ketika pengunjung mengisi formulir pendaftaran dengan data diri seperti nama, surel, nomor telepon, dan kata sandi. Sistem kemudian memvalidasi seluruh data yang dimasukkan. Apabila terdapat kesalahan seperti kata sandi yang tidak cocok, nomor telepon yang terlalu pendek, atau surel yang sudah terdaftar, sistem menampilkan pesan kesalahan yang sesuai. Jika semua data valid, sistem membuat akun baru, melakukan proses masuk secara otomatis, menggabungkan keranjang sesi tamu ke keranjang akun, dan mengarahkan pengguna ke halaman utama.

(Gambar Activity Diagram Pendaftaran)

2. Activity Diagram Masuk Akun

Diagram ini menggambarkan alur proses masuk ke akun oleh konsumen yang sudah terdaftar. Konsumen memasukkan surel atau nomor telepon sebagai pengenal. Sistem memeriksa apakah pengenal tersebut sudah terdaftar. Jika sudah terdaftar, sistem menampilkan formulir kata sandi untuk diverifikasi. Jika pengenal belum terdaftar, sistem mengalihkan alur ke proses pendaftaran. Setelah kata sandi terverifikasi, sistem membuat sesi masuk, menggabungkan keranjang tamu, dan mengarahkan ke halaman utama.

(Gambar Activity Diagram Masuk Akun)

3. Activity Diagram Melihat Detail Produk dan Menambahkan ke Keranjang

Diagram ini menggambarkan alur ketika pengguna membuka halaman detail produk dan melakukan penambahan ke keranjang belanja. Pengguna dapat menjelajahi galeri foto, memilih ukuran yang diinginkan, dan membaca informasi pada tab deskripsi atau ulasan. Setelah memilih ukuran, pengguna mengklik tombol tambah ke keranjang. Sistem memvalidasi ketersediaan stok dan menyimpan item ke keranjang yang sesuai, baik keranjang sesi untuk tamu maupun keranjang basis data untuk pengguna yang sudah masuk.

(Gambar Activity Diagram Melihat Detail Produk dan Menambahkan ke Keranjang)

4. Activity Diagram Mengelola Wishlist

Diagram ini menggambarkan alur pengelolaan daftar keinginan oleh konsumen. Ketika konsumen mengklik ikon wishlist pada kartu produk, sistem memeriksa apakah pengguna sudah masuk. Jika belum, pengguna diarahkan ke halaman masuk. Jika sudah masuk, sistem memeriksa apakah produk sudah ada di wishlist. Produk yang sudah ada akan dihapus, sementara produk yang belum ada akan ditambahkan. Ikon berubah secara langsung tanpa memuat ulang halaman sebagai konfirmasi tindakan.

(Gambar Activity Diagram Mengelola Wishlist)

5. Activity Diagram Penggunaan Kupon

Diagram ini menggambarkan alur penerapan kode voucher diskon pada halaman checkout. Konsumen memasukkan kode voucher dan mengirimkan permintaan validasi. Sistem memeriksa keberadaan kode, masa berlaku, status aktif, dan apakah nilai belanja memenuhi syarat minimum. Jika semua kondisi terpenuhi, nilai diskon ditampilkan pada ringkasan pembayaran dan disimpan dalam sesi untuk diterapkan saat pesanan dibuat.

(Gambar Activity Diagram Penggunaan Kupon)

6. Activity Diagram Checkout dan Hitung Ongkir

Diagram ini menggambarkan alur proses checkout tiga tahap. Tahap pertama adalah pengisian alamat pengiriman dengan pilihan provinsi dan kota yang berkaitan secara otomatis. Setelah alamat diisi, sistem meminta data ongkos kirim dari layanan RajaOngkir dan menampilkan pilihan ekspedisi beserta tarifnya. Konsumen memilih satu layanan dan total pembayaran diperbarui secara otomatis. Tahap ketiga adalah konfirmasi ringkasan pesanan sebelum melanjutkan ke pembayaran.

(Gambar Activity Diagram Checkout dan Hitung Ongkir)

7. Activity Diagram Pembayaran Midtrans

Diagram ini menggambarkan alur pembayaran melalui Midtrans Snap. Setelah konsumen mengkonfirmasi pesanan, sistem membuat data pesanan dengan status menunggu, lalu meminta token Snap dari Midtrans. Jendela pembayaran Midtrans muncul dan konsumen memilih metode pembayaran yang tersedia. Setelah pembayaran berhasil, Midtrans mengirimkan pemberitahuan webhook ke sistem. Sistem memverifikasi tanda tangan digital dan memperbarui status pesanan menjadi terbayar, lalu mengosongkan keranjang belanja.

(Gambar Activity Diagram Pembayaran Midtrans)

8. Activity Diagram Ajukan Garansi atau Pengembalian

Diagram ini menggambarkan alur pengajuan klaim garansi oleh konsumen. Sistem memvalidasi bahwa pesanan berstatus selesai dan masih dalam periode tujuh hari garansi, serta belum pernah diajukan sebelumnya. Jika semua kondisi terpenuhi, konsumen mengisi formulir dengan memilih kategori masalah, menjelaskan kendala, dan mengunggah foto bukti. Klaim yang berhasil disimpan dan notifikasi dikirimkan kepada konsumen.

(Gambar Activity Diagram Ajukan Garansi atau Pengembalian)

9. Activity Diagram Tulis Ulasan Produk

Diagram ini menggambarkan alur penulisan ulasan produk oleh konsumen setelah pesanan selesai. Sistem memvalidasi bahwa pesanan berstatus selesai dan item belum pernah diulas. Konsumen memilih rating bintang, menulis komentar, dan mengunggah foto secara opsional. Setelah dikirim, ulasan tersimpan dan langsung tampil di halaman detail produk.

(Gambar Activity Diagram Tulis Ulasan Produk)

10. Activity Diagram Kelola Pesanan dan Input Resi

Diagram ini menggambarkan alur pengelolaan pesanan oleh staf. Staf membuka daftar pesanan dan memilih pesanan yang berstatus terbayar untuk diproses. Status diubah menjadi sedang diproses dan notifikasi dikirim ke pelanggan. Setelah barang dikemas dan diserahkan ke ekspedisi, staf memasukkan nomor resi dan mengubah status menjadi dikirim. Notifikasi berisi nomor resi secara otomatis terkirim kepada pelanggan.

(Gambar Activity Diagram Kelola Pesanan dan Input Resi)

11. Activity Diagram Tinjau Laporan Garansi

Diagram ini menggambarkan alur penanganan laporan garansi oleh staf. Staf membuka laporan yang masuk dan menelaah detail masalah beserta foto bukti dari pelanggan. Staf kemudian mengubah status laporan menjadi sedang ditinjau. Setelah analisis selesai, staf membuat keputusan untuk menyetujui dengan catatan resolusi atau menolak dengan alasan yang jelas. Sistem secara otomatis mengirimkan notifikasi kepada pelanggan sesuai keputusan yang diambil.

(Gambar Activity Diagram Tinjau Laporan Garansi)

12. Activity Diagram Ekspor Laporan Penjualan

Diagram ini menggambarkan alur pengunduhan laporan penjualan yang dilakukan oleh pemilik toko. Proses dimulai ketika pemilik toko membuka menu laporan pada panel administrasi. Sistem menampilkan halaman ekspor dengan pilihan filter periode berdasarkan bulan dan tahun. Pemilik toko memilih periode yang diinginkan dan mengklik tombol tampilkan. Sistem mengambil data transaksi dari basis data sesuai periode yang dipilih dan menampilkan pratinjau tabel laporan. Apabila data yang ditampilkan sudah sesuai, pemilik toko mengklik tombol ekspor ke Excel. Sistem memproses data menggunakan pustaka openpyxl, membuat berkas Excel dengan format tabel yang terstruktur berisi nomor pesanan, tanggal, nama pelanggan, detail produk, ekspedisi, total pembayaran, dan status pesanan, kemudian mengunduh berkas tersebut secara otomatis melalui browser.

(Gambar Activity Diagram Ekspor Laporan Penjualan)

---

#### c. Sequence Diagram

Sequence diagram menggambarkan urutan interaksi antara aktor dan komponen-komponen sistem secara kronologis. Diagram ini menunjukkan bagaimana pesan dikirim dan diterima antar objek dalam suatu skenario tertentu dari waktu ke waktu. Pada platform ZTP Sneakers, sequence diagram disusun untuk empat belas skenario utama yang mencakup seluruh alur konsumen dan pengelolaan.

1. Sequence Diagram Registrasi

Menggambarkan urutan interaksi antara pengunjung, antarmuka halaman, dan sistem basis data saat proses pembuatan akun baru. Pengunjung mengirimkan data formulir, sistem memvalidasi dan menyimpan akun baru, lalu mengembalikan respons masuk otomatis kepada pengguna.

(Gambar Sequence Diagram Registrasi)

2. Sequence Diagram Masuk Akun

Menggambarkan urutan verifikasi identitas pengguna. Sistem menerima pengenal, mengambil data pengguna dari basis data, memverifikasi kata sandi, membuat sesi, dan menggabungkan keranjang tamu sebelum mengarahkan ke halaman utama.

(Gambar Sequence Diagram Masuk Akun)

3. Sequence Diagram Lihat Katalog dan Filter Produk

Menggambarkan urutan permintaan data katalog dengan berbagai parameter filter. Setiap perubahan filter dikirim sebagai permintaan parsial menggunakan HTMX, sistem memfilter data dari basis data, dan mengembalikan daftar produk yang diperbarui tanpa memuat ulang halaman.

(Gambar Sequence Diagram Lihat Katalog dan Filter Produk)

4. Sequence Diagram Melihat Detail Produk

Menggambarkan urutan pengambilan data detail produk termasuk galeri foto, varian ukuran, stok per ukuran, dan ulasan yang telah disetujui untuk ditampilkan kepada pengunjung.

(Gambar Sequence Diagram Melihat Detail Produk)

5. Sequence Diagram Tambah ke Keranjang

Menggambarkan urutan proses penambahan item ke keranjang. Sistem memeriksa stok, menentukan jenis keranjang yang digunakan, menyimpan atau memperbarui item, lalu mengirimkan respons pembaruan badge keranjang melalui HTMX.

(Gambar Sequence Diagram Tambah ke Keranjang)

6. Sequence Diagram Kelola Wishlist

Menggambarkan urutan toggle wishlist. Sistem memeriksa autentikasi, mencari entri wishlist yang ada, menghapus jika sudah ada atau menambahkan jika belum, kemudian mengembalikan respons perubahan ikon secara langsung.

(Gambar Sequence Diagram Kelola Wishlist)

7. Sequence Diagram Checkout dan Pembayaran

Menggambarkan urutan interaksi lengkap dalam proses pembelian yang melibatkan sistem, layanan RajaOngkir untuk kalkulasi ongkos kirim, dan layanan Midtrans untuk pemrosesan pembayaran. Sistem membuat data pesanan, meminta token Snap, menerima konfirmasi webhook, dan memperbarui status pesanan.

(Gambar Sequence Diagram Checkout dan Pembayaran)

8. Sequence Diagram Kelola Status Pesanan

Menggambarkan urutan pembaruan status pesanan oleh staf. Staf memilih status baru, sistem memperbarui data di basis data, sinyal Django memicu pembuatan notifikasi, dan notifikasi tersampaikan kepada pelanggan.

(Gambar Sequence Diagram Kelola Status Pesanan)

9. Sequence Diagram Kelola Konfirmasi Pesanan

Menggambarkan urutan konfirmasi penerimaan barang oleh konsumen. Konsumen mengklik tombol konfirmasi, sistem memvalidasi status pesanan, mengubah status menjadi selesai, dan membuka akses ke fitur ulasan serta klaim garansi.

(Gambar Sequence Diagram Kelola Konfirmasi Pesanan)

10. Sequence Diagram Tulis Ulasan Produk

Menggambarkan urutan penyimpanan ulasan. Sistem memvalidasi hak akses ulasan, menyimpan data rating dan komentar beserta foto, lalu memperbarui rata-rata penilaian produk secara otomatis.

(Gambar Sequence Diagram Tulis Ulasan Produk)

11. Sequence Diagram Mengajukan Garansi

Menggambarkan urutan pengajuan klaim garansi. Sistem memvalidasi periode garansi dan status pesanan, menyimpan data klaim, dan memicu pengiriman notifikasi konfirmasi kepada pelanggan melalui sinyal Django.

(Gambar Sequence Diagram Mengajukan Garansi)

12. Sequence Diagram Memproses Pesanan

Menggambarkan urutan pemrosesan pesanan oleh staf dari status terbayar hingga dikirim, termasuk input nomor resi dan pengiriman notifikasi otomatis kepada pelanggan di setiap tahap.

(Gambar Sequence Diagram Memproses Pesanan)

13. Sequence Diagram Kelola Laporan Garansi

Menggambarkan urutan penanganan klaim garansi oleh staf, mulai dari penelaahan laporan, pembaruan status, penulisan catatan resolusi, hingga pengiriman notifikasi keputusan kepada pelanggan.

(Gambar Sequence Diagram Kelola Laporan Garansi)

14. Sequence Diagram Laporan Penjualan Excel

Menggambarkan urutan pembuatan dan pengunduhan laporan penjualan. Pemilik toko memilih periode, sistem mengambil data transaksi dari basis data, memproses data menggunakan openpyxl, dan mengirimkan berkas Excel kepada pengguna untuk diunduh.

(Gambar Sequence Diagram Laporan Penjualan Excel)

---

#### d. Class Diagram

Class diagram merupakan representasi visual dari struktur kelas-kelas yang membentuk sistem perangkat lunak beserta hubungan di antara kelas-kelas tersebut. Diagram ini menggambarkan atribut dan metode yang dimiliki oleh setiap kelas, serta jenis relasi yang menghubungkan satu kelas dengan kelas lainnya seperti asosiasi, agregasi, dan komposisi. Pada platform ZTP Sneakers, class diagram disusun berdasarkan model-model Django yang telah diimplementasikan.

Sistem terdiri dari beberapa kelompok kelas yang saling berelasi. Kelas User menjadi pusat dari hampir seluruh relasi karena hampir semua aktivitas dalam sistem melibatkan identitas pengguna. Kelas ini berelasi satu ke satu dengan UserProfile yang menyimpan data profil tambahan. Kelas Product menjadi kelas inti dalam domain katalog yang berelasi dengan Brand dan Category sebagai penyedia referensi, serta memiliki komposisi dengan ProductImage dan ProductSize untuk menyimpan gambar dan varian ukuran. Kelas Order menjadi kelas inti dalam domain transaksi yang berelasi dengan User, Voucher, OrderItem, dan ShippingAddress. Setiap OrderItem memiliki potensi relasi ke Review dan WarrantyClaim sebagai fitur purna jual. Kelas Cart dan CartItem mengelola data keranjang belanja, sementara Wishlist menjembatani relasi banyak ke banyak antara User dan Product.

(Gambar Class Diagram ZTP Sneakers)

Class diagram di atas menunjukkan bahwa arsitektur kelas pada platform ZTP Sneakers telah dirancang dengan pemisahan tanggung jawab yang jelas antar domain. Setiap kelas hanya menyimpan data yang relevan dengan entitasnya masing-masing, sementara relasi antar kelas diimplementasikan melalui kunci asing yang sesuai dengan hasil normalisasi basis data yang telah dilakukan sebelumnya. Pendekatan ini memastikan bahwa sistem dapat dikembangkan dan dipelihara dengan lebih mudah karena setiap perubahan pada satu kelas tidak akan berdampak berlebihan pada kelas-kelas lainnya.

---

## 5.1.3 Fase Rapid Construction

Fase Rapid Construction merupakan tahap implementasi sistem di mana seluruh rancangan yang telah ditetapkan pada fase User Design diwujudkan menjadi kode program yang berfungsi. Pada fase ini, pengembangan dilakukan secara iteratif dengan mengacu pada daftar kebutuhan yang telah diidentifikasi. Hasil dari fase ini mencakup dua komponen utama, yaitu antarmuka pengguna di sisi depan (frontend) dan logika sistem di sisi belakang beserta antarmuka pengelolaan (backend).

---

### 5.1.3.1 Frontend

Antarmuka platform ZTP Sneakers dibangun menggunakan template HTML yang dikelola oleh Django Template Engine, dipadukan dengan Tailwind CSS untuk tampilan yang responsif di berbagai ukuran layar. Pustaka HTMX digunakan untuk menghadirkan interaktivitas seperti pencarian langsung, pemfilteran katalog, pembaruan keranjang, dan penghitungan ongkos kirim tanpa perlu memuat ulang halaman secara penuh. Berikut ini adalah beberapa halaman yang dibuat pada sisi pengguna:

a. Halaman Beranda

Merupakan halaman utama yang pertama kali dilihat pengguna saat mengakses platform ZTP Sneakers. Halaman ini berfungsi sebagai pintu gerbang yang merepresentasikan identitas toko, menampilkan promosi unggulan, produk-produk terpilih, serta berbagai keunggulan layanan toko. Halaman beranda memiliki beberapa elemen antara lain:

1. Navbar

   Merupakan bilah navigasi yang tersedia di seluruh halaman dan menampilkan logo toko, kolom pencarian langsung, ikon keranjang belanja dengan badge jumlah item, ikon notifikasi, serta menu kategori produk.

2. Hero Carousel

   Merupakan slideshow banner promosi yang tampil secara otomatis setiap lima detik. Setiap banner dapat dikonfigurasi dengan gambar, judul, subjudul, dan tautan tujuan oleh pengelola toko.

3. Trust Badge Strip

   Merupakan baris ikon kepercayaan yang menampilkan keunggulan layanan toko seperti garansi produk, kebijakan pengembalian tujuh hari, keaslian produk, dan kelengkapan koleksi.

4. Seksi Produk

   Menampilkan beberapa kelompok produk yang dibagi berdasarkan kategori seperti produk terlaris, produk baru, dan produk dengan penilaian tertinggi dalam format grid yang dapat digulir.

5. Footer

   Menampilkan informasi kontak toko, tautan navigasi cepat, serta ikon-ikon metode pembayaran dan layanan ekspedisi yang tersedia.

(Gambar Halaman Beranda)

---

b. Halaman Katalog Produk

Merupakan halaman yang menampilkan seluruh produk aktif yang tersedia di toko dalam format grid. Halaman ini dilengkapi dengan berbagai alat penyaringan dan pengurutan untuk membantu pelanggan menemukan produk yang sesuai dengan kebutuhannya. Halaman katalog memiliki beberapa elemen antara lain:

1. Filter Sidebar

   Menampilkan pilihan penyaringan produk berdasarkan merek, kategori, ukuran, warna, dan kondisi barang. Seluruh filter bekerja secara langsung tanpa memuat ulang halaman.

2. Sortir Produk

   Memungkinkan pelanggan mengurutkan tampilan produk berdasarkan produk terbaru, terlaris, harga terendah, atau harga tertinggi.

3. Grid Produk

   Menampilkan kartu produk dalam susunan empat kolom pada layar desktop dan dua kolom pada perangkat bergerak. Setiap kartu memuat foto produk, nama, kondisi, harga, dan ikon daftar keinginan.

(Gambar Halaman Katalog)

---

c. Halaman Detail Produk

Merupakan halaman yang menampilkan informasi lengkap sebuah produk. Pelanggan dapat melihat galeri foto, memilih ukuran yang tersedia, dan membaca ulasan dari pembeli sebelumnya sebelum memutuskan untuk membeli. Halaman detail produk memiliki beberapa elemen antara lain:

1. Galeri Foto

   Menampilkan foto utama produk berukuran besar dengan baris gambar miniatur di bawahnya. Pelanggan dapat mengklik miniatur untuk menampilkan foto yang berbeda.

2. Informasi Produk

   Menampilkan nama produk, merek, kondisi barang, harga jual, harga coret jika ada, pilihan ukuran dengan keterangan stok per ukuran, serta tombol tambah ke keranjang dan simpan ke daftar keinginan.

3. Tab Informasi

   Menyediakan tiga tab yang dapat dipilih: deskripsi produk, ulasan dari pelanggan yang telah membeli, dan informasi kebijakan garansi serta pengembalian barang.

4. Produk Terkait

   Menampilkan empat produk lain dari merek yang sama sebagai rekomendasi tambahan di bagian bawah halaman.

(Gambar Halaman Detail Produk)

---

d. Halaman Autentikasi

Merupakan halaman masuk dan pendaftaran akun yang digabungkan dalam satu tampilan. Halaman ini menggunakan desain dua sisi di mana formulir ditampilkan di satu sisi layar. Pengguna baru diarahkan ke formulir pendaftaran apabila alamat surel atau nomor telepon yang dimasukkan belum terdaftar, dan diarahkan ke formulir kata sandi apabila sudah terdaftar. Tersedia juga pilihan masuk menggunakan akun Google.

(Gambar Halaman Autentikasi)

---

e. Halaman Keranjang Belanja

Merupakan halaman yang menampilkan seluruh produk yang telah ditambahkan oleh pelanggan sebelum melakukan pembelian. Pelanggan dapat mengubah jumlah item atau menghapus item langsung dari halaman ini tanpa memuat ulang halaman. Ringkasan total belanja ditampilkan di bagian bawah beserta tombol untuk melanjutkan ke proses checkout.

(Gambar Halaman Keranjang Belanja)

---

f. Halaman Checkout

Merupakan halaman proses pembelian yang terdiri dari tiga tahap dalam satu halaman. Tahap pertama adalah pengisian alamat pengiriman dengan dropdown provinsi dan kota yang saling berkaitan. Tahap kedua adalah pemilihan layanan ekspedisi di mana sistem secara otomatis menghitung ongkos kirim untuk beberapa pilihan ekspedisi. Tahap ketiga adalah konfirmasi pembayaran di mana pelanggan dapat memasukkan kode voucher dan menyelesaikan pembayaran melalui jendela Midtrans Snap.

(Gambar Halaman Checkout)

---

g. Halaman Riwayat Pesanan

Merupakan halaman yang menampilkan seluruh pesanan yang pernah dibuat oleh pelanggan beserta status terkininya. Setiap entri pesanan menampilkan nomor pesanan, tanggal, total pembayaran, dan status dalam bentuk lencana berwarna. Pelanggan dapat mengklik pesanan untuk melihat detail lengkapnya.

(Gambar Halaman Riwayat Pesanan)

---

h. Halaman Detail Pesanan

Merupakan halaman yang menampilkan rincian lengkap satu pesanan. Terdapat linimasa status pesanan yang menunjukkan perkembangan dari pembayaran hingga penerimaan barang, informasi alamat dan ekspedisi, daftar item yang dibeli, serta ringkasan biaya. Pelanggan dapat mengonfirmasi penerimaan barang, menulis ulasan, atau mengajukan klaim garansi dari halaman ini.

(Gambar Halaman Detail Pesanan)

---

i. Halaman Daftar Keinginan

Merupakan halaman yang menampilkan seluruh produk yang disimpan oleh pelanggan ke dalam daftar keinginan. Pelanggan dapat menghapus produk dari daftar atau langsung menambahkannya ke keranjang belanja. Sistem akan memberikan pemberitahuan apabila stok produk yang disimpan tersisa sangat sedikit.

(Gambar Halaman Daftar Keinginan)

---

j. Halaman Profil Akun

Merupakan halaman pengelolaan akun pelanggan. Pelanggan dapat memperbarui nama tampil, nomor telepon, alamat, dan foto profil. Halaman ini juga menyediakan akses cepat ke riwayat pesanan terbaru.

(Gambar Halaman Profil Akun)

---

### 5.1.3.2 Backend (UI)

Antarmuka sisi pengelolaan pada platform ZTP Sneakers dibangun menggunakan kerangka kerja Django dengan panel administrasi yang dikustomisasi menggunakan tema Jazzmin untuk tampilan yang lebih modern dan terstruktur. Seluruh logika pengelolaan data, pemrosesan pesanan, dan komunikasi dengan layanan eksternal diimplementasikan pada lapisan ini. Berikut ini adalah beberapa halaman yang dibuat pada sisi pengelolaan:

a. Halaman Dasbor Admin Toko

Merupakan halaman utama yang pertama kali ditampilkan setelah staf berhasil masuk ke panel pengelolaan. Halaman ini menyajikan ringkasan aktivitas operasional toko secara terpusat sehingga staf dapat langsung mengetahui kondisi terkini tanpa perlu membuka halaman lain. Halaman dasbor memiliki beberapa elemen antara lain:

1. Kartu Indikator Harian

   Menampilkan empat angka ringkasan: total pesanan masuk hari ini, jumlah pesanan yang menunggu pembayaran, jumlah pesanan yang sudah terbayar dan perlu diproses, serta jumlah klaim garansi baru yang belum ditangani.

2. Daftar Stok Menipis

   Menampilkan daftar varian produk yang stoknya tersisa dua unit atau kurang agar staf dapat segera mengambil tindakan pengisian stok.

(Gambar Halaman Dasbor Admin Toko)

---

b. Halaman Manajemen Produk

Merupakan halaman yang digunakan staf untuk mengelola seluruh data produk yang terdaftar dalam sistem. Staf dapat melihat daftar produk, menambahkan produk baru, mengubah data produk yang sudah ada, serta mengaktifkan atau menonaktifkan produk dari katalog publik. Halaman ini memiliki beberapa elemen antara lain:

1. Tabel Produk

   Menampilkan seluruh produk beserta informasi ringkas seperti foto, nama, merek, harga, total stok, dan status tampil. Dilengkapi dengan tombol aksi untuk mengubah data atau mengubah status produk.

2. Formulir Tambah dan Ubah Produk

   Menyediakan formulir lengkap untuk mengisi nama, merek, kategori, kondisi, warna, harga, deskripsi, serta stok untuk setiap ukuran yang tersedia. Baris ukuran dapat ditambah atau dihapus secara dinamis.

(Gambar Halaman Manajemen Produk)

---

c. Halaman Manajemen Pesanan

Merupakan halaman yang digunakan staf untuk memantau dan memproses seluruh pesanan yang masuk. Staf dapat menyaring pesanan berdasarkan status, mengubah status pesanan sesuai perkembangan pengiriman, serta memasukkan nomor resi ekspedisi. Setiap perubahan status secara otomatis mengirimkan notifikasi kepada pelanggan yang bersangkutan.

(Gambar Halaman Manajemen Pesanan)

---

d. Halaman Klaim Garansi

Merupakan halaman yang menampilkan seluruh pengajuan klaim garansi dari pelanggan. Staf dapat melihat detail setiap klaim termasuk kategori masalah, penjelasan pelanggan, dan foto bukti yang dilampirkan. Staf kemudian dapat memperbarui status klaim dan menambahkan catatan resolusi yang akan tersampaikan kepada pelanggan melalui notifikasi.

(Gambar Halaman Klaim Garansi)

---

e. Halaman Moderasi Ulasan

Merupakan halaman yang memungkinkan staf untuk memantau seluruh ulasan yang diberikan pelanggan terhadap produk-produk di toko. Staf dapat mengatur visibilitas ulasan dengan menyembunyikan ulasan yang dianggap tidak sesuai atau melanggar ketentuan toko.

(Gambar Halaman Moderasi Ulasan)

---

f. Halaman Data Pelanggan

Merupakan halaman yang menampilkan daftar seluruh akun pelanggan yang terdaftar dalam sistem. Informasi yang ditampilkan mencakup nama, alamat surel, nomor telepon, dan tanggal pendaftaran. Halaman ini bersifat hanya tampil dan tidak dapat digunakan untuk mengubah data pelanggan.

(Gambar Halaman Data Pelanggan)

---

g. Halaman Dasbor Analitik Pemilik

Merupakan halaman khusus untuk pemilik toko yang menampilkan gambaran menyeluruh mengenai performa bisnis toko secara visual. Halaman ini diakses melalui panel Django Admin dengan antarmuka Jazzmin yang telah dikustomisasi. Halaman dasbor analitik memiliki beberapa elemen antara lain:

1. Kartu Indikator Kinerja Utama

   Menampilkan empat indikator utama: total pendapatan bulan berjalan, total pesanan keseluruhan, jumlah pelanggan baru bulan ini, dan produk yang paling banyak terjual.

2. Grafik Penjualan

   Menampilkan grafik batang yang menggambarkan perkembangan penjualan dalam empat minggu terakhir dalam satuan juta rupiah.

3. Tabel Transaksi Terbaru

   Menampilkan sepuluh transaksi terbaru beserta informasi pelanggan, tanggal, total, dan status pesanan.

(Gambar Halaman Dasbor Analitik Pemilik)

---

h. Halaman Ekspor Laporan

Merupakan halaman yang memungkinkan pemilik toko untuk mengunduh laporan penjualan dalam format berkas Excel. Pemilik dapat memilih periode laporan berdasarkan bulan dan tahun yang diinginkan. Berkas yang dihasilkan memuat data seluruh transaksi pada periode tersebut dalam format tabel yang terstruktur dan siap digunakan untuk keperluan analisis lebih lanjut.

(Gambar Halaman Ekspor Laporan)

---

## 5.1.4 Fase Cutover

Fase Cutover merupakan tahap akhir dalam metodologi RAD yang mencakup proses pengujian sistem secara menyeluruh dan penerapan sistem ke lingkungan produksi. Pada fase ini, sistem yang telah dibangun dievaluasi kesesuaiannya dengan kebutuhan yang telah diidentifikasi sebelum diserahkan untuk digunakan secara nyata.

---

### 5.1.4.1 Hosting

Penerapan platform ZTP Sneakers dilakukan pada layanan shared hosting yang menggunakan panel kontrol cPanel. Proses penerapan memanfaatkan antarmuka Passenger WSGI yang tersedia pada cPanel untuk menghubungkan server web dengan aplikasi Django. Berkas statis seperti CSS, JavaScript, dan gambar dilayani menggunakan pustaka WhiteNoise yang terintegrasi langsung sebagai middleware Django sehingga tidak memerlukan konfigurasi server web terpisah.

Basis data PostgreSQL dikonfigurasi melalui panel cPanel dengan menggunakan variabel lingkungan yang disimpan dalam berkas .env untuk menjaga kerahasiaan kredensial. Seluruh berkas media yang diunggah pengguna, seperti foto produk, foto ulasan, dan foto bukti klaim garansi, disimpan pada direktori media yang dapat diakses melalui URL publik sesuai konfigurasi MEDIA_ROOT dan MEDIA_URL pada pengaturan Django.

Sebelum penerapan ke lingkungan produksi, perintah collectstatic dijalankan untuk mengumpulkan seluruh berkas statis ke direktori staticfiles yang kemudian dilayani oleh WhiteNoise. Variabel DEBUG ditetapkan bernilai False pada lingkungan produksi untuk menonaktifkan halaman debug dan memastikan penanganan kesalahan yang aman bagi pengguna akhir.

---

### 5.1.4.2 Pengujian Black Box

Blackbox testing merupakan pengujian yang dilakukan terhadap fungsional atau kegunaan dari sebuah aplikasi yang sedang dikembangkan. Pengujian ini hanya memeriksa apakah input yang diberikan menghasilkan output yang sesuai. Blackbox testing digunakan untuk mengetahui apakah setiap fitur pada platform B2C ZTP Sneakers sudah berjalan sebagaimana mestinya dari sudut pandang pengguna akhir.

a. Pengujian Pendaftaran Akun

Pengujian dilakukan untuk memastikan bahwa fitur pendaftaran akun baru berjalan sesuai dengan kebutuhan sistem, yaitu hanya memperbolehkan data yang valid untuk mendaftarkan akun baru, menolak surel atau nomor telepon yang sudah terdaftar, dan memvalidasi format data yang dimasukkan. Pengujian pendaftaran akun dapat dilihat pada tabel berikut.

Tabel 5.25 Pengujian Pendaftaran Akun

| No | Skenario Uji | Input | Output yang Diharapkan | Keterangan |
|---|---|---|---|---|
| 1 | Pendaftaran berhasil dengan data valid | Nama: Wahyu, Email: wahyu@gmail.com, No. HP: 08123456789, Password: Test1234, Konfirmasi: Test1234 | Akun berhasil dibuat, sistem melakukan masuk otomatis, pengguna diarahkan ke halaman beranda | Lulus |
| 2 | Pendaftaran dengan email yang sudah terdaftar | Email yang sudah ada di sistem | Sistem menampilkan pesan: Email/No HP sudah terdaftar, formulir tidak diproses | Lulus |
| 3 | Pendaftaran dengan nomor telepon yang sudah terdaftar | No. HP yang sudah ada di sistem | Sistem menampilkan pesan: Email/No HP sudah terdaftar, formulir tidak diproses | Lulus |
| 4 | Pendaftaran dengan kata sandi yang tidak cocok | Password: Test1234, Konfirmasi: Test5678 | Sistem menampilkan pesan: Password tidak cocok, formulir tidak diproses | Lulus |
| 5 | Pendaftaran dengan nomor telepon kurang dari 10 digit | No. HP: 0812 | Sistem menampilkan pesan: Nomor HP harus minimal 10 digit | Lulus |
| 6 | Pendaftaran dengan email dan nomor telepon kosong | Email dan No. HP dikosongkan | Sistem menampilkan pesan: Email dan Nomor HP wajib diisi | Lulus |

b. Pengujian Login dan Logout

Pengujian dilakukan untuk memastikan bahwa fitur masuk dan keluar akun berjalan sesuai dengan kebutuhan sistem, yaitu hanya memperbolehkan pengguna yang terdaftar untuk masuk ke dalam sistem menggunakan kredensial yang benar. Pengujian login dan logout dapat dilihat pada tabel berikut.

Tabel 5.26 Pengujian Login dan Logout

| No | Skenario Uji | Input | Output yang Diharapkan | Keterangan |
|---|---|---|---|---|
| 1 | Login berhasil menggunakan email | Email: wahyu@gmail.com, Password: Test1234 | Pengguna berhasil masuk dan diarahkan ke halaman beranda | Lulus |
| 2 | Login berhasil menggunakan nomor telepon | No. HP: 08123456789, Password: Test1234 | Pengguna berhasil masuk dan diarahkan ke halaman beranda | Lulus |
| 3 | Login dengan kata sandi yang salah | Email valid, Password: salah | Sistem menampilkan pesan: Password salah, pengguna tetap di halaman masuk | Lulus |
| 4 | Login dengan email yang tidak terdaftar | Email: tidakterdaftar@gmail.com | Sistem mengarahkan ke formulir pendaftaran karena pengenal tidak ditemukan | Lulus |
| 5 | Login menggunakan Google OAuth | Klik tombol masuk dengan Google, pilih akun Google yang valid | Pengguna berhasil masuk menggunakan akun Google dan diarahkan ke beranda | Lulus |
| 6 | Logout dari akun | Klik tombol keluar pada navbar | Sesi pengguna dihapus, pengguna diarahkan ke halaman beranda dalam kondisi tidak masuk | Lulus |
| 7 | Akses halaman yang membutuhkan autentikasi tanpa masuk | Kunjungi URL /pesanan/checkout/ tanpa masuk akun | Sistem mengarahkan ke halaman masuk akun | Lulus |

c. Pengujian Katalog dan Pencarian Produk

Pengujian dilakukan untuk memastikan bahwa fitur katalog, pencarian, dan filter produk berfungsi dengan benar dan menampilkan hasil yang sesuai dengan kriteria yang dipilih. Pengujian katalog dan pencarian produk dapat dilihat pada tabel berikut.

Tabel 5.27 Pengujian Katalog dan Pencarian Produk

| No | Skenario Uji | Input | Output yang Diharapkan | Keterangan |
|---|---|---|---|---|
| 1 | Pencarian produk dengan kata kunci yang sesuai | Kata kunci: "Nike" | Daftar produk mengandung kata Nike muncul tanpa memuat ulang halaman | Lulus |
| 2 | Pencarian produk dengan kata kunci yang tidak ada | Kata kunci: "xyzabc" | Halaman menampilkan grid kosong atau keterangan produk tidak ditemukan | Lulus |
| 3 | Filter katalog berdasarkan merek | Pilih merek Nike | Hanya produk dengan merek Nike yang ditampilkan | Lulus |
| 4 | Filter katalog berdasarkan ukuran | Pilih ukuran 40 | Hanya produk yang memiliki varian ukuran 40 yang ditampilkan | Lulus |
| 5 | Filter katalog berdasarkan kondisi | Pilih kondisi: Second | Hanya produk second yang ditampilkan | Lulus |
| 6 | Sortir produk berdasarkan harga terendah | Pilih urutan: Harga Terendah | Produk ditampilkan dari harga paling murah ke paling mahal | Lulus |
| 7 | Reset semua filter | Klik tombol reset filter | Semua filter dihapus dan seluruh produk aktif kembali ditampilkan | Lulus |

d. Pengujian Keranjang Belanja

Pengujian dilakukan untuk memastikan bahwa fitur keranjang belanja berfungsi dengan benar, termasuk penambahan item, perubahan jumlah, penghapusan item, dan penggabungan keranjang tamu saat pengguna masuk akun. Pengujian keranjang belanja dapat dilihat pada tabel berikut.

Tabel 5.28 Pengujian Keranjang Belanja

| No | Skenario Uji | Input | Output yang Diharapkan | Keterangan |
|---|---|---|---|---|
| 1 | Tambah produk ke keranjang dengan ukuran valid | Pilih ukuran 40, klik Tambah ke Keranjang | Produk masuk ke keranjang, notifikasi sukses muncul, badge keranjang diperbarui | Lulus |
| 2 | Tambah produk ke keranjang tanpa memilih ukuran | Klik Tambah ke Keranjang tanpa memilih ukuran | Sistem menampilkan pesan: Pilih ukuran terlebih dahulu | Lulus |
| 3 | Tambah produk dengan stok nol | Pilih ukuran yang stoknya sudah habis | Tombol ukuran tidak dapat dipilih atau sistem menampilkan pesan stok habis | Lulus |
| 4 | Ubah jumlah item di keranjang | Klik tombol tambah pada item di keranjang | Jumlah item bertambah satu, total harga diperbarui otomatis | Lulus |
| 5 | Hapus item dari keranjang | Klik tombol hapus pada item di keranjang | Item terhapus dari keranjang, total harga diperbarui | Lulus |
| 6 | Penggabungan keranjang tamu saat masuk akun | Pengunjung menambah produk ke keranjang, kemudian masuk akun | Item keranjang sesi tamu tergabung ke keranjang akun tanpa kehilangan data | Lulus |

e. Pengujian Checkout dan Pembayaran

Pengujian dilakukan untuk memastikan bahwa alur checkout berjalan dengan benar mulai dari pengisian alamat, kalkulasi ongkos kirim otomatis, penggunaan voucher, hingga proses pembayaran melalui Midtrans. Pengujian checkout dan pembayaran dapat dilihat pada tabel berikut.

Tabel 5.29 Pengujian Checkout dan Pembayaran

| No | Skenario Uji | Input | Output yang Diharapkan | Keterangan |
|---|---|---|---|---|
| 1 | Checkout dengan alamat lengkap dan pilih ekspedisi | Isi nama, telepon, provinsi, kota, kecamatan, alamat lengkap, pilih JNE REG | Daftar layanan ekspedisi muncul, total diperbarui otomatis setelah memilih | Lulus |
| 2 | Checkout tanpa memilih layanan pengiriman | Klik lanjut ke pembayaran tanpa memilih ongkir | Formulir tidak dapat dilanjutkan, sistem menampilkan peringatan untuk memilih ekspedisi | Lulus |
| 3 | Penggunaan kode voucher yang valid | Masukkan kode voucher aktif dengan total belanja memenuhi syarat minimum | Nilai diskon ditampilkan pada ringkasan, total dikurangi sesuai nilai diskon | Lulus |
| 4 | Penggunaan kode voucher yang sudah kedaluwarsa | Masukkan kode voucher yang masa berlakunya sudah habis | Sistem menampilkan pesan: Voucher tidak valid atau sudah tidak berlaku | Lulus |
| 5 | Penggunaan kode voucher dengan total belanja di bawah minimum | Masukkan kode voucher yang memiliki syarat minimum lebih tinggi dari total belanja | Sistem menampilkan pesan: Total belanja tidak memenuhi syarat minimum voucher | Lulus |
| 6 | Konfirmasi pembayaran otomatis melalui webhook Midtrans | Simulasi notifikasi pembayaran berhasil dari Midtrans | Status pesanan berubah dari menunggu menjadi terbayar, notifikasi dikirim ke pelanggan | Lulus |

f. Pengujian Manajemen Pesanan

Pengujian dilakukan untuk memastikan bahwa staf dapat mengelola pesanan dengan benar, mulai dari pemrosesan pesanan yang masuk, input nomor resi, hingga konfirmasi penerimaan oleh pelanggan. Pengujian manajemen pesanan dapat dilihat pada tabel berikut.

Tabel 5.30 Pengujian Manajemen Pesanan

| No | Skenario Uji | Input | Output yang Diharapkan | Keterangan |
|---|---|---|---|---|
| 1 | Perbarui status pesanan dari terbayar ke diproses | Staf memilih status: Diproses dan menyimpan | Status pesanan diperbarui, notifikasi dalam aplikasi dikirim ke pelanggan | Lulus |
| 2 | Input nomor resi dan ubah status ke dikirim | Staf memasukkan nomor resi: JNE123456, pilih status: Dikirim | Nomor resi tersimpan, status berubah menjadi dikirim, notifikasi dikirim ke pelanggan | Lulus |
| 3 | Konfirmasi penerimaan barang oleh pelanggan | Pelanggan mengklik tombol Pesanan Sudah Diterima | Status pesanan berubah menjadi selesai, tombol tulis ulasan dan laporan garansi muncul | Lulus |
| 4 | Cek status pembayaran manual oleh pelanggan | Pelanggan mengklik Cek Status Pembayaran pada pesanan pending | Sistem mengecek status ke Midtrans dan memperbarui status pesanan jika sudah terbayar | Lulus |
| 5 | Filter daftar pesanan berdasarkan status | Pilih tab: Menunggu Pembayaran di panel admin | Hanya pesanan dengan status menunggu pembayaran yang ditampilkan | Lulus |

g. Pengujian Ulasan dan Garansi

Pengujian dilakukan untuk memastikan bahwa fitur ulasan produk dan klaim garansi berjalan sesuai dengan aturan bisnis yang telah ditetapkan, termasuk pembatasan akses berdasarkan status pesanan dan periode waktu. Pengujian ulasan dan garansi dapat dilihat pada tabel berikut.

Tabel 5.31 Pengujian Ulasan dan Garansi

| No | Skenario Uji | Input | Output yang Diharapkan | Keterangan |
|---|---|---|---|---|
| 1 | Tulis ulasan setelah pesanan selesai | Rating: 5 bintang, komentar, 2 foto bukti | Ulasan tersimpan dan tampil di halaman detail produk, rata-rata rating diperbarui | Lulus |
| 2 | Tulis ulasan kedua untuk item yang sama | Mencoba mengulas item yang sudah pernah diulas | Sistem menampilkan informasi bahwa ulasan sudah pernah diberikan untuk item ini | Lulus |
| 3 | Tulis ulasan untuk pesanan yang belum selesai | Akses formulir ulasan pada pesanan berstatus dikirim | Sistem menolak akses dan menampilkan pesan bahwa ulasan hanya untuk pesanan selesai | Lulus |
| 4 | Ajukan klaim garansi dalam batas waktu 7 hari | Isi formulir garansi dalam 7 hari sejak pesanan selesai | Klaim tersimpan dengan status menunggu, notifikasi konfirmasi dikirim ke pelanggan | Lulus |
| 5 | Ajukan klaim garansi setelah melewati batas waktu | Akses formulir garansi setelah 7 hari sejak pesanan selesai | Sistem menampilkan pesan: Batas waktu klaim garansi telah berakhir | Lulus |
| 6 | Perbarui status klaim garansi oleh staf | Staf mengubah status ke Disetujui dan mengisi catatan resolusi | Status klaim diperbarui, notifikasi dikirim ke pelanggan, catatan tersimpan | Lulus |
| 7 | Moderasi ulasan oleh staf | Staf mengklik Sembunyikan pada ulasan yang tidak pantas | Ulasan tidak lagi tampil di halaman detail produk | Lulus |

h. Pengujian Ekspor Laporan Penjualan

Pengujian dilakukan untuk memastikan bahwa fitur ekspor laporan penjualan menghasilkan berkas Excel yang sesuai dengan data transaksi pada periode yang dipilih. Pengujian ekspor laporan penjualan dapat dilihat pada tabel berikut.

Tabel 5.32 Pengujian Ekspor Laporan Penjualan

| No | Skenario Uji | Input | Output yang Diharapkan | Keterangan |
|---|---|---|---|---|
| 1 | Ekspor laporan dengan filter bulan dan tahun yang valid | Pilih bulan: Juni, Tahun: 2026, klik Ekspor | Berkas Excel terunduh berisi data transaksi bulan Juni 2026 sesuai filter | Lulus |
| 2 | Ekspor laporan pada periode yang tidak memiliki transaksi | Pilih bulan dan tahun yang tidak ada transaksinya | Berkas Excel terunduh dengan tabel kosong atau hanya header kolom | Lulus |
| 3 | Akses halaman ekspor tanpa otentikasi staf | Kunjungi URL ekspor tanpa masuk sebagai staf | Sistem mengarahkan ke halaman masuk atau menampilkan pesan akses ditolak | Lulus |

---

## 5.2 Demonstrasi

Demonstrasi sistem merupakan tahap pemaparan hasil pengembangan platform ZTP Sneakers kepada pemangku kepentingan untuk memastikan bahwa seluruh fitur yang dibangun telah sesuai dengan kebutuhan yang diidentifikasi pada fase Requirements Planning. Demonstrasi dilaksanakan dengan menjalankan sistem secara langsung dan menelusuri alur penggunaan dari perspektif setiap peran pengguna.

Demonstrasi dimulai dari sisi konsumen dengan menampilkan halaman beranda yang memuat slideshow banner, produk terlaris, dan produk baru. Proses penelusuran katalog ditunjukkan dengan menggunakan fitur pencarian langsung dan pemfilteran berdasarkan merek serta ukuran. Selanjutnya ditampilkan alur pembelian lengkap mulai dari pemilihan produk, penambahan ke keranjang, pengisian alamat pengiriman, pemilihan layanan ekspedisi dengan penghitungan ongkos kirim otomatis, hingga pembayaran melalui jendela Midtrans Snap. Setelah pesanan berhasil dibuat, ditampilkan pula tampilan riwayat pesanan dengan linimasa status, formulir ulasan produk, dan formulir pengajuan klaim garansi.

Demonstrasi dilanjutkan dari sisi staf pengelola dengan menampilkan dasbor ringkasan operasional yang mencakup indikator pesanan harian dan stok menipis. Proses pengelolaan pesanan ditunjukkan dengan memperbarui status pesanan dari terbayar menjadi diproses dan kemudian menjadi dikirim dengan menyertakan nomor resi. Penanganan klaim garansi didemonstrasikan dengan menelusuri laporan yang masuk, menelaah foto bukti, memperbarui status, dan menambahkan catatan resolusi. Moderasi ulasan produk juga ditampilkan untuk menunjukkan kemampuan staf dalam mengatur visibilitas ulasan.

Demonstrasi pada sisi pemilik toko difokuskan pada dasbor analitik yang menampilkan grafik penjualan empat minggu terakhir, peta panas pesanan berdasarkan hari dan jam, serta tabel transaksi terbaru. Fitur ekspor laporan penjualan ditunjukkan dengan memilih periode bulan dan tahun tertentu kemudian mengunduh berkas Excel yang dihasilkan.

Hasil demonstrasi secara keseluruhan menunjukkan bahwa platform ZTP Sneakers telah berhasil mengimplementasikan seluruh kebutuhan fungsional yang telah ditetapkan, dengan antarmuka yang responsif dan alur transaksi yang terdigitalisasi secara menyeluruh sesuai dengan tujuan awal pengembangan.

---

*Dokumen ini disusun sebagai bagian dari laporan skripsi pengembangan platform e-commerce B2C ZTP Sneakers.*

---

# BAB 6
# PENUTUP

## 6.1 Kesimpulan


---

*Dokumen BAB 5 dan BAB 6 disusun sebagai bagian dari laporan skripsi pengembangan platform e-commerce B2C ZTP Sneakers.*
