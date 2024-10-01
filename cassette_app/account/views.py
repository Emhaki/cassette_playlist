import os, requests
from django.shortcuts import redirect, render
from cassette_app.account.serializers import KakaoLoginSerializer
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import KakaoLoginSerializer
from .models import PlyUser  # 사용자 모델
from dotenv import load_dotenv
import json
import jwt

load_dotenv()

# 카카오 API 키
KAKAO_REST_API_KEY = os.getenv("KAKAO_REST_API_KEY")

# 카카오 토큰 요청 및 사용자 정보 URL
KAKAO_ACCESS_TOKEN_URL = 'https://kauth.kakao.com/oauth/token'
KAKAO_USER_INFO_URL = 'https://kapi.kakao.com/v2/user/me'

# 로그인 및 콜백 URL 설정 (카카오 Redirect URI와 일치해야 함)
KAKAO_REDIRECT_URI = 'http://localhost:8000/kakao/callback/'
SECRET_KEY = os.getenv("SECRET_KEY")

class KakaoLoginView(APIView):
    def post(self, request):
        serializer = KakaoLoginSerializer(data=request.data)
        if serializer.is_valid():
            access_token = serializer.validated_data['access_token']
            
            # 카카오 사용자 정보 요청
            user_info_url =KAKAO_USER_INFO_URL
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-type': 'application/x-www-form-urlencoded; charset=utf-8'
            }
            response = requests.get(user_info_url, headers=headers)
            user_info = response.json()

            if response.status_code != 200:
                return Response({'error': 'Failed to get user info from Kakao.'}, status=status.HTTP_400_BAD_REQUEST)
            
            # 카카오 ID를 이용하여 사용자 식별
            kakao_id = user_info.get('id')
            kakao_account = user_info.get('kakao_account')
            email = kakao_account.get('email', None)
            nickname = kakao_account.get('profile', {}).get('nickname', None)

            # 기존 사용자 확인 또는 새 사용자 생성
            user, created = PlyUser.objects.get_or_create(
                username=f'kakao_{kakao_id}', # 랜덤으로 생성할지 고민해보기
                defaults={'email': email, 'first_name': nickname}
            )

            # JWT 토큰 발급
            token = jwt.encode({'id': user.id}, SECRET_KEY, algorithm='HS256')

            return Response({
                'token': token,
                'user_id': user.id,
                'email': email,
                'nickname': nickname,
                'created': created  # 새로 생성된 사용자인지 여부
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
