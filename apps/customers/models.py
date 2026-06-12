from django.contrib.auth.models import User
from django.db import models


class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    birth_date = models.DateField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    passport_number = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} - {self.phone_number}'
