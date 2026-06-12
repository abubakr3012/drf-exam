from rest_framework import serializers

from apps.wallets.models import BankCard, Wallet
from common.serializers import UserShortSerializer


class WalletSerializer(serializers.ModelSerializer):
    user = UserShortSerializer(read_only=True)
    balance = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    wallet_number = serializers.CharField(read_only=True)

    class Meta:
        model = Wallet
        fields = (
            'id', 'user', 'wallet_number', 'balance', 'currency',
            'status', 'created_at', 'updated_at',
        )
        read_only_fields = ('id', 'created_at', 'updated_at')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['balance'] = f'{instance.balance:.2f} {instance.currency}'
        return data


class BankCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankCard
        fields = (
            'id', 'user', 'card_holder', 'masked_pan', 'card_type',
            'expire_month', 'expire_year', 'status', 'created_at',
        )
        read_only_fields = ('id', 'created_at')
