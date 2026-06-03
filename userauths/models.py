from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100)
    
    # Kamu bisa menambahkan field ekstra di sini nantinya
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    
    USERNAME_FIELD = "email" # Mengatur email sebagai acuan login
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username