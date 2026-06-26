# Class Diagram — ZTP Sneakers B2C Platform

> **Versi:** 1.0  
> **Tanggal:** 2026  
> **Author:** Wahyu Ahmad Cahyadi (221103805)  
> **Tool:** PlantUML  

> **Cara Render:** Copy kode di bawah ini lalu paste di [PlantUML Online](https://www.plantuml.com/plantuml/uml/) atau gunakan ekstensi PlantUML di VSCode.

---

```plantuml
@startuml ClassDiagram_ZTPSneakers
title Class Diagram - ZTP Sneakers B2C Platform

skinparam classAttributeIconSize 0
skinparam roundcorner 5
skinparam classBackgroundColor #FFFFFF
skinparam classBorderColor #555555
skinparam arrowColor #333333

class User {
  +id: int
  +email: String
  +username: String
  +phone_number: String
  +address: text
  +role: String
  +is_active: boolean
  +is_staff: boolean
}

class UserProfile {
  +id: int
  +created_at: datetime
  +updated_at: datetime
}

class Category {
  +id: int
  +name: String
  +slug: String
  +order: int
}

class Brand {
  +id: int
  +name: String
  +slug: String
}

class Product {
  +id: int
  +name: String
  +slug: String
  +color: String
  +condition: String
  +price: decimal
  +crossed_price: decimal
  +is_active: boolean
  +is_featured: boolean
  +created_at: datetime
  +get_primary_image(): String
  +average_rating(): float
  +total_stock(): int
}

class ProductImage {
  +id: int
  +image: String
  +is_primary: boolean
  +order: int
}

class ProductSize {
  +id: int
  +size: String
  +stock: int
}

class Review {
  +id: int
  +rating: int
  +comment: text
  +is_visible: boolean
  +created_at: datetime
}

class Wishlist {
  +id: int
  +created_at: datetime
}

class Voucher {
  +id: int
  +code: String
  +discount_type: String
  +discount_value: decimal
  +min_purchase: decimal
  +valid_from: datetime
  +valid_to: datetime
  +is_active: boolean
  +is_valid(amount): boolean
  +calculate_discount(amount): decimal
}

class Cart {
  +id: int
  +session_key: String
  +created_at: datetime
  +updated_at: datetime
  +get_total_price(): decimal
}

class CartItem {
  +id: int
  +quantity: int
  +get_cost(): decimal
}

class Order {
  +id: int
  +order_number: String
  +status: String
  +midtrans_transaction_id: String
  +courier: String
  +shipping_service: String
  +shipping_cost: decimal
  +tracking_number: String
  +subtotal: decimal
  +total: decimal
  +created_at: datetime
}

class OrderItem {
  +id: int
  +product_name: String
  +size_str: String
  +price: decimal
  +quantity: int
  +get_cost(): decimal
}

class ShippingAddress {
  +id: int
  +recipient_name: String
  +phone_number: String
  +province_name: String
  +city_name: String
  +district_name: String
  +full_address: text
}

class WarrantyClaim {
  +id: int
  +kategori: String
  +reason: text
  +status: String
  +admin_notes: text
  +created_at: datetime
}

' Relasi User
User "1" -- "0..1" UserProfile : memiliki >
User "1" -- "*" Order : melakukan >
User "1" -- "0..1" Cart : memiliki >
User "1" -- "*" Wishlist : menyimpan >
User "1" -- "*" Review : menulis >
User "1" -- "*" WarrantyClaim : mengajukan >

' Relasi Produk
Product "*" -- "1" Category : dikelompokkan dalam >
Product "*" -- "1" Brand : diproduksi oleh >
Product "1" *-- "*" ProductImage : memiliki >
Product "1" *-- "*" ProductSize : ukuran >
Product "1" -- "*" Review : menerima >
Product "1" -- "*" Wishlist : disimpan di >

' Relasi Keranjang
Cart "1" *-- "*" CartItem : berisi >
CartItem "*" -- "1" Product : merujuk >
CartItem "*" -- "1" ProductSize : merujuk >

' Relasi Pesanan
Order "1" *-- "*" OrderItem : terdiri dari >
Order "1" -- "1" ShippingAddress : memiliki >
Order "*" -- "0..1" Voucher : menggunakan >

OrderItem "*" -- "0..1" Product : mereferensikan >
OrderItem "1" -- "0..1" Review : diulas >
OrderItem "1" -- "0..1" WarrantyClaim : diklaim >

@enduml
```
