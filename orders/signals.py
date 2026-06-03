from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Order
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
                title = "Pesanan Dikirim"
                message = f"Pesanan {instance.order_number} telah dikirim via {instance.courier.upper()}. No Resi: {instance.tracking_number or '-'}"
            elif instance.status == 'completed':
                title = "Pesanan Selesai"
                message = f"Terima kasih! Pesanan {instance.order_number} telah selesai."
                
            if title and message:
                Notification.objects.create(
                    user=instance.user,
                    title=title,
                    message=message,
                    link=f"/pesanan/history/{instance.order_number}/"
                )
