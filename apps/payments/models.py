from django.contrib.auth.models import User
from django.db import models


class PaymentCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ServiceProvider(models.Model):
    category = models.ForeignKey(PaymentCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    account_mask = models.CharField(max_length=50, null=True, blank=True)
    min_amount = models.DecimalField(max_digits=12, decimal_places=2, default=1)
    max_amount = models.DecimalField(max_digits=12, decimal_places=2, default=10000)
    commission_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Payment(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed'),
        ('CANCELLED', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    wallet = models.ForeignKey('wallets.Wallet', on_delete=models.CASCADE)
    provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    commission = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    transaction = models.OneToOneField(
        'transactions.Transaction',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.provider.name} - {self.amount}'


class FavoritePayment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    account_number = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
