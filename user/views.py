from rest_framework import viewsets, mixins, permissions, status
from rest_framework.response import Response
from .serializers import UserSignupSerializer, UserDetailSerializer, UserUpdateSerializer
from .models import User, UserToken
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.utils import timezone

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

class UserLoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'error': 'Email and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        # 이메일, 비밀번호로 유저 인증
        user = authenticate(request, email=email, password=password)
        if user is None:
            return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

        # 기존 UserToken 확인
        try:
            user_token = UserToken.objects.get(user=user)
            refresh = RefreshToken(user_token.refresh_token)
            refresh.check_exp()  # 만료 여부 확인
            refresh_token = str(refresh)
        except (UserToken.DoesNotExist, TokenError):
            # 없거나 만료됐으면 새로 생성
            refresh = RefreshToken.for_user(user)
            refresh_token = str(refresh)

        # access token 발급
        access_token = str(refresh.access_token)

                # UserToken 객체 생성 및 만료시간 설정
        user_token, created = UserToken.objects.update_or_create(
            user=user,
            defaults={
                'access_token': access_token,
                'refresh_token': str(refresh),
            }
        )
        user_token.set_expired_at()  # 만료시간을 6개월 뒤로 설정
        user_token.save()

        # UserToken 테이블에 저장 또는 업데이트
        UserToken.objects.update_or_create(
            user=user,
            defaults={
                'access_token': access_token,
                'refresh_token': refresh_token,
            }
        )

        # 마지막 로그인 시간 업데이트
        user.last_login = timezone.now()
        user.save()

        return Response({
            'access_token': access_token,
            'refresh_token': refresh_token,
        }, status=status.HTTP_200_OK)