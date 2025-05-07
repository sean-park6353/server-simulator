from rest_framework import viewsets, mixins, permissions, status
from rest_framework.response import Response
from .serializers import UserSignupSerializer, UserDetailSerializer, UserUpdateSerializer
from .models import User

class UserSignupView(mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSignupSerializer
    permission_classes = [permissions.AllowAny]

class UserDetailView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UserDetailSerializer
        if self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        return super().get_serializer_class()

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        user.is_active = False  # 실제 삭제 대신 비활성화
        user.save()
        return Response({"detail": "회원 탈퇴 처리되었습니다."}, status=status.HTTP_204_NO_CONTENT)
