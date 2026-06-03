from django.db import models

class FooterIcon(models.Model):
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to="footer_icons/")
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title