from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from user.views import UserSignupView, UserDetailView

user_list = UserSignupView.as_view({'post': 'create', 'delete': 'destroy'})
user_detail = UserDetailView.as_view({
    'get': 'retrieve', 
    'patch': 'partial_update'
})

urlpatterns = [
    # 회원가입
    path('signup/', user_list, name='user_signup'),

    # 로그인
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    # 토큰 재발급
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # 내 정보 조회 및 수정
    path('me/', user_detail, name='user_detail'),
]
