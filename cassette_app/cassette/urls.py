from django.urls import path
from cassette.views import PlaylistCreateView, PlaylistDetailView, PlaylistWithRecommendationsDetailView, PlaylistsWithRecommendationsByUserView, RecommendedPlaylistCreateView, RecommendedPlaylistDetailView

urlpatterns = [
    # path('<uuid:uuid>/', user_playlist, name='user_playlist'),  # <uuid:uuid>로 URL 패턴 처리
    path('playlists/create/<str:user_uuid>/', PlaylistCreateView.as_view(), name='playlist-create'),
    path('<str:user_uuid>/', PlaylistsWithRecommendationsByUserView.as_view(), name='user-playlist-with-recommendations'),
    path('playlists/<str:user_uuid>/<int:pk>/', PlaylistDetailView.as_view(), name='playlist-detail'),
    path('recommended-playlist/create/<str:user_uuid>/<int:playlist_id>/', RecommendedPlaylistCreateView.as_view(), name='recommended-playlist-create'),
    path('recommended-playlist/<str:user_uuid>/<int:playlist_id>/', RecommendedPlaylistDetailView.as_view(), name='recommended-playlist-detail'),
]