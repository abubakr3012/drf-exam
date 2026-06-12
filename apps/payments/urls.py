from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.payments.views import (
    FavoritePaymentViewSet,
    PaymentListCreateView,
    ServiceProviderViewSet,
    payment_category_detail,
    payment_category_list_create,
)

router = DefaultRouter()
router.register('providers', ServiceProviderViewSet, basename='service-provider')
router.register('favorites', FavoritePaymentViewSet, basename='favorite-payment')

urlpatterns = [
    path('categories/', payment_category_list_create, name='payment-category-list'),
    path('categories/<int:pk>/', payment_category_detail, name='payment-category-detail'),
    path('', PaymentListCreateView.as_view(), name='payment-list-create'),
    *router.urls,
]
