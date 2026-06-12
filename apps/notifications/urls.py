from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.notifications.views import MarkNotificationAsReadAPIView, NotificationViewSet

router = DefaultRouter()
router.register('', NotificationViewSet, basename='notification')

urlpatterns = [
    path('<int:pk>/mark-as-read/', MarkNotificationAsReadAPIView.as_view(), name='notification-mark-read'),
    *router.urls,
]