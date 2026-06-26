# Normalisasi Database — ZTP Sneakers B2C

> **Versi:** 1.0
> **Tanggal:** 2026
> **Author:** Wahyu Ahmad Cahyadi (221103805)
> **Deskripsi:** Normalisasi database dari UNF hingga 3NF untuk semua entitas pada platform ZTP Sneakers B2C

---

## Daftar Isi

1. [UNF — Unnormalized Form](#1-unf--unnormalized-form)
2. [1NF — First Normal Form](#2-1nf--first-normal-form)
3. [2NF — Second Normal Form](#3-2nf--second-normal-form)
4. [3NF — Third Normal Form](#4-3nf--third-normal-form)

---

## 1. UNF — Unnormalized Form

Semua field dari seluruh entitas digabungkan menjadi satu tabel besar tanpa pemisahan.

### tb_ztpsneakers (UNF)

| Field |
|---|
| id_user |
| username |
| email |
| password |
| last_login |
| is_superuser |
| is_active |
| is_staff |
| date_joined |
| full_name |
| phone_number |
| address_line1 |
| address_line2 |
| city |
| avatar |
| role |
| id_userprofile |
| userprofile_created_at |
| userprofile_updated_at |
| id_notification |
| notification_title |
| notification_message |
| notification_link |
| notification_is_read |
| notification_created_at |
| id_category |
| category_name |
| category_slug |
| category_icon |
| category_order |
| id_brand |
| brand_name |
| brand_slug |
| brand_logo |
| id_product |
| product_name |
| product_color |
| product_color_secondary |
| product_slug |
| product_description |
| product_condition |
| product_price |
| product_crossed_price |
| product_is_active |
| product_is_featured |
| product_created_at |
| id_product_image |
| product_image_file |
| product_image_is_primary |
| product_image_order |
| id_product_size |
| product_size |
| product_size_stock |
| id_banner |
| banner_title |
| banner_subtitle |
| banner_image |
| banner_link |
| banner_order |
| banner_is_active |
| id_review |
| review_rating |
| review_comment |
| review_image1 |
| review_image2 |
| review_image3 |
| review_is_visible |
| review_created_at |
| id_voucher |
| voucher_code |
| voucher_discount_type |
| voucher_discount_value |
| voucher_min_purchase |
| voucher_valid_from |
| voucher_valid_to |
| voucher_is_active |
| id_wishlist |
| wishlist_created_at |
| id_cart |
| cart_session_key |
| cart_created_at |
| cart_updated_at |
| id_cart_item |
| cart_item_quantity |
| id_order |
| order_number |
| order_status |
| order_midtrans_transaction_id |
| order_courier |
| order_shipping_service |
| order_shipping_cost |
| order_tracking_number |
| order_discount_amount |
| order_subtotal |
| order_total |
| order_created_at |
| order_updated_at |
| id_order_item |
| order_item_size_str |
| order_item_product_name |
| order_item_price |
| order_item_quantity |
| id_shipping_address |
| shipping_recipient_name |
| shipping_phone_number |
| shipping_province_id |
| shipping_province_name |
| shipping_city_id |
| shipping_city_name |
| shipping_district_name |
| shipping_postal_code |
| shipping_full_address |
| id_warranty_claim |
| warranty_kategori |
| warranty_reason |
| warranty_evidence_image |
| warranty_status |
| warranty_admin_notes |
| warranty_created_at |
| warranty_updated_at |
| id_footer_icon |
| footer_icon_title |
| footer_icon_image |
| footer_icon_order |

---

## 2. 1NF — First Normal Form

Setiap entitas dipisahkan ke tabel masing-masing. Setiap field bersifat atomik (satu nilai per sel), tidak ada grup berulang, dan baris sudah terurut berdasarkan identifikasi unik masing-masing entitas.

### tb_user

| Field |
|---|
| id_user |
| username |
| email |
| password |
| last_login |
| is_superuser |
| is_active |
| is_staff |
| date_joined |
| full_name |
| phone_number |
| address_line1 |
| address_line2 |
| city |
| avatar |
| role |

### tb_userprofile

| Field |
|---|
| id_userprofile |
| id_user |
| created_at |
| updated_at |

### tb_notification

| Field |
|---|
| id_notification |
| id_user |
| title |
| message |
| link |
| is_read |
| created_at |

### tb_category

| Field |
|---|
| id_category |
| name |
| slug |
| icon |
| order |

### tb_brand

| Field |
|---|
| id_brand |
| name |
| slug |
| logo |

### tb_product

| Field |
|---|
| id_product |
| id_brand |
| id_category |
| name |
| color |
| color_secondary |
| slug |
| description |
| condition |
| price |
| crossed_price |
| is_active |
| is_featured |
| created_at |

### tb_product_image

| Field |
|---|
| id_product_image |
| id_product |
| image |
| is_primary |
| order |

### tb_product_size

| Field |
|---|
| id_product_size |
| id_product |
| size |
| stock |

### tb_banner

| Field |
|---|
| id_banner |
| title |
| subtitle |
| image |
| link |
| order |
| is_active |

### tb_review

| Field |
|---|
| id_review |
| id_product |
| id_user |
| id_order_item |
| rating |
| comment |
| image1 |
| image2 |
| image3 |
| is_visible |
| created_at |

### tb_voucher

| Field |
|---|
| id_voucher |
| code |
| discount_type |
| discount_value |
| min_purchase |
| valid_from |
| valid_to |
| is_active |

### tb_wishlist

| Field |
|---|
| id_wishlist |
| id_user |
| id_product |
| created_at |

### tb_cart

| Field |
|---|
| id_cart |
| id_user |
| session_key |
| created_at |
| updated_at |

### tb_cart_item

| Field |
|---|
| id_cart_item |
| id_cart |
| id_product |
| id_product_size |
| quantity |

### tb_order

| Field |
|---|
| id_order |
| id_user |
| id_voucher |
| order_number |
| status |
| midtrans_transaction_id |
| courier |
| shipping_service |
| shipping_cost |
| tracking_number |
| discount_amount |
| subtotal |
| total |
| created_at |
| updated_at |

### tb_order_item

| Field |
|---|
| id_order_item |
| id_order |
| id_product |
| size_str |
| product_name |
| price |
| quantity |

### tb_shipping_address

| Field |
|---|
| id_shipping_address |
| id_order |
| recipient_name |
| phone_number |
| province_id |
| province_name |
| city_id |
| city_name |
| district_name |
| postal_code |
| full_address |

### tb_warranty_claim

| Field |
|---|
| id_warranty_claim |
| id_order_item |
| id_user |
| kategori |
| reason |
| evidence_image |
| status |
| admin_notes |
| created_at |
| updated_at |

### tb_footer_icon

| Field |
|---|
| id_footer_icon |
| title |
| image |
| order |

---

## 3. 2NF — Second Normal Form

Setiap tabel sudah berada di 1NF dan setiap field non-primary-key bergantung penuh pada Primary Key (PK). Tidak ada ketergantungan parsial.

### tb_user

| Field | Keterangan |
|---|---|
| **PK** id_user | Primary Key |
| username | |
| email | |
| password | |
| last_login | |
| is_superuser | |
| is_active | |
| is_staff | |
| date_joined | |
| full_name | |
| phone_number | |
| address_line1 | |
| address_line2 | |
| city | |
| avatar | |
| role | |

### tb_userprofile

| Field | Keterangan |
|---|---|
| **PK** id_userprofile | Primary Key |
| id_user | |
| created_at | |
| updated_at | |

### tb_notification

| Field | Keterangan |
|---|---|
| **PK** id_notification | Primary Key |
| id_user | |
| title | |
| message | |
| link | |
| is_read | |
| created_at | |

### tb_category

| Field | Keterangan |
|---|---|
| **PK** id_category | Primary Key |
| name | |
| slug | |
| icon | |
| order | |

### tb_brand

| Field | Keterangan |
|---|---|
| **PK** id_brand | Primary Key |
| name | |
| slug | |
| logo | |

### tb_product

| Field | Keterangan |
|---|---|
| **PK** id_product | Primary Key |
| id_brand | |
| id_category | |
| name | |
| color | |
| color_secondary | |
| slug | |
| description | |
| condition | |
| price | |
| crossed_price | |
| is_active | |
| is_featured | |
| created_at | |

### tb_product_image

| Field | Keterangan |
|---|---|
| **PK** id_product_image | Primary Key |
| id_product | |
| image | |
| is_primary | |
| order | |

### tb_product_size

| Field | Keterangan |
|---|---|
| **PK** id_product_size | Primary Key |
| id_product | |
| size | |
| stock | |

### tb_banner

| Field | Keterangan |
|---|---|
| **PK** id_banner | Primary Key |
| title | |
| subtitle | |
| image | |
| link | |
| order | |
| is_active | |

### tb_review

| Field | Keterangan |
|---|---|
| **PK** id_review | Primary Key |
| id_product | |
| id_user | |
| id_order_item | |
| rating | |
| comment | |
| image1 | |
| image2 | |
| image3 | |
| is_visible | |
| created_at | |

### tb_voucher

| Field | Keterangan |
|---|---|
| **PK** id_voucher | Primary Key |
| code | |
| discount_type | |
| discount_value | |
| min_purchase | |
| valid_from | |
| valid_to | |
| is_active | |

### tb_wishlist

| Field | Keterangan |
|---|---|
| **PK** id_wishlist | Primary Key |
| id_user | |
| id_product | |
| created_at | |

### tb_cart

| Field | Keterangan |
|---|---|
| **PK** id_cart | Primary Key |
| id_user | |
| session_key | |
| created_at | |
| updated_at | |

### tb_cart_item

| Field | Keterangan |
|---|---|
| **PK** id_cart_item | Primary Key |
| id_cart | |
| id_product | |
| id_product_size | |
| quantity | |

### tb_order

| Field | Keterangan |
|---|---|
| **PK** id_order | Primary Key |
| id_user | |
| id_voucher | |
| order_number | |
| status | |
| midtrans_transaction_id | |
| courier | |
| shipping_service | |
| shipping_cost | |
| tracking_number | |
| discount_amount | |
| subtotal | |
| total | |
| created_at | |
| updated_at | |

### tb_order_item

| Field | Keterangan |
|---|---|
| **PK** id_order_item | Primary Key |
| id_order | |
| id_product | |
| size_str | |
| product_name | |
| price | |
| quantity | |

### tb_shipping_address

| Field | Keterangan |
|---|---|
| **PK** id_shipping_address | Primary Key |
| id_order | |
| recipient_name | |
| phone_number | |
| province_id | |
| province_name | |
| city_id | |
| city_name | |
| district_name | |
| postal_code | |
| full_address | |

### tb_warranty_claim

| Field | Keterangan |
|---|---|
| **PK** id_warranty_claim | Primary Key |
| id_order_item | |
| id_user | |
| kategori | |
| reason | |
| evidence_image | |
| status | |
| admin_notes | |
| created_at | |
| updated_at | |

### tb_footer_icon

| Field | Keterangan |
|---|---|
| **PK** id_footer_icon | Primary Key |
| title | |
| image | |
| order | |

---

## 4. 3NF — Third Normal Form

Setiap tabel sudah berada di 2NF dan tidak ada ketergantungan transitif — setiap field non-primary-key hanya bergantung pada Primary Key, bukan pada field non-PK lainnya. Foreign Key (FK) ditambahkan secara eksplisit untuk menunjukkan relasi antar tabel.

### tb_user

| Field | Keterangan |
|---|---|
| **PK** id_user | Primary Key |
| username | |
| email | |
| password | |
| last_login | |
| is_superuser | |
| is_active | |
| is_staff | |
| date_joined | |
| full_name | |
| phone_number | |
| address_line1 | |
| address_line2 | |
| city | |
| avatar | |
| role | |

### tb_userprofile

| Field | Keterangan |
|---|---|
| **PK** id_userprofile | Primary Key |
| **FK** id_user | → tb_user.id_user |
| created_at | |
| updated_at | |

### tb_notification

| Field | Keterangan |
|---|---|
| **PK** id_notification | Primary Key |
| **FK** id_user | → tb_user.id_user |
| title | |
| message | |
| link | |
| is_read | |
| created_at | |

### tb_category

| Field | Keterangan |
|---|---|
| **PK** id_category | Primary Key |
| name | |
| slug | |
| icon | |
| order | |

### tb_brand

| Field | Keterangan |
|---|---|
| **PK** id_brand | Primary Key |
| name | |
| slug | |
| logo | |

### tb_product

| Field | Keterangan |
|---|---|
| **PK** id_product | Primary Key |
| **FK** id_brand | → tb_brand.id_brand |
| **FK** id_category | → tb_category.id_category |
| name | |
| color | |
| color_secondary | |
| slug | |
| description | |
| condition | |
| price | |
| crossed_price | |
| is_active | |
| is_featured | |
| created_at | |

### tb_product_image

| Field | Keterangan |
|---|---|
| **PK** id_product_image | Primary Key |
| **FK** id_product | → tb_product.id_product |
| image | |
| is_primary | |
| order | |

### tb_product_size

| Field | Keterangan |
|---|---|
| **PK** id_product_size | Primary Key |
| **FK** id_product | → tb_product.id_product |
| size | |
| stock | |

### tb_banner

| Field | Keterangan |
|---|---|
| **PK** id_banner | Primary Key |
| title | |
| subtitle | |
| image | |
| link | |
| order | |
| is_active | |

### tb_review

| Field | Keterangan |
|---|---|
| **PK** id_review | Primary Key |
| **FK** id_product | → tb_product.id_product |
| **FK** id_user | → tb_user.id_user |
| **FK** id_order_item | → tb_order_item.id_order_item |
| rating | |
| comment | |
| image1 | |
| image2 | |
| image3 | |
| is_visible | |
| created_at | |

### tb_voucher

| Field | Keterangan |
|---|---|
| **PK** id_voucher | Primary Key |
| code | |
| discount_type | |
| discount_value | |
| min_purchase | |
| valid_from | |
| valid_to | |
| is_active | |

### tb_wishlist

| Field | Keterangan |
|---|---|
| **PK** id_wishlist | Primary Key |
| **FK** id_user | → tb_user.id_user |
| **FK** id_product | → tb_product.id_product |
| created_at | |

### tb_cart

| Field | Keterangan |
|---|---|
| **PK** id_cart | Primary Key |
| **FK** id_user | → tb_user.id_user |
| session_key | |
| created_at | |
| updated_at | |

### tb_cart_item

| Field | Keterangan |
|---|---|
| **PK** id_cart_item | Primary Key |
| **FK** id_cart | → tb_cart.id_cart |
| **FK** id_product | → tb_product.id_product |
| **FK** id_product_size | → tb_product_size.id_product_size |
| quantity | |

### tb_order

| Field | Keterangan |
|---|---|
| **PK** id_order | Primary Key |
| **FK** id_user | → tb_user.id_user |
| **FK** id_voucher | → tb_voucher.id_voucher |
| order_number | |
| status | |
| midtrans_transaction_id | |
| courier | |
| shipping_service | |
| shipping_cost | |
| tracking_number | |
| discount_amount | |
| subtotal | |
| total | |
| created_at | |
| updated_at | |

### tb_order_item

| Field | Keterangan |
|---|---|
| **PK** id_order_item | Primary Key |
| **FK** id_order | → tb_order.id_order |
| **FK** id_product | → tb_product.id_product |
| size_str | |
| product_name | |
| price | |
| quantity | |

### tb_shipping_address

| Field | Keterangan |
|---|---|
| **PK** id_shipping_address | Primary Key |
| **FK** id_order | → tb_order.id_order |
| recipient_name | |
| phone_number | |
| province_id | |
| province_name | |
| city_id | |
| city_name | |
| district_name | |
| postal_code | |
| full_address | |

### tb_warranty_claim

| Field | Keterangan |
|---|---|
| **PK** id_warranty_claim | Primary Key |
| **FK** id_order_item | → tb_order_item.id_order_item |
| **FK** id_user | → tb_user.id_user |
| kategori | |
| reason | |
| evidence_image | |
| status | |
| admin_notes | |
| created_at | |
| updated_at | |

### tb_footer_icon

| Field | Keterangan |
|---|---|
| **PK** id_footer_icon | Primary Key |
| title | |
| image | |
| order | |

---

## Ringkasan Relasi Antar Tabel (3NF)

| Tabel | Berelasi Dengan | Jenis Relasi |
|---|---|---|
| tb_userprofile | tb_user | One-to-One |
| tb_notification | tb_user | Many-to-One |
| tb_product | tb_brand | Many-to-One |
| tb_product | tb_category | Many-to-One |
| tb_product_image | tb_product | Many-to-One |
| tb_product_size | tb_product | Many-to-One |
| tb_review | tb_product, tb_user, tb_order_item | Many-to-One |
| tb_wishlist | tb_user, tb_product | Many-to-One |
| tb_cart | tb_user | One-to-One |
| tb_cart_item | tb_cart, tb_product, tb_product_size | Many-to-One |
| tb_order | tb_user, tb_voucher | Many-to-One |
| tb_order_item | tb_order, tb_product | Many-to-One |
| tb_shipping_address | tb_order | One-to-One |
| tb_warranty_claim | tb_order_item, tb_user | One-to-One / Many-to-One |
