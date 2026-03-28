from django.tasks import task
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Task
from .serializers import TaskSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .permissions import IsTaskProjectMember,IsAssignedOrOwner
from .models import Attachment,Comment
from .serializers import AttachmentSerializer,CommentSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from .filters import TaskFilter
from rest_framework.decorators import action
from django.utils.timezone import now
from rest_framework import viewsets, status

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsAssignedOrOwner]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = TaskFilter
    search_fields = ['title', 'description']
    ordering_fields = ['due_date', 'created_at', 'priority']

    def get_queryset(self):
        user = self.request.user
        queryset = Task.objects.filter(project__members=user)

        # 🔥 FILTER BY PROJECT IF PROVIDED
        project_id = self.request.query_params.get("project")
        if project_id:
            queryset = queryset.filter(project_id=project_id)

        return queryset

    @action(detail=False, methods=['get'])
    def my_tasks(self, request):
        tasks = Task.objects.filter(assigned_to=request.user)
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def overdue(self, request):
        tasks = Task.objects.filter(
            assigned_to=request.user,
            due_date__lt=now(),
            status__in=['pending', 'in_progress']
        )
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)
    def perform_create(self, serializer):
        task = serializer.save()
        task._actor = self.request.user  # pass actor

    def perform_update(self, serializer):
        task = serializer.save()
        task._actor = self.request.user




class AttachmentViewSet(viewsets.ModelViewSet):
    serializer_class = AttachmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Attachment.objects.filter(
            task__project__members=self.request.user
        )

        task_id = self.request.query_params.get("task")
        if task_id:
            queryset = queryset.filter(task_id=task_id)

        return queryset

    def create(self, request, *args, **kwargs):
        file = request.FILES.get("file")
        task_id = request.data.get("task")

        attachment = Attachment.objects.create(
            task_id=task_id,
            file=file,
            uploaded_by=request.user
        )

        serializer = self.get_serializer(attachment)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

# class AttachmentViewSet(viewsets.ModelViewSet):
#     serializer_class = AttachmentSerializer
#     parser_classes = (MultiPartParser, FormParser)
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         user = self.request.user
#         queryset = Attachment.objects.filter(task__project__members=user)

#         # 🔥 Filter by task
#         task_id = self.request.query_params.get("task")
#         if task_id:
#             queryset = queryset.filter(task_id=task_id)

#         return queryset

#     def perform_create(self, serializer):
#         task = serializer.validated_data['task']
#         if not task.project.members.filter(id=self.request.user.id).exists():
#             raise PermissionDenied("You are not a member of this project")
#         serializer.save()




class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Comment.objects.filter(task__project__members=user)

        # 🔥 FILTER BY TASK
        task_id = self.request.query_params.get("task")
        if task_id:
            queryset = queryset.filter(task_id=task_id)

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
