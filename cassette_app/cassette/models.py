from django.db import models

class Playlist(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    user_id = models.CharField(max_length=255)
    playlist = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.playlist

class RecommendedSong(models.Model):
    playlist_id = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=255, null=True, blank=True)
    singer = models.CharField(max_length=255, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    youtube_url = models.CharField(max_length=255, null=True, blank=True)
    content = models.CharField(max_length=255, null=True, blank=True)
    like = models.CharField(max_length=255, null=True, blank=True)  # 좋아요를 숫자로 저장할 계획이라면 IntegerField로 변경 가능
    created_at = models.DateTimeField(auto_now_add=True)  # 레코드 생성 시 자동으로 현재 시간 저장

    def __str__(self):
        return self.title  # 객체 출력 시 노래 제목이 출력되도록 설정