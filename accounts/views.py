from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer, ChangePasswordSerializer,EmailTokenObtainPairSerializer,CreateUserSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer



User = get_user_model()



@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me(request):
    user = request.user
    return Response({
        "id": user.id,
        "username": user.username,
        "email": user.email,
    })
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        user = request.user
        if not user.check_password(request.data.get('old_password')):
            return Response({"error": "Wrong password"}, status=400)

        user.set_password(request.data.get('new_password'))
        user.save()
        return Response({"message": "Password updated"})


class CreateUserView(generics.CreateAPIView):

    serializer_class = CreateUserSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):

        if self.request.user.role != "OWNER":
            raise PermissionError("Only owner can create users")

        serializer.save(created_by=self.request.user)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_users(request):

    users = User.objects.filter(company=request.user.company)

    data = [
        {
            "id": u.id,
            "username": u.username,
            "email": u.email,
        }
        for u in users
    ]

    return Response(data)



@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def update_user(request, pk):

    try:
        user = User.objects.get(id=pk, company=request.user.company)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)

    if request.user.role != "OWNER":
        return Response({"error": "Only owner can update users"}, status=403)

    user.username = request.data.get("username", user.username)
    user.email = request.data.get("email", user.email)

    user.save()

    return Response({
        "message": "User updated successfully"
    })

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_user(request, pk):

    try:
        user = User.objects.get(id=pk, company=request.user.company)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)

    if request.user.role != "OWNER":
        return Response({"error": "Only owner can delete users"}, status=403)

    user.delete()

    return Response({
        "message": "User deleted"
    })