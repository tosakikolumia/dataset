# api/views/public.py
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from api.models import Hospital
from api.serializers import HospitalSerializer

class PublicViewSet(viewsets.ViewSet):
    """
    专门给公众用的只读/搜索接口，不需要 ModelViewSet
    """
    authentication_classes = []  # 不需要认证
    permission_classes = [AllowAny] # 允许任何人访问

    # POST /api/public/search_hospital/
    @action(detail=False, methods=['post'])
    def search_hospital(self, request):
        # 获取前端传来的筛选条件
        district_id = request.data.get('district')
        level_id = request.data.get('level')
        name_keyword = request.data.get('name')

        # 构造查询
        qs = Hospital.objects.all()
        if district_id:
            qs = qs.filter(district_id=district_id)
        if level_id:
            qs = qs.filter(level_id=level_id)
        if name_keyword:
            qs = qs.filter(name__contains=name_keyword)

        serializer = HospitalSerializer(qs, many=True)
        return Response({
            "code": 0,
            "message": "success",
            "data": serializer.data
        })