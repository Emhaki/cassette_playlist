from django.urls import path
from account.views import CurrentURLView, KakaoCallbackView, UpdateNicknameView, kakao_login

urlpatterns = [
    path('kakao/login', kakao_login, name='kakao_login'),
    path('kakao/callback/', KakaoCallbackView.as_view(), name='kakao_callback'),
    path('update-nickname/<str:uuid>/', UpdateNicknameView.as_view(), name='update-nickname'),
    path('current-url/', CurrentURLView.as_view(), name='current-url'),
    # path('kakao/logout/', KakaoLogoutView.as_view(), name='kakao-logout'),

    # path('kakao/login/finish/', KakaoLogin.as_view(), name='kakao_login_todjango'),
]
