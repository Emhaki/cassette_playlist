import os, requests
import random
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from cassette.models import Playlist

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
# KAKAO_REDIRECT_URI = 'http://223.130.130.103/account/kakao/callback/'
# KAKAO_REDIRECT_URI = 'http://127.0.0.1:8000/account/kakao/callback/'
KAKAO_REDIRECT_URI = 'http://www.perply.site/account/kakao/callback/'

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
        
        # 각 카테고리의 리스트
        genres = [
            "팝", "록", "재즈", "힙합", "EDM", "R&B", "국악", "트롯", "메탈", "레게", "펑크", "인디", "민요", "가요"
        ]
        actions = [
            "듣는", "즐기는", "감상하는", "부르는", "배우는", "연주하는", "작곡하는", "작사하는", 
            "노래하는", "공연하는", "열창하는", "에빠진", "연습하는", "녹음하는"
        ]
        animals = [
            "개", "곰", "닭", "판다", "여우", "토끼", "돼지", "오리", "사슴", "하마", "기린", 
            "치타", "거북", "상어", "사자", "악어", "염소", "오리", "수달", "참새", "제비", 
            "늑대", "펭귄", "자라", "물개", "표범", "타조", "노루", "산양", "불곰"
        ]
        # 중복되지 않는 닉네임을 찾을 때까지 반복
        while True:
            random_nickname = random.choice(genres) + random.choice(actions) + random.choice(animals)
            if not PlyUser.objects.filter(nickname=random_nickname).exists():
                break
        
        # 유저가 존재하는지 확인하고 없으면 생성
        user, created = PlyUser.objects.get_or_create(
            kakao_id=profile_json.get('id'),  # 카카오 id를 사용해서 고유한 유저 식별
            defaults={
                "nickname": random_nickname,
                "profile_image_url": f"{profile_image}",
            }
        )
        
        if not Playlist.objects.filter(user_id=user):
            # 5개의 기본 플레이리스트 생성
            playlist_titles = [
                "당신이 떠올리는 그 사람의 풍경, 이 노래로 표현할 수 있다면 어떤 곡일까요?",
                "당신의 마음속 이야기를 이 노래로 전할 수 있다면, 어떤 곡일까요?",
                "만약 이 노래가 그 사람을 위한 편지라면, 어떤 마음을 담고 싶나요?",
                "그 사람과 함께 듣고 싶은 노래가 있다면, 어떤 곡이 떠오르나요?",
                "당신이 전하고 싶은 마음, 이 노래로 대신할 수 있다면 어떤 곡일까요?"
            ]

            # 처음 회원가입 후 5개 플레이리스트 생성
            for title in playlist_titles:
                Playlist.objects.create(user_id=user, playlist_title=title)  # user 대신 user_id 사용

        data = {
            'token': access_token,
            'user_id': user.id,
            'user_uuid': user.uuid,
            'nickname': nickname,
            'profile_image': user.profile_image_url,
            'created': created  # 새로 생성된 사용자인지 여부
        }

        return Response(data, status=status.HTTP_200_OK)

class UpdateNicknameView(APIView):
    # permission_classes = [IsAuthenticated]  # 인증이 필요한 경우 사용

    def patch(self, request, uuid):
        # uuid로 사용자를 조회
        user = get_object_or_404(PlyUser, uuid=uuid)

        # request.data에서 닉네임 가져오기
        new_nickname = request.data.get("nickname")
        if not new_nickname:
            return Response({"error": "닉네임이 필요합니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        if PlyUser.objects.filter(nickname=new_nickname).exists():
            return Response({
            "error": "닉네임이 중복되었습니다.",
            "nickname": new_nickname
        }, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            # 닉네임 업데이트
            user.nickname = new_nickname
            user.save()

            # 응답 반환
            return Response({
                "message": "닉네임이 성공적으로 변경되었습니다.",
                "nickname": user.nickname
            }, status=status.HTTP_200_OK)


# class KakaoLogoutView(APIView):
#     def kakao_logout(request):
#         # REST_API_KEY = getattr(settings, 'KAKAO_REST_KEY')
#         # LOGOUT_REDIRECT_URI = getattr(settings, 'KAKAO_REDIRECT_URI')

#         # 로그아웃 
#         # headers = {"Authorization": f'Bearer {access_token}'}
#         logout_response = requests.post('https://kapi.kakao.com/v1/user/logout', headers=headers)
#         print(logout_response.json())
        
#         # 카카오계정과 함께 로그아웃
#         logout_response = requests.get(f'https://kauth.kakao.com/oauth/logout?client_id=${REST_API_KEY}&logout_redirect_uri=${LOGOUT_REDIRECT_URI}')




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

