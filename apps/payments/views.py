from decimal import Decimal

from django.db import transaction as db_transaction
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.notifications.models import Notification
from apps.payments.filters import PaymentFilter, ProviderFilter
from apps.payments.models import FavoritePayment, Payment, PaymentCategory, ServiceProvider
from apps.payments.serializers import (
    FavoritePaymentSerializer,
    PaymentCategorySerializer,
    PaymentCreateSerializer,
    PaymentSerializer,
    ServiceProviderSerializer,
)
from apps.transactions.models import Transaction
from apps.wallets.models import Wallet


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def payment_category_list_create(request):
    if request.method == 'GET':
        categories = PaymentCategory.objects.all()
        serializer = PaymentCategorySerializer(categories, many=True)
        return Response(serializer.data)

    serializer = PaymentCategorySerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def payment_category_detail(request, pk):
    category = get_object_or_404(PaymentCategory, pk=pk)

    if request.method == 'GET':
        return Response(PaymentCategorySerializer(category).data)

    if request.method == 'DELETE':
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    partial = request.method == 'PATCH'
    serializer = PaymentCategorySerializer(category, data=request.data, partial=partial)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


class ServiceProviderViewSet(viewsets.ModelViewSet):
    serializer_class = ServiceProviderSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = ProviderFilter
    search_fields = ['name', 'category__name']
    queryset = ServiceProvider.objects.all()


class FavoritePaymentViewSet(viewsets.ModelViewSet):
    serializer_class = FavoritePaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FavoritePayment.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PaymentListCreateView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = PaymentFilter
    search_fields = ['account_number', 'provider__name']

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PaymentCreateSerializer
        return PaymentSerializer

    @db_transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = PaymentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            wallet = Wallet.objects.select_for_update().get(
                id=data['wallet_id'], user=request.user,
            )
        except Wallet.DoesNotExist:
            return Response({'detail': 'Ҳамёни молиявӣ ёфт нашуд.'}, status=status.HTTP_404_NOT_FOUND)

        if wallet.status != 'ACTIVE':
            return Response({'detail': 'Ҳамёни молиявӣ фаъол нест.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            provider = ServiceProvider.objects.get(id=data['provider_id'])
        except ServiceProvider.DoesNotExist:
            return Response({'detail': 'Провайдер ёфт нашуд.'}, status=status.HTTP_404_NOT_FOUND)

        if not provider.is_active:
            return Response({'detail': 'Провайдер фаъол нест.'}, status=status.HTTP_400_BAD_REQUEST)

        amount = data['amount']
        if amount < provider.min_amount:
            return Response(
                {'detail': f'Маблағи минималӣ {provider.min_amount} аст.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if amount > provider.max_amount:
            return Response(
                {'detail': f'Маблағи максималӣ {provider.max_amount} аст.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        commission = amount * provider.commission_percent / Decimal('100')
        total_amount = amount + commission

        if wallet.balance < total_amount:
            return Response({'detail': 'Маблағи кофӣ дар ҳамён нест.'}, status=status.HTTP_400_BAD_REQUEST)

        wallet.balance -= total_amount
        wallet.save()

        txn = Transaction.objects.create(
            sender_wallet=wallet,
            transaction_type='PAYMENT',
            amount=amount,
            commission=commission,
            total_amount=total_amount,
            currency=wallet.currency,
            status='SUCCESS',
            description=f'Пардохт ба {provider.name}',
        )

        payment = Payment.objects.create(
            user=request.user,
            wallet=wallet,
            provider=provider,
            account_number=data['account_number'],
            amount=amount,
            commission=commission,
            total_amount=total_amount,
            status='SUCCESS',
            transaction=txn,
        )

        Notification.objects.create(
            user=request.user,
            title='Пардохт',
            message=f'Пардохти {total_amount} {wallet.currency} ба {provider.name} муваффақ шуд.',
            notification_type='PAYMENT',
        )

        return Response(PaymentSerializer(payment).data, status=status.HTTP_201_CREATED)
