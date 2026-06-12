import django_filters

from apps.transactions.models import Transaction


class TransactionFilter(django_filters.FilterSet):
    class Meta:
        model = Transaction
        fields = [
            'status',
            'transaction_type',
            'currency',
            'sender_wallet',
            'receiver_wallet',
        ]
