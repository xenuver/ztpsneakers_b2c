"""
Email utilities untuk ZTP Sneakers.
Trigger:
  - send_order_confirmation_email: saat pesanan dibuat
  - send_order_shipped_email: saat status ganti ke shipped
  - send_order_completed_email: saat status ganti ke completed
  - send_invoice_email: saat admin/pembeli minta kirim invoice
"""
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def _get_from_email():
    return getattr(settings, 'DEFAULT_FROM_EMAIL', 'ZTP Sneakers <noreply@ztpsneakers.com>')

def send_order_confirmation_email(order):
    """
    Kirim email konfirmasi saat pesanan baru dibuat.
    """
    if not order.user or not order.user.email:
        return False
    try:
        subject = f"Pesanan #{order.order_number} Berhasil Dibuat — ZTP Sneakers"
        context = {
            'order': order,
            'customer_name': order.user.get_full_name() or order.user.email,
        }
        html_body = render_to_string('emails/order_confirmation.html', context)
        text_body = f"Pesanan #{order.order_number} berhasil dibuat. Total: Rp {order.total:,.0f}"

        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_body,
            from_email=_get_from_email(),
            to=[order.user.email],
        )
        msg.attach_alternative(html_body, "text/html")
        msg.send()
        logger.info(f"Order confirmation email sent for {order.order_number} to {order.user.email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send order confirmation email for {order.order_number}: {e}")
        return False


def send_order_shipped_email(order):
    """
    Kirim email notifikasi saat status pesanan berubah ke 'shipped'.
    """
    if not order.user or not order.user.email:
        return False
    try:
        subject = f"Pesanan #{order.order_number} Sudah Dikirim! — ZTP Sneakers"
        context = {
            'order': order,
            'customer_name': order.user.get_full_name() or order.user.email,
            'tracking_number': order.tracking_number or '-',
            'courier': order.courier.upper() if order.courier else '-',
        }
        html_body = render_to_string('emails/order_shipped.html', context)
        text_body = (
            f"Pesanan #{order.order_number} Anda sudah dikirim!\n"
            f"Kurir: {context['courier']}\n"
            f"No. Resi: {context['tracking_number']}"
        )

        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_body,
            from_email=_get_from_email(),
            to=[order.user.email],
        )
        msg.attach_alternative(html_body, "text/html")
        msg.send()
        logger.info(f"Shipped email sent for {order.order_number}")
        return True
    except Exception as e:
        logger.error(f"Failed to send shipped email for {order.order_number}: {e}")
        return False


def send_order_completed_email(order):
    """
    Kirim email notifikasi saat pesanan selesai / diterima.
    """
    if not order.user or not order.user.email:
        return False
    try:
        subject = f"Pesanan #{order.order_number} Selesai — Terima Kasih! 🎉"
        context = {
            'order': order,
            'customer_name': order.user.get_full_name() or order.user.email,
        }
        html_body = render_to_string('emails/order_completed.html', context)
        text_body = (
            f"Pesanan #{order.order_number} telah selesai.\n"
            f"Terima kasih sudah berbelanja di ZTP Sneakers!\n"
            f"Jangan lupa tulis ulasan Anda."
        )

        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_body,
            from_email=_get_from_email(),
            to=[order.user.email],
        )
        msg.attach_alternative(html_body, "text/html")
        msg.send()
        logger.info(f"Completed email sent for {order.order_number}")
        return True
    except Exception as e:
        logger.error(f"Failed to send completed email for {order.order_number}: {e}")
        return False


def send_invoice_email(order):
    """
    Kirim email invoice ke pembeli atas permintaan.
    """
    if not order.user or not order.user.email:
        return False
    try:
        subject = f"Invoice Pesanan #{order.order_number} — ZTP Sneakers"
        context = {
            'order': order,
            'customer_name': order.user.get_full_name() or order.user.email,
        }
        html_body = render_to_string('emails/invoice_email.html', context)
        text_body = f"Invoice untuk pesanan #{order.order_number}. Total: Rp {order.total:,.0f}"

        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_body,
            from_email=_get_from_email(),
            to=[order.user.email],
        )
        msg.attach_alternative(html_body, "text/html")
        msg.send()
        logger.info(f"Invoice email sent for {order.order_number} to {order.user.email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send invoice email for {order.order_number}: {e}")
        return False
