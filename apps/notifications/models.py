from django.contrib.auth.models import User
from django.db import models


class Notification(models.Model):
    TYPE_CHOICES = [
        ('TRANSACTION', 'Transaction'),
        ('PAYMENT', 'Payment'),
        ('SYSTEM', 'System'),
        ('CARD', 'Card'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title} - {self.user.username}'
