from django.db import models


class Transaction(models.Model):
    TYPE_CHOICES = [
        ('TOP_UP', 'Top Up'),
        ('TRANSFER', 'Transfer'),
        ('PAYMENT', 'Payment'),
        ('WITHDRAW', 'Withdraw'),
    ]
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed'),
        ('CANCELLED', 'Cancelled'),
    ]

    sender_wallet = models.ForeignKey(
        'wallets.Wallet',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sent_transactions',
    )
    receiver_wallet = models.ForeignKey(
        'wallets.Wallet',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='received_transactions',
    )
    transaction_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    commission = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default='TJS')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.transaction_type} - {self.amount} {self.currency}'
