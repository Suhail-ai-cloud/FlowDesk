from rest_framework import serializers
from .models import Project, ProjectMembership
from django.contrib.auth import get_user_model

User = get_user_model()


class ProjectMembershipSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = ProjectMembership
        fields = ["id", "user", "username", "project", "role"]


class ProjectSerializer(serializers.ModelSerializer):
    members = serializers.SerializerMethodField()
    completion_percentage = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = "__all__"
        read_only_fields = ["owner", "company", "members", "is_archived", "created_at"]

    def get_completion_percentage(self, obj):
        total = obj.task_set.count()
        completed = obj.task_set.filter(status="COMPLETED").count()
        return (completed / total * 100) if total else 0

    def get_members(self, obj):
        memberships = ProjectMembership.objects.filter(project=obj).select_related("user")

        return [
            {
                "id": m.user.id,
                "name": m.user.username
            }
            for m in memberships
        ]