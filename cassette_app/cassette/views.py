from django.forms import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, status
from account.models import PlyUser
from .models import Playlist, RecommendedPlaylist
from .serializers import PlaylistSerializer, RecommendedPlaylistSerializer

# 간단한 INDEX 페이지를 보여주는 뷰
class IndexView(APIView):
    def get(self, request):
        return Response({"message": "안녕하세요 퍼플리 서버입니다."})
    
class PlaylistCreateView(generics.CreateAPIView):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer

    # URL로 전달된 user_id 값을 이용해 Playlist를 생성하는 메서드
    def perform_create(self, serializer):
        user_uuid = self.kwargs.get('user_uuid')  # URL에서 user_id 가져오기

        # user_uuid가 실제로 존재하는지 확인
        try:
            user = PlyUser.objects.get(uuid=user_uuid)
        except PlyUser.DoesNotExist:
            raise ValidationError({"user_id": "Invalid user_id. User does not exist."})

        # 해당 유저와 연결된 플레이리스트 생성
        serializer.save(user_id=user)

class PlaylistDetailView(generics.RetrieveAPIView):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
    lookup_field = 'pk'

    def get(self, request, user_uuid, pk):
        # 해당 플레이리스트 가져오기
        # user_uuid로 PlyUser를 찾음
        try:
            user = PlyUser.objects.get(uuid=user_uuid)
        except PlyUser.DoesNotExist:
            raise ValidationError({"user_uuid": "Invalid user_uuid. User does not exist."})
        
        try:
            playlist = Playlist.objects.get(id=pk, user_id=user.id)
        except Playlist.DoesNotExist:
            return Response({"error": "Playlist not found"}, status=status.HTTP_404_NOT_FOUND)

        # Playlist 직렬화
        playlist_serializer = PlaylistSerializer(playlist)

        # 해당 플레이리스트에 연결된 추천받은 곡들 가져오기
        recommended_songs = RecommendedPlaylist.objects.filter(playlist_id=pk)
        recommended_songs_serializer = RecommendedPlaylistSerializer(recommended_songs, many=True)

        # Playlist와 그에 해당하는 추천받은 곡들 반환
        return Response({
            "playlist": playlist_serializer.data,
            "recommended_songs": recommended_songs_serializer.data
        }, status=status.HTTP_200_OK)

class RecommendedPlaylistCreateView(generics.CreateAPIView):
    queryset = RecommendedPlaylist.objects.all()
    serializer_class = RecommendedPlaylistSerializer

    # playlist_id와 user_uuid를 이용해 객체를 생성하는 메서드
    def perform_create(self, serializer):
        playlist_id = self.kwargs.get('playlist_id')  # URL에서 playlist_id 가져오기
        user_uuid = self.kwargs.get('user_uuid')  # URL에서 user_uuid 가져오기

        # user_uuid로 PlyUser를 찾음
        try:
            user = PlyUser.objects.get(uuid=user_uuid)
        except PlyUser.DoesNotExist:
            raise ValidationError({"user_uuid": "Invalid user_uuid. User does not exist."})

        # 해당 유저의 플레이리스트가 맞는지 확인
        try:
            playlist = Playlist.objects.get(id=playlist_id, user_id=user.id)
        except Playlist.DoesNotExist:
            raise ValidationError({"playlist_id": "Invalid playlist_id. Playlist does not belong to the user."})

        # playlist_id 값을 사용하여 RecommendedPlaylist 인스턴스를 생성
        serializer.save(playlist_id=playlist)

# 사용자의 모든 플레이리스트
class UserPlaylistsView(generics.ListAPIView):
    serializer_class = PlaylistSerializer

    # 유저의 모든 플레이리스트를 반환하는 메서드
    def get_queryset(self):
        user_uuid = self.kwargs['user_uuid']
        # user_uuid를 이용해 유저 객체를 찾음
        user = get_object_or_404(PlyUser, uuid=user_uuid)
        # 해당 유저의 모든 플레이리스트 반환
        return Playlist.objects.filter(user_id=user.id)

