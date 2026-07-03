from django.db import models
from django.conf import settings
from products.models import Product, ProductSize
from django.utils import timezone

class Voucher(models.Model):
    DISCOUNT_TYPES = [
        ('percentage', 'Percentage'),
        ('nominal', 'Nominal'),
    ]
    code = models.CharField(max_length=20, unique=True)
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPES)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    max_discount = models.DecimalField(max_digits=12, decimal_places=2, default=0, help_text="Batas maksimum diskon (0 = tanpa batas)")
    min_purchase = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='vouchers')
    is_used = models.BooleanField(default=False)

    def is_valid(self, purchase_amount):
        now = timezone.now()
        if not self.is_active:
            return False
        if self.is_used:
            return False
        if now < self.valid_from or now > self.valid_to:
            return False
        if purchase_amount < self.min_purchase:
            return False
        return True
        
    def calculate_discount(self, purchase_amount):
        if self.discount_type == 'percentage':
            discount = (purchase_amount * self.discount_value) / 100
            if self.max_discount > 0:
                discount = min(discount, self.max_discount)
            return discount
        return min(self.discount_value, purchase_amount)

    def __str__(self):
        return self.code


class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wishlists')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.email} - {self.product.name}"

class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='cart')
    session_key = models.CharField(max_length=40, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_total_price(self):
        return sum(item.get_cost() for item in self.items.all())

    def __str__(self):
        if self.user:
            return f"Cart of {self.user.email}"
        return f"Guest Cart {self.session_key}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(ProductSize, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('cart', 'product', 'size')

    def get_cost(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name} (Size: {self.size.size})"

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Payment'),
        ('paid', 'Paid'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    order_number = models.CharField(max_length=50, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Midtrans Info
    midtrans_transaction_id = models.CharField(max_length=100, null=True, blank=True)
    
    # Shipping Info
    courier = models.CharField(max_length=50) # jne, pos, tiki
    shipping_service = models.CharField(max_length=100) # REG, YES, dll
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tracking_number = models.CharField(max_length=100, null=True, blank=True)
    
    # Voucher Info
    voucher = models.ForeignKey(Voucher, on_delete=models.SET_NULL, null=True, blank=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Cost Summary
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    total = models.DecimalField(max_digits=12, decimal_places=2) # subtotal + shipping_cost
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.order_number

    @property
    def has_shipping_address(self):
        return hasattr(self, 'shipping_address')

    @property
    def is_warranty_expired(self):
        if self.status != 'completed':
            return False
        from django.utils import timezone
        from datetime import timedelta
        return self.updated_at < timezone.now() - timedelta(days=7)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    size_str = models.CharField(max_length=10) # Simpan sbg string karena ProductSize bisa dihapus
    product_name = models.CharField(max_length=200) # Snap shot nama saat dibeli
    price = models.DecimalField(max_digits=12, decimal_places=2) # Snap shot harga saat dibeli
    quantity = models.PositiveIntegerField(default=1)

    def get_cost(self):
        return self.price * self.quantity

    @property
    def has_review(self):
        return hasattr(self, 'review')
        
    @property
    def has_warranty_claim(self):
        return hasattr(self, 'warranty_claim')

    def __str__(self):
        return f"{self.quantity} x {self.product_name}"

class ShippingAddress(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='shipping_address')
    recipient_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    province_id = models.CharField(max_length=50)
    province_name = models.CharField(max_length=100)
    city_id = models.CharField(max_length=50)
    city_name = models.CharField(max_length=100)
    district_name = models.CharField(max_length=100) # Kecamatan
    postal_code = models.CharField(max_length=20)
    full_address = models.TextField()

    def __str__(self):
        return f"Address for Order {self.order.order_number}"

class WarrantyClaim(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Menunggu Pengecekan'),
        ('approved', 'Disetujui'),
        ('rejected', 'Ditolak'),
        ('resolved', 'Selesai'),
    ]
    KATEGORI_CHOICES = [
        ('cacat_produk', 'Cacat Produk'),
        ('salah_ukuran', 'Salah Ukuran / Barang Berbeda'),
        ('tidak_sesuai_foto', 'Tidak Sesuai Foto'),
        ('lainnya', 'Lainnya'),
    ]
    order_item = models.OneToOneField(OrderItem, on_delete=models.CASCADE, related_name='warranty_claim')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    kategori = models.CharField(max_length=50, choices=KATEGORI_CHOICES, default='lainnya')
    reason = models.TextField()
    evidence_image = models.ImageField(upload_to='warranties/')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    admin_notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"Claim for {self.order_item.product_name} - {self.get_status_display()}"
