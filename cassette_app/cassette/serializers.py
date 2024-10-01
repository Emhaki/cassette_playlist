from rest_framework import serializers
from .models import Playlist, RecommendedSong

class PlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ['id', 'user_id', 'name', 'created_at']

class RecommendedSongSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecommendedSong
        fields = ['playlist_id', 'user_name', 'singer', 'title', 'youtube_url', 'content', 'like', 'created_at']