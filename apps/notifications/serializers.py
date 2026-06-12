from rest_framework import serializers

from apps.notifications.models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = (
            'id', 'user', 'title', 'message', 'notification_type',
            'is_read', 'created_at',
        )
        read_only_fields = ('id', 'user', 'created_at')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['status_text'] = 'Хондашуда' if instance.is_read else 'Нав'
        return data
