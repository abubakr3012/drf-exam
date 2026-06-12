from rest_framework.routers import DefaultRouter

from apps.customers.views import CustomerProfileViewSet

router = DefaultRouter()
router.register('profiles', CustomerProfileViewSet, basename='customer-profile')

urlpatterns = router.urls
