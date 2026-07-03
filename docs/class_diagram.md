# Class Diagram — ZTP Sneakers B2C Platform

> **Versi:** 1.0  
> **Tanggal:** 2026  
> **Author:** Wahyu Ahmad Cahyadi (221103805)  
> **Tool:** Mermaid  

> **Cara Render:** Copy kode di bawah ini lalu paste di [Mermaid Live Editor](https://mermaid.live/) atau gunakan ekstensi Mermaid di VSCode.

---

```mermaid
classDiagram
    class User {
        +int id
        +String email
        +String username
        +String phone_number
        +text address
        +String role
        +boolean is_active
        +boolean is_staff
    }

    class UserProfile {
        +int id
        +datetime created_at
        +datetime updated_at
    }

    class Category {
        +int id
        +String name
        +String slug
        +int order
    }

    class Brand {
        +int id
        +String name
        +String slug
    }

    class Product {
        +int id
        +String name
        +String slug
        +String color
        +String condition
        +decimal price
        +decimal crossed_price
        +boolean is_active
        +boolean is_featured
        +datetime created_at
        +get_primary_image() String
        +average_rating() float
        +total_stock() int
    }

    class ProductImage {
        +int id
        +String image
        +boolean is_primary
        +int order
    }

    class ProductSize {
        +int id
        +String size
        +int stock
    }

    class Review {
        +int id
        +int rating
        +text comment
        +boolean is_visible
        +datetime created_at
    }

    class Wishlist {
        +int id
        +datetime created_at
    }

    class Voucher {
        +int id
        +String code
        +String discount_type
        +decimal discount_value
        +decimal min_purchase
        +datetime valid_from
        +datetime valid_to
        +boolean is_active
        +is_valid(amount) boolean
        +calculate_discount(amount) decimal
    }

    class Cart {
        +int id
        +String session_key
        +datetime created_at
        +datetime updated_at
        +get_total_price() decimal
    }

    class CartItem {
        +int id
        +int quantity
        +get_cost() decimal
    }

    class Order {
        +int id
        +String order_number
        +String status
        +String midtrans_transaction_id
        +String courier
        +String shipping_service
        +decimal shipping_cost
        +String tracking_number
        +decimal subtotal
        +decimal total
        +datetime created_at
    }

    class OrderItem {
        +int id
        +String product_name
        +String size_str
        +decimal price
        +int quantity
        +get_cost() decimal
    }

    class ShippingAddress {
        +int id
        +String recipient_name
        +String phone_number
        +String province_name
        +String city_name
        +String district_name
        +text full_address
    }

    class WarrantyClaim {
        +int id
        +String kategori
        +text reason
        +String status
        +text admin_notes
        +datetime created_at
    }

    direction TB

    %% 1. Relasi User (Level Atas)
    User "1" --> "0..1" UserProfile : memiliki
    User "1" --> "0..1" Cart : memiliki
    User "1" --> "*" Order : melakukan
    User "1" --> "*" Wishlist : menyimpan
    User "1" --> "*" Review : menulis
    User "1" --> "*" WarrantyClaim : mengajukan

    %% 2. Relasi Transaksi (Level Menengah)
    Cart "1" *--> "*" CartItem : berisi
    Order "1" *--> "*" OrderItem : terdiri dari
    Order "1" --> "1" ShippingAddress : memiliki
    Order "*" --> "0..1" Voucher : menggunakan

    %% 3. Relasi ke Produk (Level Bawah)
    Category "1" --> "*" Product : mengelompokkan
    Brand "1" --> "*" Product : memproduksi
    Wishlist "*" --> "1" Product : menautkan
    CartItem "*" --> "1" Product : merujuk
    OrderItem "*" --> "0..1" Product : mereferensikan
    Review "*" --> "1" Product : menilai

    %% 4. Detail Produk (Level Paling Bawah)
    Product "1" *--> "*" ProductImage : memiliki foto
    Product "1" *--> "*" ProductSize : memiliki ukuran
    CartItem "*" --> "1" ProductSize : memilih ukuran

    %% 5. Relasi Lintas OrderItem
    OrderItem "1" --> "0..1" Review : diulas pada
    OrderItem "1" --> "0..1" WarrantyClaim : diklaim pada
```