# 사용자에 대한 모든 플레이리스트에 대한 추천받은 뮤직카드
class PlaylistsWithRecommendationsByUserView(APIView):
    def get(self, request, user_uuid):
        
        # user_uuid로 PlyUser를 찾음
        try:
            user = PlyUser.objects.get(uuid=user_uuid)
        except PlyUser.DoesNotExist:
            raise ValidationError({"user_uuid": "Invalid user_uuid. User does not exist."})
        
        # 해당 user_id와 연결된 모든 Playlist 가져오기
        playlists = Playlist.objects.filter(user_id=user.id)

        # 플레이리스트가 없을 경우 처리
        if not playlists.exists():
            return Response({"error": "No playlists found for this user"}, status=status.HTTP_404_NOT_FOUND)

        # 프론트에서 정렬 방식을 받음 (쿼리 파라미터에서 'order' 값을 확인)
        order = request.query_params.get('order', 'latest')  # 기본값은 'latest'

        # 정렬 기준 설정
        if order == 'old':
            sort_order = 'created_at'  # 오래된 순 (오름차순)
        else:
            sort_order = '-created_at'  # 최신순 (내림차순)

        all_recommended_songs = []  # 전체 recommended_songs 리스트
        total_music_cards = 0  # 전체 뮤직카드 수를 계산하기 위한 변수

        for playlist in playlists:
            # 정렬 방식에 따라 추천곡을 가져오기
            recommended_songs_queryset = RecommendedPlaylist.objects.filter(playlist_id=playlist.id).order_by(sort_order)[:5]
            recommended_all_songs_queryset = RecommendedPlaylist.objects.filter(playlist_id=playlist.id)
            recommended_songs_count = recommended_all_songs_queryset.count()

            recommended_songs_serializer = RecommendedPlaylistSerializer(recommended_songs_queryset, many=True)

            all_recommended_songs.extend(recommended_songs_serializer.data)  # 각 플레이리스트의 추천곡들을 통합 리스트에 추가
            total_music_cards += recommended_songs_count  # 전체 뮤직카드 수 증가

        # 모든 recommended_songs 리스트 반환
        return Response({
            "recommended_songs": all_recommended_songs,  # 모든 추천곡 리스트
            "total_music_cards": total_music_cards  # 전체 뮤직카드 수
        }, status=status.HTTP_200_OK)


# 플레이리스트에 대한 모든 뮤직카드
class PlaylistWithRecommendationsDetailView(APIView):
    def get(self, request, user_id):
        # Playlist 데이터 가져오기
        try:
            playlist = Playlist.objects.get(user_id=user_id)
        except Playlist.DoesNotExist:
            return Response({"error": "Playlist not found"}, status=status.HTTP_404_NOT_FOUND)

        # Playlist 직렬화
        playlist_serializer = PlaylistSerializer(playlist)

        # RecommendedPlaylist 데이터 가져오기
        recommended_songs = RecommendedPlaylist.objects.filter(playlist_id__user_id=user_id)
        recommended_songs_serializer = RecommendedPlaylistSerializer(recommended_songs, many=True)

        # 두 직렬화된 데이터를 하나의 응답으로 반환
        return Response({
            "playlist": playlist_serializer.data,
            "recommended_songs": recommended_songs_serializer.data
        }, status=status.HTTP_200_OK)

class RecommendedPlaylistView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RecommendedPlaylistSerializer

    def get_queryset(self):
        user_uuid = self.kwargs['user_uuid']
        playlist_id = self.kwargs['playlist_id']
        
        # user_uuid로 PlyUser를 찾음
        try:
            user = PlyUser.objects.get(uuid=user_uuid)
        except PlyUser.DoesNotExist:
            raise ValidationError({"user_uuid": "Invalid user_uuid. User does not exist."})

        # 해당 user_id와 playlist_id에 해당하는 추천 노래 필터링
        return RecommendedPlaylist.objects.filter(playlist_id=playlist_id, playlist_id__user_id=user.id)

# 유저의 플레이리스트의 뮤직카드 단건 조회
class RecommendedPlaylistDetailView(generics.RetrieveAPIView):
    queryset = RecommendedPlaylist.objects.all()
    serializer_class = RecommendedPlaylistSerializer

    def get_object(self, request):
        user_uuid = self.kwargs.get('user_uuid')
        playlist_id = self.kwargs.get('playlist_id')
        recommended_song_id = self.kwargs.get('pk')

        # 유저 확인
        try:
            user = PlyUser.objects.get(uuid=user_uuid)
        except PlyUser.DoesNotExist:
            raise ValidationError({"user": "User not found"})

        # 해당 유저의 플레이리스트 확인
        try:
            playlist = Playlist.objects.get(id=playlist_id, user_id=user.id)
        except Playlist.DoesNotExist:
            raise ValidationError({"playlist": "Invalid playlist or user."})

        # 해당 플레이리스트에 속한 추천받은 노래 조회
        try:
            recommended_song = RecommendedPlaylist.objects.get(id=recommended_song_id, playlist_id=playlist.id)
            
            # 로그인한 유저와 조회된 유저가 일치하는 경우 is_read를 True로 변경
            if request.user == user:
                recommended_song.is_read = True
                recommended_song.save()
                
        except RecommendedPlaylist.DoesNotExist:
            raise ValidationError({"recommended_song": "Recommended song not found in this playlist."})

        return recommended_song

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object(request)  # request를 get_object에 전달
        serializer = self.get_serializer(instance)

        # 현재 URL을 추가한 데이터 반환
        current_url = request.build_absolute_uri()
        data = serializer.data
        data["current_url"] = current_url

        return Response(data)


