from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

urlpatterns = [
    # 회원가입
    path('signup/', views.UserSignupView.as_view(), name='user_signup'),

    # 로그인 (Access, Refresh Token 발급)
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    # 토큰 (Refresh Token 사용해서 Access 재발급)
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # 내 정보 조회
    path('me/', views.UserMeView.as_view(), name='user_me'),
]
