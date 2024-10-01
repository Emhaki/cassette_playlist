import os, requests
from django.shortcuts import redirect, render
from account.serializers import KakaoLoginSerializer
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import KakaoLoginSerializer
from .models import PlyUser  # 사용자 모델
from dotenv import load_dotenv
import jwt

load_dotenv()

# 카카오 API 키
KAKAO_REST_API_KEY = os.getenv("KAKAO_REST_API_KEY")
client_id = os.getenv('KAKAO_SECRET')

# 카카오 토큰 요청 및 사용자 정보 URL
KAKAO_ACCESS_TOKEN_URL = 'https://kauth.kakao.com/oauth/token'
KAKAO_USER_INFO_URL = 'https://kapi.kakao.com/v2/user/me'

# 로그인 및 콜백 URL 설정 (카카오 Redirect URI와 일치해야 함)
KAKAO_REDIRECT_URI = 'http://223.130.130.103/account/kakao/callback/'
SECRET_KEY = os.getenv("SECRET_KEY")

def kakao_login(request):
    return redirect(f"https://kauth.kakao.com/oauth/authorize?client_id={KAKAO_REST_API_KEY}&redirect_uri={KAKAO_REDIRECT_URI}&response_type=code")

class KakaoCallbackView(APIView):
    def get(self, request):
        code = request.GET.get('code')

        if code is None:
            return Response({"error": "카카오 인증 코드가 없습니다."}, status=400)
        
        # code로 access token 요청
        token_request = requests.get(f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={KAKAO_REST_API_KEY}&redirect_uri={KAKAO_REDIRECT_URI}&code={code}")
        token_response_json = token_request.json()

        # 에러 발생 시 중단
        error = token_response_json.get("error", None)
        if error is not None:
            return Response({'error': 'Failed to get user info from Kakao.'}, status=status.HTTP_400_BAD_REQUEST)

        access_token = token_response_json.get("access_token")
        # access token으로 카카오톡 프로필 요청
        profile_request = requests.post(
            KAKAO_USER_INFO_URL,
            headers={"Authorization": f"Bearer {access_token}"},
        )

        profile_json = profile_request.json()

        kakao_account = profile_json.get('kakao_account')
        profile_image = kakao_account.get('profile', {}).get('profile_image_url', None)
        # email = kakao_account.get('email', None)
        nickname = kakao_account.get('profile', {}).get('nickname', None)

        user, created = PlyUser.objects.get_or_create(
            defaults={
                "nickname": nickname,
                "profile_image_url": f"{profile_image}",
            }
        #     id=f'kakao_{kakao_id}',  # PlyUser의 id 필드 사용
        #     defaults={
        #         'email': email,       # 카카오에서 받은 이메일
        #         'nickname': nickname, # 카카오에서 받은 닉네임
        # }
    )
        # JWT 토큰 발급
        token = jwt.encode({'id': user.id}, SECRET_KEY, algorithm='HS256')

        data = {
            'token': token,
            'user_id': user.id,
            'user_uuid': user.uuid,
            'nickname': nickname,
            'profile_image': user.profile_image_url,
            'created': created  # 새로 생성된 사용자인지 여부
        }

        return Response(data, status=status.HTTP_200_OK)




# class KakaoLoginView(APIView):
#     def post(self, request):
#         serializer = KakaoLoginSerializer(data=request.data)
#         if serializer.is_valid():
#             access_token = serializer.validated_data['access_token']
            
#             # 카카오 사용자 정보 요청
#             user_info_url =KAKAO_USER_INFO_URL
#             headers = {
#                 'Authorization': f'Bearer {access_token}',
#                 'Content-type': 'application/x-www-form-urlencoded; charset=utf-8'
#             }
#             response = requests.get(user_info_url, headers=headers)
#             user_info = response.json()

#             if response.status_code != 200:
#                 return Response({'error': 'Failed to get user info from Kakao.'}, status=status.HTTP_400_BAD_REQUEST)
            
#             # 카카오 ID를 이용하여 사용자 식별
#             kakao_id = user_info.get('id')
#             kakao_account = user_info.get('kakao_account')
#             email = kakao_account.get('email', None)
#             nickname = kakao_account.get('profile', {}).get('nickname', None)


#             user, created = PlyUser.objects.get_or_create(
#                 id=f'kakao_{kakao_id}',  # PlyUser의 id 필드 사용
#                 defaults={
#                     'email': email,       # 카카오에서 받은 이메일
#                     'nickname': nickname, # 카카오에서 받은 닉네임
#                 }
# )
#             # JWT 토큰 발급
#             token = jwt.encode({'id': user.id}, SECRET_KEY, algorithm='HS256')

#             return Response({
#                 'token': token,
#                 'user_id': user.id,
#                 'email': email,
#                 'nickname': nickname,
#                 'created': created  # 새로 생성된 사용자인지 여부
#             }, status=status.HTTP_200_OK)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

