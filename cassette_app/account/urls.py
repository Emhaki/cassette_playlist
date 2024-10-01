from django.urls import path

from cassette_app.account.views import KakaoLoginView
from . import viewss

urlpatterns = [
    path("kakao/callback", KakaoLoginView.as_view(), name="kakao_login"),
]
