import os
import sys
import django
import random
from django.core.files import File
from django.conf import settings

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ztpsneakers.settings')
django.setup()

from products.models import Category, Brand, Product, ProductSize, ProductImage
from django.core.files.uploadedfile import SimpleUploadedFile

def run():
    print("Mulai seeding data ZTP Sneakers...")

    # Bersihkan data lama jika ingin mulai dari awal
    # Product.objects.all().delete()
    # Brand.objects.all().delete()
    # Category.objects.all().delete()

    # 1. Buat Kategori
    categories = ['Sneakers', 'Running', 'Casual', 'Basketball']
    cat_objs = []
    for cat_name in categories:
        cat, created = Category.objects.get_or_create(name=cat_name)
        cat_objs.append(cat)
        if created:
            print(f"Kategori '{cat_name}' dibuat.")

    # 2. Buat Brand
    brands = ['Nike', 'Adidas', 'New Balance', 'Puma', 'Vans', 'ZTP Exclusives']
    brand_objs = []
    for brand_name in brands:
        brand, created = Brand.objects.get_or_create(name=brand_name)
        brand_objs.append(brand)
        if created:
            print(f"Brand '{brand_name}' dibuat.")

    # Cek folder media untuk foto
    media_root = settings.MEDIA_ROOT
    default_image_path = os.path.join(media_root, 'products', 'images')
    if not os.path.exists(default_image_path):
        os.makedirs(default_image_path, exist_ok=True)
    
    # Kumpulkan foto yang ada di folder products/images/
    available_images = []
    if os.path.exists(default_image_path):
        for f in os.listdir(default_image_path):
            if f.endswith(('.jpg', '.jpeg', '.png', '.webp')):
                available_images.append(os.path.join(default_image_path, f))

    def assign_image(product):
        if available_images:
            img_path = random.choice(available_images)
            filename = os.path.basename(img_path)
            with open(img_path, 'rb') as f:
                ProductImage.objects.create(
                    product=product,
                    image=File(f, name=filename),
                    is_primary=True
                )

    # 3. Buat Produk: Normal dengan beberapa ukuran dan stok acak
    p1, created = Product.objects.get_or_create(
        name="Nike Air Force 1 '07",
        defaults={
            'brand': Brand.objects.get(name='Nike'),
            'category': Category.objects.get(name='Sneakers'),
            'description': 'The radiance lives on in the Nike Air Force 1 ’07, the b-ball icon that puts a fresh spin on what you know best.',
            'price': 1500000.00,
            'color': 'white',
            'condition': 'new',
            'is_featured': True
        }
    )
    if created:
        ProductSize.objects.create(product=p1, size='40', stock=5)
        ProductSize.objects.create(product=p1, size='41', stock=12)
        ProductSize.objects.create(product=p1, size='42', stock=8)
        assign_image(p1)
        print(f"Produk normal '{p1.name}' dibuat.")

    # 4. Buat Produk: SOLD OUT (Stok 0)
    p2, created = Product.objects.get_or_create(
        name="Adidas Yeezy Boost 350 V2 Zebra",
        defaults={
            'brand': Brand.objects.get(name='Adidas'),
            'category': Category.objects.get(name='Sneakers'),
            'description': 'Koleksi Yeezy yang sangat langka. Sayangnya sedang habis terjual.',
            'price': 4500000.00,
            'color': 'multi',
            'condition': 'second',
            'is_featured': True
        }
    )
    if created:
        ProductSize.objects.create(product=p2, size='40', stock=0)
        ProductSize.objects.create(product=p2, size='42', stock=0)
        assign_image(p2)
        print(f"Produk SOLD OUT '{p2.name}' dibuat.")

    # 5. Buat Produk: Stok = 1 dengan 2 ukuran (salah satu ukuran stoknya 0, satunya 1)
    p3, created = Product.objects.get_or_create(
        name="New Balance 550 White Green",
        defaults={
            'brand': Brand.objects.get(name='New Balance'),
            'category': Category.objects.get(name='Casual'),
            'description': 'Sisa satu ukuran terakhir! Jangan sampai kehabisan.',
            'price': 2200000.00,
            'color': 'green',
            'condition': 'new',
            'is_featured': False
        }
    )
    if created:
        ProductSize.objects.create(product=p3, size='39', stock=0)
        ProductSize.objects.create(product=p3, size='41', stock=1)
        assign_image(p3)
        print(f"Produk stok terbatas '{p3.name}' dibuat.")

    print("Seeding selesai! Anda bisa menjalankan 'python seed.py' kapan saja untuk mengisi ulang database.")

if __name__ == '__main__':
    run()
