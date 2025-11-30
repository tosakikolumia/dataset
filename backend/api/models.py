from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


# --- 0. 用户档案扩展 (处理角色) ---
class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('city_admin', '市政管理'),
        ('hospital_admin', '医院管理'),
        ('public', '居民'),
    )

    # 关联到 Django 自带的 User 表
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='public')

    # 如果是医院管理员，必须关联一家医院 (如果是市政或居民，这里为空)
    # 注意：这里用了字符串 'Hospital' 是因为 Hospital 类还在下面没定义，防报错
    hospital = models.ForeignKey('Hospital', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"

# 1. District（行政区）
class District(models.Model):
    district_id = models.IntegerField(primary_key=True)
    district_name = models.CharField(max_length=100)

    class Meta:
        db_table = 'District'


# 2. HospitalLevel（医院等级）
class HospitalLevel(models.Model):
    level_id = models.IntegerField(primary_key=True)
    level_name = models.CharField(max_length=50)
    description = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'HospitalLevel'


# 3. Hospital（医院）
class Hospital(models.Model):
    hospital_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=300, null=True, blank=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, db_column='district_id')
    level = models.ForeignKey(HospitalLevel, on_delete=models.CASCADE, db_column='level_id')
    longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    established_year = models.IntegerField(null=True, blank=True)
    bed_total = models.IntegerField(null=True, blank=True)
    outpatient_capacity = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'Hospital'


# 4. Department（科室）
class Department(models.Model):
    dept_id = models.IntegerField(primary_key=True)
    dept_name = models.CharField(max_length=200)
    standard_code = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = 'Department'


# 5. DepartmentResource（科室资源）
class DepartmentResource(models.Model):
    dept_res_id = models.AutoField(primary_key=True)

    # ✅✅✅ 必须补上下面这一行！否则没法区分这是哪家医院的资源
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, db_column='hospital_id')

    dept = models.ForeignKey(Department, on_delete=models.CASCADE, db_column='dept_id')
    bed_count = models.IntegerField(null=True)
    device_count = models.IntegerField(null=True)
    daily_capacity = models.IntegerField(null=True)

    class Meta:
        db_table = 'DepartmentResource'


# 6. Staff（医护人员）
class Staff(models.Model):
    staff_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    gender = models.CharField(max_length=10, null=True, blank=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    hire_date = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'Staff'


# 7. HospitalServiceScore（医院评分）
class HospitalServiceScore(models.Model):
    score_id = models.IntegerField(primary_key=True)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, db_column='hospital_id')
    hygiene_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    satisfaction_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    last_inspection_date = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'HospitalServiceScore'


# 8. EmergencyEvent（突发事件）
class EmergencyEvent(models.Model):
    event_id = models.IntegerField(primary_key=True)
    event_type = models.CharField(max_length=200, null=True, blank=True)
    severity = models.CharField(max_length=50, null=True, blank=True)
    report_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'EmergencyEvent'


# ========================================================
#   多对多中间表（全部有额外字段 → 必须建独立 Model）
# ========================================================

# 9. HospitalDepartment（医院开设科室）
class HospitalDepartment(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, db_column='hospital_id')
    dept = models.ForeignKey(Department, on_delete=models.CASCADE, db_column='dept_id')
    floor = models.CharField(max_length=50, null=True, blank=True)
    room_count = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'HospitalDepartment'
        unique_together = (('hospital', 'dept'),)


# 10. HospitalStaff（员工在医院执业）
class HospitalStaff(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, db_column='hospital_id')
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, db_column='staff_id')
    employment_type = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = 'HospitalStaff'
        unique_together = (('hospital', 'staff'),)


# 11. DepartmentStaff（员工在科室任职）
class DepartmentStaff(models.Model):
    dept = models.ForeignKey(Department, on_delete=models.CASCADE, db_column='dept_id')
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, db_column='staff_id')
    role_in_dept = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = 'DepartmentStaff'
        unique_together = (('dept', 'staff'),)


# 12. HospitalEvent（医院参与突发事件）
class HospitalEvent(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, db_column='hospital_id')
    event = models.ForeignKey(EmergencyEvent, on_delete=models.CASCADE, db_column='event_id')
    role = models.CharField(max_length=100, null=True, blank=True)
    response_time = models.DateTimeField(null=True, blank=True)
    affected_patient_count = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'HospitalEvent'
        unique_together = (('hospital', 'event'),)
