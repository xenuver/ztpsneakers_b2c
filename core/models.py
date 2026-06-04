from django.db import models

class FooterIcon(models.Model):
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to="footer_icons/")
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

class Notification(models.Model):
    user = models.ForeignKey('userauths.User', on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=255)
    message = models.TextField()
    link = models.CharField(max_length=255, blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.title}"

class StoreSetting(models.Model):
    name = models.CharField(max_length=255, default="ZTP Sneakers")
    logo = models.ImageField(upload_to="store/", blank=True, null=True)
    whatsapp_number = models.CharField(max_length=20, blank=True, null=True, help_text="Format: 62812xxx")
    instagram_url = models.URLField(blank=True, null=True)
    crisp_website_id = models.CharField(max_length=100, blank=True, null=True, help_text="ID Token dari Crisp Chat")

    class Meta:
        verbose_name = "Pengaturan Toko"
        verbose_name_plural = "Pengaturan Toko"

    def __str__(self):
        return "Pengaturan Toko"

    def save(self, *args, **kwargs):
        if not self.pk and StoreSetting.objects.exists():
            return
        return super(StoreSetting, self).save(*args, **kwargs)