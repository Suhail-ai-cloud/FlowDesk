from rest_framework.permissions import BasePermission
from projects.models import ProjectMembership


class IsTaskProjectMember(BasePermission):
    def has_object_permission(self, request, view, obj):
        return ProjectMembership.objects.filter(
            project=obj.project,
            user=request.user
        ).exists()
class IsAssignedOrOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        # Owner can do everything
        if obj.project.owner == request.user:
            return True

        # Assigned users can view/edit
        return obj.assigned_to.filter(id=request.user.id).exists()