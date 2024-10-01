from rest_framework.response import Response
from rest_framework.views import APIView

# 간단한 INDEX 페이지를 보여주는 뷰
class IndexView(APIView):
    def get(self, request):
        return Response({"message": "안녕하세요 퍼플리 서버입니다."})
