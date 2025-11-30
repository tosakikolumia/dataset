from django.core.management.base import BaseCommand
from django.utils import timezone
from api.models import (
    District, HospitalLevel, Hospital, Department,
    DepartmentResource, Staff, HospitalServiceScore,
    EmergencyEvent, HospitalDepartment, HospitalStaff,
    DepartmentStaff, HospitalEvent
)


class Command(BaseCommand):
    help = "Inject initial test data into database"

    def handle(self, *args, **kwargs):
        # -----------------------------
        # 1. District
        # -----------------------------
        districts = [
            (1, "南山区"),
            (2, "福田区"),
            (3, "罗湖区"),
        ]
        for id_, name in districts:
            District.objects.get_or_create(
                district_id=id_,
                defaults={"district_name": name}
            )

        # -----------------------------
        # 2. HospitalLevel
        # -----------------------------
        levels = [
            (1, "三级甲等", "最高等级医院"),
            (2, "三级乙等", "大型综合医院"),
            (3, "二级甲等", "区域主要医院"),
        ]
        for id_, name, desc in levels:
            HospitalLevel.objects.get_or_create(
                level_id=id_,
                defaults={"level_name": name, "description": desc}
            )

        # -----------------------------
        # 3. Hospital
        # -----------------------------
        Hospital.objects.get_or_create(
            hospital_id=1,
            defaults={
                "name": "深圳市人民医院",
                "address": "福田区深南大道1018号",
                "district_id": 2,
                "level_id": 1,
                "longitude": 114.064839,
                "latitude": 22.548857,
                "established_year": 1985,
                "bed_total": 3000,
                "outpatient_capacity": 5000,
            }
        )

        Hospital.objects.get_or_create(
            hospital_id=2,
            defaults={
                "name": "南山医院",
                "address": "南山区桃园路200号",
                "district_id": 1,
                "level_id": 2,
                "longitude": 113.932777,
                "latitude": 22.533333,
                "established_year": 1990,
                "bed_total": 1500,
                "outpatient_capacity": 3000,
            }
        )

        # -----------------------------
        # 4. Department
        # -----------------------------
        Department.objects.get_or_create(dept_id=1, defaults={"dept_name": "内科"})
        Department.objects.get_or_create(dept_id=2, defaults={"dept_name": "外科"})
        Department.objects.get_or_create(dept_id=3, defaults={"dept_name": "急诊科"})

        # -----------------------------
        # 5. DepartmentResource
        # -----------------------------
        DepartmentResource.objects.get_or_create(
            dept_res_id=1, dept_id=1,
            defaults={"bed_count": 100, "device_count": 20, "daily_capacity": 150}
        )
        DepartmentResource.objects.get_or_create(
            dept_res_id=2, dept_id=3,
            defaults={"bed_count": 50, "device_count": 15, "daily_capacity": 300}
        )

        # -----------------------------
        # 6. Staff
        # -----------------------------
        staff_list = [
            (1, "张三", "男", "主任医师", "13800138000"),
            (2, "李四", "女", "副主任医师", "13800138001"),
            (3, "王五", "男", "护士长", "13800138002"),
        ]
        for sid, name, gender, title, phone in staff_list:
            Staff.objects.get_or_create(
                staff_id=sid,
                defaults={
                    "name": name,
                    "gender": gender,
                    "title": title,
                    "phone": phone,
                    "hire_date": timezone.now().date()
                }
            )

        # -----------------------------
        # 7. HospitalServiceScore
        # -----------------------------
        HospitalServiceScore.objects.get_or_create(
            score_id=1, hospital_id=1,
            defaults={
                "hygiene_score": 95.5,
                "satisfaction_score": 92.3,
                "last_inspection_date": timezone.now().date()
            }
        )

        # -----------------------------
        # 8. EmergencyEvent
        # -----------------------------
        EmergencyEvent.objects.get_or_create(
            event_id=1,
            defaults={
                "event_type": "火灾事故",
                "severity": "严重",
                "report_time": timezone.now()
            }
        )

        # -----------------------------
        # 9. HospitalDepartment（M:N）
        # -----------------------------
        HospitalDepartment.objects.get_or_create(
            hospital_id=1, dept_id=1,
            defaults={"floor": "3F", "room_count": 20}
        )
        HospitalDepartment.objects.get_or_create(
            hospital_id=1, dept_id=3,
            defaults={"floor": "1F", "room_count": 10}
        )

        # -----------------------------
        # 10. HospitalStaff（M:N）
        # -----------------------------
        HospitalStaff.objects.get_or_create(
            hospital_id=1, staff_id=1,
            defaults={"employment_type": "全职"}
        )
        HospitalStaff.objects.get_or_create(
            hospital_id=1, staff_id=3,
            defaults={"employment_type": "兼职"}
        )

        # -----------------------------
        # 11. DepartmentStaff（M:N）
        # -----------------------------
        DepartmentStaff.objects.get_or_create(
            dept_id=1, staff_id=1,
            defaults={"role_in_dept": "科主任"}
        )
        DepartmentStaff.objects.get_or_create(
            dept_id=3, staff_id=3,
            defaults={"role_in_dept": "负责人"}
        )

        # -----------------------------
        # 12. HospitalEvent（M:N）
        # -----------------------------
        HospitalEvent.objects.get_or_create(
            hospital_id=1, event_id=1,
            defaults={
                "role": "应急处理",
                "response_time": timezone.now(),
                "affected_patient_count": 50
            }
        )

        self.stdout.write(self.style.SUCCESS("Test data injected successfully!"))
