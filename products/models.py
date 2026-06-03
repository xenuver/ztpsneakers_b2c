from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    icon = models.ImageField(upload_to='categories/icons/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['order', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    logo = models.ImageField(upload_to='brands/logos/', blank=True, null=True)

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Product(models.Model):
    CONDITION_CHOICES = [
        ('new', 'New'),
        ('second', 'Second'),
    ]
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    description = models.TextField()
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='new')
    price = models.DecimalField(max_digits=12, decimal_places=2)
    crossed_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, help_text="Harga coret untuk diskon")
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    def get_primary_image(self):
        primary = self.images.filter(is_primary=True).first()
        if primary:
            return primary.image.url
        first_img = self.images.first()
        return first_img.image.url if first_img else None

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/images/')
    is_primary = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', '-is_primary']

    def __str__(self):
        return f"Image for {self.product.name}"

class ProductSize(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sizes')
    size = models.CharField(max_length=10, help_text="e.g. 35, 40, 42.5")
    stock = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('product', 'size')
        ordering = ['size']

    def __str__(self):
        return f"{self.product.name} - Size {self.size}"

    def save(self, *args, **kwargs):
        # Determine if this is an update that drops total stock to <= 2
        is_existing = self.pk is not None
        super().save(*args, **kwargs)
        
        # Calculate total stock
        total_stock = sum(s.stock for s in self.product.sizes.all())
        if total_stock <= 2:
            from django.apps import apps
            Wishlist = apps.get_model('orders', 'Wishlist')
            Notification = apps.get_model('core', 'Notification')
            
            wishlists = Wishlist.objects.filter(product=self.product)
            for w in wishlists:
                # Check if unread notification already exists to avoid spamming
                if not Notification.objects.filter(user=w.user, title="Stok Hampir Habis!", message__contains=self.product.name, is_read=False).exists():
                    Notification.objects.create(
                        user=w.user,
                        title="Stok Hampir Habis!",
                        message=f"Produk wishlist Anda '{self.product.name}' sisa {total_stock} stok terakhir. Beli sekarang sebelum kehabisan!",
                        link=f"/produk/{self.product.slug}/"
                    )

class Banner(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='banners/')
    link = models.URLField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', '-id']

    def __str__(self):
        return self.title
