from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from .models import Playlist, RecommendedSong
from .serializers import PlaylistSerializer, RecommendedSongSerializer

# 간단한 INDEX 페이지를 보여주는 뷰
class IndexView(APIView):
    def get(self, request):
        return Response({"message": "안녕하세요 퍼플리 서버입니다."})




class PlaylistDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer

class RecommendedSongListCreateView(generics.ListCreateAPIView):
    queryset = RecommendedSong.objects.all()
    serializer_class = RecommendedSongSerializer

class RecommendedSongDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RecommendedSong.objects.all()
    serializer_class = RecommendedSongSerializer
