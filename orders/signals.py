from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Order, WarrantyClaim
from django.apps import apps

@receiver(pre_save, sender=Order)
def order_status_changed(sender, instance, **kwargs):
    if instance.pk:
        old_order = Order.objects.get(pk=instance.pk)
        if old_order.status != instance.status:
            Notification = apps.get_model('core', 'Notification')
            
            title = ""
            message = ""
            
            if instance.status == 'paid':
                title = "Pembayaran Berhasil"
                message = f"Pembayaran untuk pesanan {instance.order_number} telah berhasil."
            elif instance.status == 'processing':
                title = "Pesanan Diproses"
                message = f"Pesanan {instance.order_number} sedang kami siapkan."
            elif instance.status == 'shipped':
                courier = instance.courier.upper() if instance.courier else '-'
                resi = instance.tracking_number or '-'
                title = "Pesanan Dikirim 📦"
                message = f"Pesanan {instance.order_number} telah dikirim via {courier}. No Resi: {resi}"
            elif instance.status == 'completed':
                title = "Pesanan Selesai ⭐"
                message = f"Terima kasih! Pesanan {instance.order_number} telah selesai. Yuk, berikan ulasanmu!"
            elif instance.status == 'cancelled':
                title = "Pesanan Dibatalkan"
                message = f"Pesanan {instance.order_number} telah dibatalkan."
                
            if title and message:
                from django.urls import reverse
                Notification.objects.create(
                    user=instance.user,
                    title=title,
                    message=message,
                    link=reverse('orders:order_detail', kwargs={'order_number': instance.order_number})
                )
            
            # Voucher loyalitas: setelah 5 transaksi selesai, beri voucher 20%
            if instance.status == 'completed' and instance.user:
                completed_count = Order.objects.filter(
                    user=instance.user, status='completed'
                ).count() + 1  # +1 karena instance belum tersimpan
                
                if completed_count == 5:
                    from .models import Voucher
                    from django.utils import timezone
                    from datetime import timedelta
                    import uuid
                    
                    # Cek apakah sudah pernah dapat voucher loyalty
                    existing_loyalty = Voucher.objects.filter(
                        user=instance.user,
                        code__startswith='LOYAL-',
                        is_used=False
                    ).exists()
                    
                    if not existing_loyalty:
                        voucher_code = f"LOYAL-{uuid.uuid4().hex[:8].upper()}"
                        Voucher.objects.create(
                            code=voucher_code,
                            discount_type='percentage',
                            discount_value=20,
                            max_discount=150000,
                            min_purchase=100000,
                            valid_from=timezone.now(),
                            valid_to=timezone.now() + timedelta(days=60),
                            is_active=True,
                            user=instance.user,
                        )
                        
                        Notification.objects.create(
                            user=instance.user,
                            title="Voucher Loyalitas 🎉",
                            message=f"Selamat! Kamu telah menyelesaikan 5 transaksi. Dapatkan voucher diskon 20% (maks Rp 150.000) dengan kode {voucher_code}!",
                            link="/"
                        )


@receiver(pre_save, sender=WarrantyClaim)
def warranty_status_changed(sender, instance, **kwargs):
    """Notifikasi in-app saat status klaim garansi berubah."""
    if instance.pk:
        try:
            old_claim = WarrantyClaim.objects.get(pk=instance.pk)
            if old_claim.status != instance.status:
                Notification = apps.get_model('core', 'Notification')
                
                title = ""
                message = ""
                
                if instance.status == 'approved':
                    title = "Klaim Garansi Disetujui ✅"
                    message = f"Klaim garansi untuk {instance.order_item.product_name} telah disetujui dan sedang diproses."
                elif instance.status == 'rejected':
                    title = "Klaim Garansi Ditolak"
                    message = f"Klaim garansi untuk {instance.order_item.product_name} ditolak. Lihat catatan dari admin."
                elif instance.status == 'resolved':
                    title = "Klaim Garansi Selesai ✅"
                    message = f"Klaim garansi untuk {instance.order_item.product_name} telah diselesaikan."
                
                if title and message:
                    Notification.objects.create(
                        user=instance.user,
                        title=title,
                        message=message,
                        link=f"/orders/garansi/{instance.pk}/"
                    )
        except WarrantyClaim.DoesNotExist:
            pass

from django.db.models.signals import post_save

@receiver(post_save, sender=WarrantyClaim)
def warranty_created(sender, instance, created, **kwargs):
    if created:
        Notification = apps.get_model('core', 'Notification')
        from django.urls import reverse
        Notification.objects.create(
            user=instance.user,
            title="Klaim Garansi Diterima 🛡️",
            message=f"Laporan garansi untuk {instance.order_item.product_name} telah kami terima dan akan segera ditinjau.",
            link=reverse('orders:warranty_tracking', kwargs={'claim_id': instance.pk})
        )

from django.contrib.auth.signals import user_logged_in

@receiver(user_logged_in)
def merge_cart_on_login(sender, request, user, **kwargs):
    """Merge guest cart ke user cart saat login."""
    from orders.utils import merge_guest_cart
    merge_guest_cart(request, user)
