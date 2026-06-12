from rest_framework import serializers

from apps.customers.models import CustomerProfile
from common.serializers import UserShortSerializer


class CustomerProfileSerializer(serializers.ModelSerializer):
    user = UserShortSerializer(read_only=True)

    class Meta:
        model = CustomerProfile
        fields = (
            'id', 'user', 'phone_number', 'birth_date', 'address',
            'passport_number', 'created_at', 'updated_at',
        )
        read_only_fields = ('id', 'created_at', 'updated_at')
