from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, UserViewSet, ProjectMembershipViewSet

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('memberships', ProjectMembershipViewSet, basename='memberships')  # 🔥 ADD THIS
router.register('', ProjectViewSet, basename='projects')

urlpatterns = router.urls
