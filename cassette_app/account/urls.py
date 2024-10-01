from django.urls import path
from account.views import KakaoLoginView

urlpatterns = [
    path("kakao/callback", KakaoLoginView.as_view(), name="kakao_login"),
]
