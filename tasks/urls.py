from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, AttachmentViewSet, CommentViewSet
from .dashboard_views import DashboardStatsView

router = DefaultRouter()

# 🔥 REGISTER SPECIFIC ROUTES FIRST
router.register('comments', CommentViewSet, basename='comments')
router.register('attachments', AttachmentViewSet, basename='attachments')

# 🔥 REGISTER TASKS LAST
router.register('', TaskViewSet, basename='tasks')

urlpatterns = [
    path('dashboard/', DashboardStatsView.as_view()),
]

urlpatterns += router.urls
