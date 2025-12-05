from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Count, Q ,Case, When, IntegerField
from api.models import Hospital, DepartmentResource, HospitalDepartment, Department,Staff,HospitalStaff
from api.permission import IsCityAdmin


class StatisticsViewSet(viewsets.ViewSet):
    """
    市政管理-全城资源统计接口
    """
    permission_classes = [IsCityAdmin]  # 只有市政管理员能看

    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        """
        获取顶部卡片数据 (Dashboard)
        """
        # 1. 基础计数
        total_hospitals = Hospital.objects.count()

        # 2. 资源总和 (使用 Django 聚合函数)
        # 注意：如果没有数据，aggregate 返回 None，所以要用 or 0
        total_beds = Hospital.objects.aggregate(sum=Sum('bed_total'))['sum'] or 0
        total_rooms = HospitalDepartment.objects.aggregate(sum=Sum('room_count'))['sum'] or 0
        total_devices = DepartmentResource.objects.aggregate(sum=Sum('device_count'))['sum'] or 0

        # 3. ICU 特殊统计 (假设科室名包含 "ICU" 或 "重症")
        icu_departments = Department.objects.filter(Q(dept_name__icontains='ICU') | Q(dept_name__icontains='重症'))
        icu_beds = DepartmentResource.objects.filter(dept__in=icu_departments).aggregate(sum=Sum('bed_count'))[
                       'sum'] or 0

        # 4. 科室覆盖率 (全市一共有多少种不同的科室)
        total_dept_types = Department.objects.count()

        return Response({
            "code": 0,
            "message": "success",
            "data": {
                "total_hospitals": total_hospitals,
                "total_dept_types": total_dept_types,
                "total_beds": total_beds,
                "total_rooms": total_rooms,
                "total_devices": total_devices,
                "icu_beds": icu_beds,
            }
        })

    @action(detail=False, methods=['get'])
    def hospital_rank(self, request):
        """
        获取资源统计表数据 (带筛选)
        """
        # 获取筛选参数
        district_id = request.query_params.get('district')
        level_id = request.query_params.get('level')

        qs = Hospital.objects.all()

        if district_id:
            qs = qs.filter(district_id=district_id)
        if level_id:
            qs = qs.filter(level_id=level_id)

        # 构造列表数据
        data = []
        for h in qs:
            # 统计该医院下的资源
            # 诊室数 (从中间表查)
            room_count = HospitalDepartment.objects.filter(hospital=h).aggregate(sum=Sum('room_count'))['sum'] or 0

            # 设备数 & ICU床位 (从资源表查)
            resources = DepartmentResource.objects.filter(hospital=h)
            device_count = resources.aggregate(sum=Sum('device_count'))['sum'] or 0

            # 简单模拟紧张度 (床位越少越紧张，或者根据门诊量)
            # 逻辑：如果 日门诊量 / 总床位 > 5，视为紧张
            stress = "normal"
            if h.bed_total and h.outpatient_capacity:
                ratio = h.outpatient_capacity / h.bed_total
                if ratio > 5:
                    stress = "high"
                elif ratio > 3:
                    stress = "medium"

            data.append({
                "hospital_id": h.hospital_id,
                "name": h.name,
                "district": h.district.district_name,
                "level": h.level.level_name,
                "bed_total": h.bed_total,
                "room_count": room_count,
                "device_count": device_count,
                "stress": stress
            })

        return Response({
            "code": 0,
            "message": "success",
            "data": data
        })


@action(detail=False, methods=['get'])
def staff_structure(self, request):
    """
    统计全市医护人员规模、医生护士比例、职称结构
    """
    # 1. 总体规模 (基于 Staff 表)
    total_staff = Staff.objects.count()

    # 使用 title 字段进行模糊匹配统计
    doctors_count = Staff.objects.filter(title__contains='医').count()
    nurses_count = Staff.objects.filter(title__contains='护').count()
    # 其他人员 = 总数 - 医生 - 护士
    others_count = total_staff - doctors_count - nurses_count

    # 2. 职称结构分布 (Group By Title)
    # 过滤掉 title 为空的数据
    title_distribution = Staff.objects.exclude(title__isnull=True).exclude(title='').values('title').annotate(
        count=Count('staff_id')
    ).order_by('-count')

    # 3. 各医院人员分布 (基于 HospitalStaff 中间表)
    # 使用条件聚合 (Case/When) 统计各医院的 医生/护士/其他 数量
    hospital_stats = HospitalStaff.objects.values(
        'hospital__name',
        'hospital__hospital_id'
    ).annotate(
        total=Count('staff__staff_id'),
        # 统计医生：关联的 staff 表 title 包含 '医'
        doctors=Count(Case(When(staff__title__contains='医', then=1), output_field=IntegerField())),
        # 统计护士：关联的 staff 表 title 包含 '护'
        nurses=Count(Case(When(staff__title__contains='护', then=1), output_field=IntegerField())),
    ).order_by('-total')

    # 格式化为前端需要的结构
    formatted_hospital_dist = []
    for h in hospital_stats:
        doc = h['doctors']
        nur = h['nurses']
        total = h['total']
        other = total - doc - nur

        formatted_hospital_dist.append({
            "hospitalId": h['hospital__hospital_id'],
            "hospitalName": h['hospital__name'],
            "doctorsCount": doc,
            "nursesCount": nur,
            "otherCount": other,
            "total": total
        })

    return Response({
        "code": 0,
        "message": "success",
        "data": {
            "overview": {
                "total": total_staff,
                "doctors": doctors_count,
                "nurses": nurses_count,
                "others": others_count
            },
            "title_structure": title_distribution,
            "hospital_distribution": formatted_hospital_dist
        }
    })