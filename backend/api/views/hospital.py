from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from api.permission import IsCityAdmin, IsHospitalAdmin, IsCityOrHospitalAdmin,ReadOnly
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
# 引入我们定义好的模型和序列化器
from api.models import (
    Hospital, HospitalLevel, HospitalDepartment,District ,
    HospitalServiceScore, EmergencyEvent, HospitalEvent
)
from api.serializers import (
    HospitalSerializer, HospitalLevelSerializer,DistrictSerializer ,
    HospitalDepartmentSerializer, HospitalServiceScoreSerializer,
    EmergencyEventSerializer
)


# 🏥 2. 医院等级 (改为 ModelViewSet 以支持 POST)
class HospitalLevelViewSet(viewsets.ModelViewSet):

    """
    医院等级视图集
    继承自ModelViewSet，提供完整的CRUD操作
    """
    queryset = HospitalLevel.objects.all()  # 获取所有医院等级数据
    serializer_class = HospitalLevelSerializer
    # 只有市政能增删改，其他人(包括居民)只能看
    permission_classes = [IsCityAdmin | ReadOnly]

# --- 2. 医院核心视图 ---
# 🏥 1. 医院基础信息
class HospitalViewSet(viewsets.ModelViewSet):
    queryset = Hospital.objects.all()
    serializer_class = HospitalSerializer

    def get_permissions(self):
        # POST(创建医院): 只有市政
        if self.action == 'create':
            return [IsCityAdmin()]
        # PATCH/PUT(修改): 市政 或 本院管理员
        elif self.action in ['update', 'partial_update']:
            return [(IsCityAdmin | IsHospitalAdmin)()]
        # DELETE: 只有市政
        elif self.action == 'destroy':
            return [IsCityAdmin()]
        return [permissions.AllowAny()]  # GET 所有人可见

    # 【自定义功能 1】: 获取某医院的所有科室
    # URL: GET /api/hospitals/{id}/departments/
    @action(detail=True, methods=['get'])
    def departments(self, request, pk=None):
        hospital = self.get_object()  # 获取当前医院对象
        # 查询中间表
        relations = HospitalDepartment.objects.filter(hospital=hospital)
        serializer = HospitalDepartmentSerializer(relations, many=True)

        # 返回符合 qwen.md 定义的格式
        return Response({
            "code": 0,
            "message": "success",
            "data": serializer.data
        })

    # 【自定义功能 2】: 获取某医院的评分
    # URL: GET /api/hospitals/{id}/scores/
    @action(detail=True, methods=['get'])
    def scores(self, request, pk=None):
        hospital = self.get_object()
        scores = HospitalServiceScore.objects.filter(hospital=hospital).order_by('-last_inspection_date')
        serializer = HospitalServiceScoreSerializer(scores, many=True)
        return Response({
            "code": 0,
            "message": "success",
            "data": serializer.data
        })

    # 【自定义功能 3】: 获取某医院参与的突发事件
    # URL: GET /api/hospitals/{id}/events/
    @action(detail=True, methods=['get'])
    def events(self, request, pk=None):
        hospital = self.get_object()
        # 通过多对多关系反向查询
        # 注意: 这里的查询逻辑稍微复杂一点，我们查 HospitalEvent 中间表
        hospital_events = HospitalEvent.objects.filter(hospital=hospital)
        # 如果你想返回事件详情，需要取出 event 对象
        events = [he.event for he in hospital_events]
        serializer = EmergencyEventSerializer(events, many=True)
        return Response({
            "code": 0,
            "message": "success",
            "data": serializer.data
        })

# 🏥 3. 医院-科室关系 (M:N)
class HospitalDepartmentViewSet(viewsets.ModelViewSet):
    queryset = HospitalDepartment.objects.all()
    serializer_class = HospitalDepartmentSerializer
    permission_classes = [IsCityAdmin | IsHospitalAdmin] # 居民不需要看这个纯关系表

    def perform_create(self, serializer):
        # 自动填充 hospital_id，防止医院管理员给别的医院加科室
        user = self.request.user
        if user.profile.role == 'hospital_admin':
            serializer.save(hospital=user.profile.hospital)
        else:
            serializer.save()

# 🏥 4 & 4.11 医院评分
class HospitalServiceScoreViewSet(viewsets.ModelViewSet):
    queryset = HospitalServiceScore.objects.all()
    serializer_class = HospitalServiceScoreSerializer
    permission_classes = [IsCityAdmin | IsHospitalAdmin | ReadOnly]

    def perform_create(self, serializer):
        # 医院管理员上报评分，自动绑定本院
        user = self.request.user
        if user.profile.role == 'hospital_admin':
            serializer.save(hospital=user.profile.hospital)
        else:
            serializer.save()


class DistrictViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
    permission_classes = [permissions.AllowAny] # 允许前端随意获取列表