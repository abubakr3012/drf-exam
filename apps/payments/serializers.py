from decimal import Decimal

from rest_framework import serializers

from apps.payments.models import FavoritePayment, Payment, PaymentCategory, ServiceProvider


class PaymentCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentCategory
        fields = ('id', 'name', 'description', 'is_active', 'created_at')
        read_only_fields = ('id', 'created_at')


class ServiceProviderSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = ServiceProvider
        fields = (
            'id', 'category', 'category_name', 'name', 'account_mask',
            'min_amount', 'max_amount', 'commission_percent', 'is_active', 'created_at',
        )
        read_only_fields = ('id', 'created_at')


class PaymentSerializer(serializers.ModelSerializer):
    provider_name = serializers.CharField(source='provider.name', read_only=True)

    class Meta:
        model = Payment
        fields = (
            'id', 'user', 'wallet', 'provider', 'provider_name', 'account_number',
            'amount', 'commission', 'total_amount', 'status', 'transaction', 'created_at',
        )
        read_only_fields = (
            'id', 'user', 'commission', 'total_amount', 'status',
            'transaction', 'created_at',
        )


class PaymentCreateSerializer(serializers.Serializer):
    wallet_id = serializers.IntegerField()
    provider_id = serializers.IntegerField()
    account_number = serializers.CharField(max_length=50)
    amount = serializers.DecimalField(max_digits=12, decimal_places=2, min_value=Decimal('0.01'))


class FavoritePaymentSerializer(serializers.ModelSerializer):
    provider_name = serializers.CharField(source='provider.name', read_only=True)

    class Meta:
        model = FavoritePayment
        fields = ('id', 'user', 'provider', 'provider_name', 'title', 'account_number', 'created_at')
        read_only_fields = ('id', 'user', 'created_at')
