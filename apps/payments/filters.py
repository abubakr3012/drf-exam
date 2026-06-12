import django_filters

from apps.payments.models import Payment, ServiceProvider


class PaymentFilter(django_filters.FilterSet):
    class Meta:
        model = Payment
        fields = ['status', 'provider', 'wallet']


class ProviderFilter(django_filters.FilterSet):
    class Meta:
        model = ServiceProvider
        fields = ['category', 'is_active']
