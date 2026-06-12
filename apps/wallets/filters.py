import django_filters

from apps.wallets.models import BankCard


class CardFilter(django_filters.FilterSet):
    class Meta:
        model = BankCard
        fields = ['status', 'card_type']
