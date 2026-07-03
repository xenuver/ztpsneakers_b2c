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
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Category.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    @property
    def hero_image(self):
        # Get the top product (by highest total view_count or just highest id if no view_count exists)
        # Using -created_at as fallback since I don't see view_count in product fields here.
        # Let's check Product fields again. Product has average_rating and review_count.
        # I'll sort by review_count and average_rating.
        top_product = self.products.order_by('-created_at').first()
        # To get the best product if they have sold_count or similar, but since they don't, I'll just use the first product that has images.
        for p in self.products.all():
            if p.get_primary_image():
                return p.get_primary_image()
        return None

class Brand(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    logo = models.ImageField(upload_to='brands/logos/', blank=True, null=True)

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Brand.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Product(models.Model):
    CONDITION_CHOICES = [
        ('new', 'New'),
        ('second', 'Second'),
    ]
    COLOR_CHOICES = [
        ('black', 'Hitam'),
        ('white', 'Putih'),
        ('red', 'Merah'),
        ('blue', 'Biru'),
        ('green', 'Hijau'),
        ('yellow', 'Kuning'),
        ('grey', 'Abu-abu'),
        ('brown', 'Cokelat'),
        ('multi', 'Multi-Warna'),
    ]
    
    name = models.CharField(max_length=200)
    color = models.CharField(max_length=20, choices=COLOR_CHOICES, default='multi')
    color_secondary = models.CharField(max_length=20, choices=COLOR_CHOICES, blank=True, null=True, help_text="Warna sekunder (Opsional)")
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
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    def get_primary_image(self):
        primary = self.images.filter(is_primary=True).first()
        if primary:
            return primary.image.url
        first_img = self.images.first()
        return first_img.image.url if first_img else None
        
    @property
    def average_rating(self):
        from django.db.models import Avg
        avg = self.reviews.aggregate(Avg('rating'))['rating__avg']
        return round(avg, 1) if avg else 0

    @property
    def review_count(self):
        return self.reviews.count()

    @property
    def total_stock(self):
        return sum(s.stock for s in self.sizes.all())

    @property
    def is_new(self):
        from django.utils import timezone
        import datetime
        return self.created_at >= timezone.now() - datetime.timedelta(days=7)

    @property
    def is_hot(self):
        return self.average_rating >= 4.0 and self.review_count >= 3

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

from django.conf import settings

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order_item = models.OneToOneField('orders.OrderItem', on_delete=models.SET_NULL, null=True, blank=True)
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    image = models.ImageField(upload_to='reviews/', null=True, blank=True)
    image2 = models.ImageField(upload_to='reviews/', null=True, blank=True)
    image3 = models.ImageField(upload_to='reviews/', null=True, blank=True)
    is_visible = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.user.email} - {self.product.name} ({self.rating}/5)"
