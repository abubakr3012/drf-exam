from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated

from apps.wallets.filters import CardFilter
from apps.wallets.models import BankCard, Wallet
from apps.wallets.serializers import BankCardSerializer, WalletSerializer


class WalletViewSet(viewsets.ModelViewSet):
    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Wallet.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BankCardViewSet(viewsets.ModelViewSet):
    serializer_class = BankCardSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = CardFilter
    search_fields = ['masked_pan', 'card_holder', 'card_type']

    def get_queryset(self):
        return BankCard.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
