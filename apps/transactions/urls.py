from django.urls import path

from apps.transactions.views import (
    TopUpAPIView,
    TransactionListView,
    TransferAPIView,
    WithdrawAPIView,
)

urlpatterns = [
    path('', TransactionListView.as_view(), name='transaction-list'),
    path('top-up/', TopUpAPIView.as_view(), name='transaction-top-up'),
    path('transfer/', TransferAPIView.as_view(), name='transaction-transfer'),
    path('withdraw/', WithdrawAPIView.as_view(), name='transaction-withdraw'),
]