from django.urls import path
from cassette.views import PlaylistCreateView, PlaylistDetailView, PlaylistWithRecommendationsDetailView, PlaylistsWithRecommendationsByUserView, RecommendedPlaylistCreateView, RecommendedPlaylistDetailView, RecommendedPlaylistView, UserPlaylistsView

urlpatterns = [
    path('playlists/create/<str:user_uuid>/', PlaylistCreateView.as_view(), name='playlist-create'),
    # 사용자의 모든 플레이리스트
    path('playlists/<str:user_uuid>/', UserPlaylistsView.as_view(), name='user-playlists'),
    # 사용자 모든 플레이리스트에 대한 모든 뮤직카드
    path('<str:user_uuid>/', PlaylistsWithRecommendationsByUserView.as_view(), name='user-playlist-with-recommendations'),
    # 플레이리스트에 대한 뮤직카드
    path('playlists/detail/<str:user_uuid>/<int:pk>/', PlaylistDetailView.as_view(), name='playlist-detail'),
    # 뮤직카드 생성
    path('recommended-playlist/create/<str:user_uuid>/<int:playlist_id>/', RecommendedPlaylistCreateView.as_view(), name='recommended-playlist-create'),
    # 플레이리스트에 대한 뮤직카드 조회
    path('recommended-playlist/<str:user_uuid>/<int:playlist_id>/', RecommendedPlaylistView.as_view(), name='recommended-playlist-list'),
    path('recommended-playlist/detail/<str:user_uuid>/<int:playlist_id>/<int:pk>/', RecommendedPlaylistDetailView.as_view(), name='recommended-playlist-detail'),
]