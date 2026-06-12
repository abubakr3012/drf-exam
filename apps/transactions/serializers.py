from decimal import Decimal

from rest_framework import serializers

from apps.transactions.models import Transaction
from apps.wallets.serializers import WalletSerializer

TYPE_TAJIK = {
    'TOP_UP': 'Пуркунӣ',
    'TRANSFER': 'Интиқол',
    'PAYMENT': 'Пардохт',
    'WITHDRAW': 'Бароред',
}

STATUS_TAJIK = {
    'PENDING': 'Дар интизор',
    'SUCCESS': 'Муваффақ',
    'FAILED': 'Ноком',
    'CANCELLED': 'Бекоршуда',
}


class TransactionSerializer(serializers.ModelSerializer):
    sender_wallet = WalletSerializer(read_only=True)
    receiver_wallet = WalletSerializer(read_only=True)

    class Meta:
        model = Transaction
        fields = (
            'id', 'sender_wallet', 'receiver_wallet', 'transaction_type',
            'amount', 'commission', 'total_amount', 'currency', 'status',
            'description', 'created_at', 'updated_at',
        )
        read_only_fields = fields

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['transaction_type'] = TYPE_TAJIK.get(instance.transaction_type, instance.transaction_type)
        data['status'] = STATUS_TAJIK.get(instance.status, instance.status)
        return data


class TopUpSerializer(serializers.Serializer):
    wallet_id = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=12, decimal_places=2, min_value=Decimal('0.01'))
    description = serializers.CharField(required=False, allow_blank=True, default='')


class TransferSerializer(serializers.Serializer):
    sender_wallet_id = serializers.IntegerField()
    receiver_wallet_number = serializers.CharField(max_length=20)
    amount = serializers.DecimalField(max_digits=12, decimal_places=2, min_value=Decimal('0.01'))
    commission = serializers.DecimalField(
        max_digits=12, decimal_places=2, min_value=Decimal('0'), default=Decimal('0'),
    )
    description = serializers.CharField(required=False, allow_blank=True, default='')


class WithdrawSerializer(serializers.Serializer):
    wallet_id = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=12, decimal_places=2, min_value=Decimal('0.01'))
    description = serializers.CharField(required=False, allow_blank=True, default='')
