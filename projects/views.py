from rest_framework import viewsets
from .models import Project, ProjectMembership
from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer
from rest_framework.exceptions import ValidationError
from .serializers import ProjectSerializer,ProjectMembershipSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsProjectMember, IsProjectOwner
from rest_framework.viewsets import ReadOnlyModelViewSet



User = get_user_model()


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(company=self.request.user.company)

class ProjectViewSet(viewsets.ModelViewSet):

    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return Project.objects.filter(
            company=self.request.user.company
        )

    def perform_create(self, serializer):

        project = serializer.save(
            owner=self.request.user,
            company=self.request.user.company
        )

        ProjectMembership.objects.create(
            user=self.request.user,
            project=project,
            role="OWNER"
        )

    def get_permissions(self):

        if self.action in ["update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsProjectOwner()]

        elif self.action in ["retrieve"]:
            return [IsAuthenticated(), IsProjectMember()]

        return super().get_permissions()
    

class ProjectMembershipViewSet(viewsets.ModelViewSet):

    serializer_class = ProjectMembershipSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        if self.action == "list":
            project_id = self.request.query_params.get("project")

            return ProjectMembership.objects.filter(
                project_id=project_id
            )

        return ProjectMembership.objects.all()

    def perform_create(self, serializer):

        user = serializer.validated_data["user"]
        project = serializer.validated_data["project"]

        if ProjectMembership.objects.filter(user=user, project=project).exists():
            raise ValidationError("User already in project")

        serializer.save()