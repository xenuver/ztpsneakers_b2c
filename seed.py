import os
import sys
import django
from django.core.files import File
from django.conf import settings

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ztpsneakers.settings')
django.setup()

from products.models import Category, Brand, Product, ProductSize, ProductImage, Banner

def run():
    print("Mulai reseeding data ZTP Sneakers...")

    # Bersihkan data lama
    Product.objects.all().delete()
    Brand.objects.all().delete()
    Category.objects.all().delete()
    Banner.objects.all().delete()

    # 1. Buat Banners
    banner_images = ['0a9593c5-4717-4510-8005-5c045290fd41_kE70NR1.jpg', 'New_Arrival.png']
    media_banners_path = os.path.join(settings.MEDIA_ROOT, 'banners')
    for i, img_name in enumerate(banner_images):
        img_path = os.path.join(media_banners_path, img_name)
        if os.path.exists(img_path):
            banner = Banner.objects.create(
                title=f"Banner {i+1}",
                subtitle=f"Promo menarik untuk Banner {i+1}",
                link='/',
                order=i,
                is_active=True
            )
            with open(img_path, 'rb') as f:
                banner.image.save(img_name, File(f))
            print(f"Banner '{banner.title}' dibuat.")
        else:
            print(f"File banner tidak ditemukan: {img_path}")

    # 2. Buat Kategori
    categories = ['Sneakers', 'Running', 'Casual', 'Basketball']
    for cat_name in categories:
        Category.objects.create(name=cat_name)
        print(f"Kategori '{cat_name}' dibuat.")

    # 3. Buat Brand beserta logo
    brands_data = [
        {"name": "Nike", "logo": "nike_logo.webp"},
        {"name": "Adidas", "logo": "ABIBAS.jpeg"},
        {"name": "New Balance", "logo": "new_balance.webp"},
        {"name": "Puma", "logo": "puma.png"},
        {"name": "Converse", "logo": "Converse-logo.png"}
    ]
    media_brands_path = os.path.join(settings.MEDIA_ROOT, 'brands', 'logos')
    for bdata in brands_data:
        brand = Brand.objects.create(name=bdata["name"])
        logo_path = os.path.join(media_brands_path, bdata["logo"])
        if os.path.exists(logo_path):
            with open(logo_path, 'rb') as f:
                brand.logo.save(bdata["logo"], File(f))
        print(f"Brand '{brand.name}' dibuat dengan logo.")

    # 4. Buat 6 Produk beserta gambar masing-masing (tidak acak)
    products_data = [
        {
            "name": "Nike Dunk Low Retro",
            "brand": "Nike",
            "category": "Sneakers",
            "desc": "Nike Dunk Low Retro membawa kembali gaya klasik hoops 80-an.",
            "price": 1800000.00,
            "color": "black",
            "image": "NIKEDUNKLOWRETRO.avif"
        },
        {
            "name": "Adidas Samba OG",
            "brand": "Adidas",
            "category": "Casual",
            "desc": "Ikon street style yang tak lekang oleh waktu.",
            "price": 2100000.00,
            "color": "white",
            "image": "ADIDAS_SAMBA_OG.jpeg"
        },
        {
            "name": "New Balance 530",
            "brand": "New Balance",
            "category": "Running",
            "desc": "Siluet running retro klasik dari New Balance.",
            "price": 1700000.00,
            "color": "white",
            "image": "MR530.webp"
        },
        {
            "name": "Puma Speed Cat",
            "brand": "Puma",
            "category": "Casual",
            "desc": "Desain motorsport yang diadaptasi untuk jalanan.",
            "price": 1200000.00,
            "color": "black",
            "image": "PUMA_SPEED_CAT.jpeg"
        },
        {
            "name": "Converse Chuck 70",
            "brand": "Converse",
            "category": "Casual",
            "desc": "Sepatu kanvas legendaris yang nyaman dipakai seharian.",
            "price": 950000.00,
            "color": "black",
            "image": "chuck_70.webp"
        },
        {
            "name": "On Cloud Shoes",
            "brand": "Nike",
            "category": "Running",
            "desc": "Sepatu lari ringan dan nyaman seperti berjalan di atas awan.",
            "price": 2800000.00,
            "color": "grey",
            "image": "ON_CLOUD_SHOES.webp"
        }
    ]

    media_products_path = os.path.join(settings.MEDIA_ROOT, 'products', 'images')
    for pdata in products_data:
        p = Product.objects.create(
            name=pdata["name"],
            brand=Brand.objects.get(name=pdata["brand"]),
            category=Category.objects.get(name=pdata["category"]),
            description=pdata["desc"],
            price=pdata["price"],
            color=pdata["color"],
            condition='new',
            is_featured=True
        )
        
        # Buat ukuran dan stok
        ProductSize.objects.create(product=p, size='40', stock=5)
        ProductSize.objects.create(product=p, size='42', stock=10)
        
        # Set gambar
        img_path = os.path.join(media_products_path, pdata["image"])
        if os.path.exists(img_path):
            with open(img_path, 'rb') as f:
                ProductImage.objects.create(
                    product=p,
                    image=File(f, name=pdata["image"]),
                    is_primary=True
                )
            print(f"Produk '{p.name}' dibuat dengan gambar spesifik.")
        else:
            print(f"Gagal memuat gambar untuk {p.name}: {img_path}")

    print("Reseeding selesai! Semua data lama telah diganti dengan data baru.")


if __name__ == '__main__':
    run()
