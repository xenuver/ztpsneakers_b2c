# Class Diagram (DBML) — ZTP Sneakers B2C

> **Tool:** [dbdiagram.io](https://dbdiagram.io)  
> **Cara Render:** Copy seluruh kode DBML di bawah ini, lalu paste di sebelah kiri halaman web dbdiagram.io.

---

```dbml
// ==========================================
// CLASS DIAGRAM B2C ZTP SNEAKERS (DBML)
// ==========================================

Table User {
  id int [pk, increment]
  email varchar
  username varchar
  phone_number varchar
  address text
  role varchar [note: 'customer | admin_toko | owner']
  is_active boolean
  is_staff boolean
}

Table UserProfile {
  id int [pk, increment]
  user_id int [ref: - User.id]
  created_at datetime
  updated_at datetime
}

Table Category {
  id int [pk, increment]
  name varchar
  slug varchar
  order int
}

Table Brand {
  id int [pk, increment]
  name varchar
  slug varchar
}

Table Product {
  id int [pk, increment]
  brand_id int [ref: > Brand.id]
  category_id int [ref: > Category.id]
  name varchar
  slug varchar
  color varchar
  condition varchar
  price decimal
  crossed_price decimal
  is_active boolean
  is_featured boolean
  created_at datetime
  
  Note: '''
  Methods / Properties:
  + get_primary_image()
  + average_rating()
  + review_count()
  + total_stock()
  + is_new()
  + is_hot()
  '''
}

Table ProductImage {
  id int [pk, increment]
  product_id int [ref: > Product.id]
  image varchar
  is_primary boolean
  order int
}

Table ProductSize {
  id int [pk, increment]
  product_id int [ref: > Product.id]
  size varchar
  stock int
}

Table Review {
  id int [pk, increment]
  product_id int [ref: > Product.id]
  user_id int [ref: > User.id]
  order_item_id int [ref: - OrderItem.id]
  rating int
  comment text
  is_visible boolean
  created_at datetime
}

Table Wishlist {
  id int [pk, increment]
  user_id int [ref: > User.id]
  product_id int [ref: > Product.id]
  created_at datetime
}

Table Voucher {
  id int [pk, increment]
  code varchar
  discount_type varchar
  discount_value decimal
  min_purchase decimal
  valid_from datetime
  valid_to datetime
  is_active boolean
  
  Note: '''
  Methods:
  + is_valid(amount)
  + calculate_discount(amount)
  '''
}

Table Cart {
  id int [pk, increment]
  user_id int [ref: - User.id]
  session_key varchar
  created_at datetime
  updated_at datetime
  
  Note: '''
  Methods:
  + get_total_price()
  '''
}

Table CartItem {
  id int [pk, increment]
  cart_id int [ref: > Cart.id]
  product_id int [ref: > Product.id]
  size_id int [ref: > ProductSize.id]
  quantity int
  
  Note: '''
  Methods:
  + get_cost()
  '''
}

Table Order {
  id int [pk, increment]
  user_id int [ref: > User.id]
  voucher_id int [ref: > Voucher.id]
  order_number varchar
  status varchar
  midtrans_transaction_id varchar
  courier varchar
  shipping_service varchar
  shipping_cost decimal
  tracking_number varchar
  subtotal decimal
  total decimal
  created_at datetime
  
  Note: '''
  Properties:
  + has_shipping_address()
  + is_warranty_expired()
  '''
}

Table OrderItem {
  id int [pk, increment]
  order_id int [ref: > Order.id]
  product_id int [ref: > Product.id]
  product_name varchar
  size_str varchar
  price decimal
  quantity int
  
  Note: '''
  Methods / Properties:
  + get_cost()
  + has_review()
  + has_warranty_claim()
  '''
}

Table ShippingAddress {
  id int [pk, increment]
  order_id int [ref: - Order.id]
  recipient_name varchar
  phone_number varchar
  province_name varchar
  city_name varchar
  district_name varchar
  full_address text
}

Table WarrantyClaim {
  id int [pk, increment]
  order_item_id int [ref: - OrderItem.id]
  user_id int [ref: > User.id]
  kategori varchar
  reason text
  status varchar
  admin_notes text
  created_at datetime
}
```
