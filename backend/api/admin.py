from django.contrib import admin

# Register your models here.
# api/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from api.models import UserProfile, Hospital

# 定义一个内联界面，把 Profile 嵌入到 User 页面里
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = '用户角色档案'

# 重新定义 User 管理界面
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)

# 重新注册 User
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# 顺便把医院也注册了，方便你造假数据
admin.site.register(Hospital)