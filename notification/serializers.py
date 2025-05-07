from rest_framework import serializers
from .models import NotificationTemplate, NotificationHistory


class NotificationTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationTemplate
        fields = [
            'id', 'title', 'body', 'notification_type',
            'template_code', 'is_active', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class NotificationHistorySerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source='sender.username', read_only=True)
    receiver_username = serializers.CharField(source='receiver.username', read_only=True)

    class Meta:
        model = NotificationHistory
        fields = [
            'id', 'notification_template', 'sender', 'receiver',
            'sender_username', 'receiver_username',
            'body', 'is_success', 'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'sender', 'body', 'is_success']
