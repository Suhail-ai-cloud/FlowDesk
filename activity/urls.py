# activity\urls.py
from rest_framework.routers import DefaultRouter
from .views import NotificationViewSet,ActivityLogViewSet

router = DefaultRouter()
router.register('notifications', NotificationViewSet, basename='notifications')
router.register('logs', ActivityLogViewSet, basename='activity-logs')
urlpatterns = router.urls
