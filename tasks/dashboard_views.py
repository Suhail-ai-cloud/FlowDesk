from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils.timezone import now
from .models import Task
from rest_framework_simplejwt.authentication import JWTAuthentication


class DashboardStatsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tasks = Task.objects.filter(project__members=request.user)

        total_tasks = tasks.count()
        completed_tasks = tasks.filter(status='COMPLETED').count()
        pending_tasks = tasks.exclude(status='COMPLETED').count()
        overdue_tasks = tasks.filter(
            due_date__lt=now().date(),
            status__in=['PENDING', 'IN_PROGRESS']
        ).count()

        completion_percentage = (
            (completed_tasks / total_tasks) * 100 if total_tasks else 0
        )

        return Response({
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "pending_tasks": pending_tasks,
            "overdue_tasks": overdue_tasks,
            "completion_percentage": round(completion_percentage, 2)
        })
