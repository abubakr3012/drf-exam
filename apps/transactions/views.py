from decimal import Decimal

from django.db import transaction as db_transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import SearchFilter
from django.db.models import Q
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.notifications.models import Notification
from apps.transactions.filters import TransactionFilter
from apps.transactions.models import Transaction
from apps.transactions.serializers import (
    TopUpSerializer,
    TransactionSerializer,
    TransferSerializer,
    WithdrawSerializer,
)
from apps.wallets.models import Wallet


class TransactionListView(ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = TransactionFilter
    search_fields = [
        'description',
        'sender_wallet__wallet_number',
        'receiver_wallet__wallet_number',
    ]

    def get_queryset(self):
        user = self.request.user
        return Transaction.objects.filter(
            Q(sender_wallet__user=user) | Q(receiver_wallet__user=user)
        ).distinct()


class TopUpAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @db_transaction.atomic
    def post(self, request):
        serializer = TopUpSerializer(data=request.data)
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

        amount = data['amount']
        wallet.balance += amount
        wallet.save()

        txn = Transaction.objects.create(
            receiver_wallet=wallet,
            transaction_type='TOP_UP',
            amount=amount,
            commission=Decimal('0'),
            total_amount=amount,
            currency=wallet.currency,
            status='SUCCESS',
            description=data.get('description', ''),
        )

        Notification.objects.create(
            user=request.user,
            title='Пуркунӣ',
            message=f'Ҳамёни шумо ба маблағи {amount} {wallet.currency} пур карда шуд.',
            notification_type='TRANSACTION',
        )

        return Response(TransactionSerializer(txn).data, status=status.HTTP_201_CREATED)


class TransferAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @db_transaction.atomic
    def post(self, request):
        serializer = TransferSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            sender_wallet = Wallet.objects.select_for_update().get(
                id=data['sender_wallet_id'], user=request.user,
            )
        except Wallet.DoesNotExist:
            return Response({'detail': 'Ҳамёни фиристанда ёфт нашуд.'}, status=status.HTTP_404_NOT_FOUND)

        if sender_wallet.status != 'ACTIVE':
            return Response({'detail': 'Ҳамёни фиристанда фаъол нест.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            receiver_wallet = Wallet.objects.select_for_update().get(
                wallet_number=data['receiver_wallet_number'],
            )
        except Wallet.DoesNotExist:
            return Response({'detail': 'Ҳамёни гиранда ёфт нашуд.'}, status=status.HTTP_404_NOT_FOUND)

        if receiver_wallet.status != 'ACTIVE':
            return Response({'detail': 'Ҳамёни гиранда фаъол нест.'}, status=status.HTTP_400_BAD_REQUEST)

        if sender_wallet.id == receiver_wallet.id:
            return Response({'detail': 'Интиқол ба ҳамёни худ имконнопазир аст.'}, status=status.HTTP_400_BAD_REQUEST)

        amount = data['amount']
        commission = data.get('commission', Decimal('0'))
        total_amount = amount + commission

        if sender_wallet.balance < total_amount:
            return Response({'detail': 'Маблағи кофӣ дар ҳамён нест.'}, status=status.HTTP_400_BAD_REQUEST)

        sender_wallet.balance -= total_amount
        sender_wallet.save()

        receiver_wallet.balance += amount
        receiver_wallet.save()

        txn = Transaction.objects.create(
            sender_wallet=sender_wallet,
            receiver_wallet=receiver_wallet,
            transaction_type='TRANSFER',
            amount=amount,
            commission=commission,
            total_amount=total_amount,
            currency=sender_wallet.currency,
            status='SUCCESS',
            description=data.get('description', ''),
        )

        Notification.objects.create(
            user=sender_wallet.user,
            title='Интиқол',
            message=f'Шумо {total_amount} {sender_wallet.currency} ба {receiver_wallet.wallet_number} интиқол додед.',
            notification_type='TRANSACTION',
        )
        Notification.objects.create(
            user=receiver_wallet.user,
            title='Интиқол',
            message=f'Шумо {amount} {receiver_wallet.currency} аз {sender_wallet.wallet_number} гирифтед.',
            notification_type='TRANSACTION',
        )

        return Response(TransactionSerializer(txn).data, status=status.HTTP_201_CREATED)


class WithdrawAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @db_transaction.atomic
    def post(self, request):
        serializer = WithdrawSerializer(data=request.data)
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

        amount = data['amount']
        if wallet.balance < amount:
            return Response({'detail': 'Маблағи кофӣ дар ҳамён нест.'}, status=status.HTTP_400_BAD_REQUEST)

        wallet.balance -= amount
        wallet.save()

        txn = Transaction.objects.create(
            sender_wallet=wallet,
            transaction_type='WITHDRAW',
            amount=amount,
            commission=Decimal('0'),
            total_amount=amount,
            currency=wallet.currency,
            status='SUCCESS',
            description=data.get('description', ''),
        )

        Notification.objects.create(
            user=request.user,
            title='Бароред',
            message=f'Аз ҳамёни шумо {amount} {wallet.currency} бароварда шуд.',
            notification_type='TRANSACTION',
        )

        return Response(TransactionSerializer(txn).data, status=status.HTTP_201_CREATED)
