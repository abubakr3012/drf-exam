import uuid

from django.contrib.auth.models import User
from django.db import models


class Wallet(models.Model):
    CURRENCY_CHOICES = [('TJS', 'TJS'), ('USD', 'USD'), ('RUB', 'RUB')]
    STATUS_CHOICES = [('ACTIVE', 'Active'), ('BLOCKED', 'Blocked'), ('CLOSED', 'Closed')]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    wallet_number = models.CharField(max_length=20, unique=True)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='TJS')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.wallet_number:
            self.wallet_number = uuid.uuid4().hex[:20].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.wallet_number} ({self.user.username})'


class BankCard(models.Model):
    CARD_TYPE_CHOICES = [
        ('VISA', 'Visa'),
        ('MASTERCARD', 'Mastercard'),
        ('KORTI_MILLI', 'Korti Milli'),
        ('OTHER', 'Other'),
    ]
    STATUS_CHOICES = [('ACTIVE', 'Active'), ('BLOCKED', 'Blocked'), ('EXPIRED', 'Expired')]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card_holder = models.CharField(max_length=100)
    masked_pan = models.CharField(max_length=19)
    card_type = models.CharField(max_length=20, choices=CARD_TYPE_CHOICES)
    expire_month = models.IntegerField()
    expire_year = models.IntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.masked_pan} ({self.card_holder})'
