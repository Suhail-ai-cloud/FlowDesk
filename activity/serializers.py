from rest_framework import serializers
from .models import Notification,ActivityLog

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'message', 'is_read', 'user', 'id']
        read_only_fields = ['user']





class ActivityLogSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = ActivityLog
        fields = ['id', 'task', 'username', 'action', 'timestamp']
