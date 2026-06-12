from rest_framework.routers import DefaultRouter

from apps.wallets.views import BankCardViewSet, WalletViewSet

router = DefaultRouter()
router.register('', WalletViewSet, basename='wallet')
router.register('cards', BankCardViewSet, basename='bank-card')

urlpatterns = router.urls
