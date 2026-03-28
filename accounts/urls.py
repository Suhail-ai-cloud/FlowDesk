from django.urls import path
from .views import RegisterView, ChangePasswordView, me,CreateUserView,my_users,update_user, delete_user
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("login/", TokenObtainPairView.as_view()),
    path("token/refresh/", TokenRefreshView.as_view()),
    path("change-password/", ChangePasswordView.as_view()),
    path("create-user/", CreateUserView.as_view()),
    path("my-users/", my_users),
    path("me/", me),
    path("update-user/<int:pk>/", update_user),
path("delete-user/<int:pk>/", delete_user),
]