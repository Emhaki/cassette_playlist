from django.urls import path
from cassette_app.cassette.views import PlaylistDetailView, RecommendedSongDetailView, RecommendedSongListCreateView

urlpatterns = [
    # path('<uuid:uuid>/', user_playlist, name='user_playlist'),  # <uuid:uuid>로 URL 패턴 처리
    path('playlists/<str:pk>/', PlaylistDetailView.as_view(), name='playlist-detail'),
    path('recommended-songs/', RecommendedSongListCreateView.as_view(), name='recommended-song-list-create'),
    path('recommended-songs/<int:pk>/', RecommendedSongDetailView.as_view(), name='recommended-song-detail'),
]