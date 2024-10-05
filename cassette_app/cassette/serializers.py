from rest_framework import serializers
from account.models import PlyUser
from .models import Playlist, RecommendedPlaylist


class PlyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlyUser
        fields = ['uuid']  # PlyUser 모델의 id와 uuid 필드 모두 포함

class PlaylistSerializer(serializers.ModelSerializer):
    user_id = user_uuid = serializers.SerializerMethodField()  # 유저의 id만 직렬화
    user_uuid = serializers.SerializerMethodField()  # 유저의 uuid만 직렬화

    class Meta:
        model = Playlist
        fields = ['id', 'user_id','user_uuid', 'playlist_title', 'playlist_title_other', 'created_at']  # user 필드로 PlyUser 직렬화, user_id 및 uuid 제외
        
    def get_user_id(self, obj):
            # user_id를 통해 PlyUser의 id만 반환
            return obj.user_id.id

    def get_user_uuid(self, obj):
            # user_id를 통해 PlyUser의 uuid만 반환
            return obj.user_id.uuid

class RecommendedPlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecommendedPlaylist
        fields = ['id','playlist_id', 'user_name', 'singer', 'title', 'youtube_url', 'content', 'like', 'is_read', 'created_at', 'color', 'albumart_url']  # color 필드 추가
        read_only_fields = ['created_at']  # created_at 필드는 자동으로 생성되므로 읽기 전용으로 설정
    
    def validate_content(self, value):
        # content 필드의 바이트 길이를 확인하여 250바이트 이하인지 체크
        if len(value.encode('utf-8')) >= 250:
            raise serializers.ValidationError("본문은 250byte를 초과할 수 없습니다.")
        return value