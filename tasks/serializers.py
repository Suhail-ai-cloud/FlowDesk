from rest_framework import serializers
from .models import Task, Comment, Attachment


class TaskSerializer(serializers.ModelSerializer):
    assigned_users = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = '__all__'

    def get_assigned_users(self, obj):
        return [
            {"id": u.id, "name": u.username}
            for u in obj.assigned_to.all()
        ]


    def get_overdue(self, obj):
        return obj.is_overdue()

class AttachmentSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = Attachment
        fields = ["id", "task", "file", "file_url", "uploaded_by", "uploaded_at"]
        read_only_fields = ["uploaded_by", "uploaded_at"]

    def get_file_url(self, obj):
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(obj.file.url)
        
class CommentSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'task', 'user', 'user_name', 'text', 'created_at']
        read_only_fields = ['user']
