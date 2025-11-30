# api/permissions.py
from rest_framework import permissions

class IsCityAdmin(permissions.BasePermission):
    """只允许市政管理员写入，其他人(包括未登录)拒绝"""
    def has_permission(self, request, view):
        return (request.user.is_authenticated and
                hasattr(request.user, 'profile') and
                request.user.profile.role == 'city_admin')

class IsHospitalAdmin(permissions.BasePermission):
    """只允许医院管理员操作"""
    def has_permission(self, request, view):
        return (request.user.is_authenticated and
                hasattr(request.user, 'profile') and
                request.user.profile.role == 'hospital_admin')

    def has_object_permission(self, request, view, obj):
        # 修改/删除时，检查对象是否属于该管理员的医院
        user_hospital = request.user.profile.hospital
        # 检查 obj 是否有 hospital 字段，或者 obj 本身就是 Hospital
        if isinstance(obj, type(user_hospital)):
            return obj == user_hospital
        if hasattr(obj, 'hospital'):
            return obj.hospital == user_hospital
        return False

class IsCityOrHospitalAdmin(permissions.BasePermission):
    """市政或医院管理员均可（用于某些共有操作，如上报事件）"""
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        role = request.user.profile.role
        return role in ['city_admin', 'hospital_admin']

class ReadOnly(permissions.BasePermission):
    """
    只允许读取方法 (GET, HEAD, OPTIONS)
    """
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS