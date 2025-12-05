from rest_framework import serializers
from api.models import (
    District, HospitalLevel, Hospital, Department,
    DepartmentResource, Staff, HospitalServiceScore,
    EmergencyEvent, HospitalDepartment, HospitalStaff,
    DepartmentStaff, HospitalEvent
)


# 1. 基础信息序列化器 (用于下拉框选择等)
class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = '__all__'


class HospitalLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = HospitalLevel
        fields = '__all__'


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


# 2. 医院相关序列化器
class HospitalSerializer(serializers.ModelSerializer):
    # 如果想在返回医院信息时，直接看到等级的名字，而不是 level_id，可以用这个技巧：
    level_name = serializers.CharField(source='level.level_name', read_only=True)
    district_name = serializers.CharField(source='district.district_name', read_only=True)
    staff_count = serializers.SerializerMethodField()
    class Meta:
        model = Hospital
        fields = '__all__'
    def get_staff_count(self, obj):
        # 统计关联到该医院的员工数量
        return obj.hospitalstaff_set.count()
class HospitalServiceScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = HospitalServiceScore
        fields = '__all__'


# 3. 资源相关序列化器
class DepartmentResourceSerializer(serializers.ModelSerializer):
    dept_name = serializers.CharField(source='dept.dept_name', read_only=True)
    hospital_name = serializers.CharField(source='hospital.name', read_only=True)

    class Meta:
        model = DepartmentResource
        fields = '__all__'


# 4. 人员相关序列化器
class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = '__all__'


class HospitalEventSerializer(serializers.ModelSerializer):
    hospital_name = serializers.CharField(source='hospital.name', read_only=True)
    role_display = serializers.CharField(source='get_role_display', read_only=True)

    class Meta:
        model = HospitalEvent
        fields = ['id', 'hospital', 'hospital_name', 'role', 'role_display', 'response_time', 'affected_patient_count']

# 5. 事件相关序列化器
class EmergencyEventSerializer(serializers.ModelSerializer):
    # 用于读取：嵌套显示参与的医院列表
    participating_hospitals = HospitalEventSerializer(source='hospital_participations', many=True, read_only=True)

    # 用于写入：接收前端传来的参与医院列表 [{'hospital_id': 1, 'role': 'primary'}, ...]
    participants = serializers.ListField(
        child=serializers.DictField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = EmergencyEvent
        fields = '__all__'

    def create(self, validated_data):
        # 提取 participants 数据
        participants_data = validated_data.pop('participants', [])

        # 创建事件本身
        event = EmergencyEvent.objects.create(**validated_data)

        # 创建关联的医院记录
        for p_data in participants_data:
            hospital_id = p_data.get('hospital_id')
            role = p_data.get('role', 'reporting')  # 默认为报告医院
            if hospital_id:
                HospitalEvent.objects.create(
                    event=event,
                    hospital_id=hospital_id,
                    role=role
                )

        return event


# --- 关系表序列化器 (M:N) ---

class HospitalDepartmentSerializer(serializers.ModelSerializer):
    # 可以在这里定义更详细的显示，比如同时显示医院名和科室名
    hospital_name = serializers.CharField(source='hospital.name', read_only=True)
    dept_name = serializers.CharField(source='dept.dept_name', read_only=True)

    class Meta:
        model = HospitalDepartment
        fields = '__all__'


class HospitalStaffSerializer(serializers.ModelSerializer):
    staff_name = serializers.CharField(source='staff.name', read_only=True)
    hospital_name = serializers.CharField(source='hospital.name', read_only=True)

    class Meta:
        model = HospitalStaff
        fields = '__all__'


class DepartmentStaffSerializer(serializers.ModelSerializer):
    staff_name = serializers.CharField(source='staff.name', read_only=True)
    dept_name = serializers.CharField(source='dept.dept_name', read_only=True)

    class Meta:
        model = DepartmentStaff
        fields = '__all__'

