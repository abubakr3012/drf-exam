from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.notifications.filters import NotificationFilter
from apps.notifications.models import Notification
from apps.notifications.serializers import NotificationSerializer


class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = NotificationFilter
    http_method_names = ['get', 'head', 'options', 'delete']

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)


class MarkNotificationAsReadAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        notification = get_object_or_404(Notification, pk=pk, user=request.user)
        notification.is_read = True
        notification.save()
        return Response(NotificationSerializer(notification).data, status=status.HTTP_200_OK)
