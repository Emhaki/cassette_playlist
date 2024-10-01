from django.urls import path
from account.views import KakaoCallbackView, kakao_login

urlpatterns = [
    path('kakao/login', kakao_login, name='kakao_login'),
    path('kakao/callback/', KakaoCallbackView.as_view(), name='kakao_callback'),
    # path('kakao/login/finish/', KakaoLogin.as_view(), name='kakao_login_todjango'),
]
