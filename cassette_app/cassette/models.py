from django.db import models
from account.models import PlyUser

class Playlist(models.Model):
    user_id = models.ForeignKey(PlyUser, on_delete=models.CASCADE)  # ForeignKey to PlyUser's id (default primary key)
    playlist_title = models.CharField(max_length=255, null=True, blank=True)
    playlist_title_other = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # def __int__(self):
    #     return self.user_id

class RecommendedPlaylist(models.Model):
    COLOR_CHOICES = [
        ('red', 'Red'),
        ('blue', 'Blue'),
        ('skyblue', 'Skyblue'),
        ('cyan', 'Cyan'),
        ('yellow', 'Yellow'),
        ('purple', 'Purple'),
        ('green', 'Green'),
        ('pink', 'Pink'),
    ]
    
    playlist_id = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=255, null=True, blank=True)
    singer = models.CharField(max_length=255, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    youtube_url = models.CharField(max_length=255, null=True, blank=True)
    content = models.CharField(max_length=255, null=True, blank=True)
    like = models.IntegerField(null=True, blank=True)  # 좋아요를 숫자로 저장할 계획이라면 IntegerField로 변경 가능
    color = models.CharField(max_length=10, choices=COLOR_CHOICES, default='purple')
    albumart_url = models.CharField(max_length=255, null=True, blank=True)
    is_read = models.BooleanField(default=False)  # 기본값은 False로 설정하여 읽지 않음 상태
    created_at = models.DateTimeField(auto_now_add=True)  # 레코드 생성 시 자동으로 현재 시간 저장
    
    def __str__(self):
        return self.title  # 객체 출력 시 노래 제목이 출력되도록 설정