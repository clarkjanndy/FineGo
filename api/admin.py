from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin

from . models import (
    Department,
    User, 
    FAQ, 
    SystemInformation,
    ActivityGroup,
    Activity,
    Attendance,
    Fine,
    Notification
)

# Register your admin manager here
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'abbreviation',)
    search_fields = ('name', 'abbreviation',)

class UserAdmin(DefaultUserAdmin):
    list_display = ('username', 'email', 'last_login', 'is_superuser', 'date_joined')

    fieldsets = (
        (_("Credentials"), {"fields": ("username", "password")}),
        (_("Information"), {"fields": ("year_level", "department", "student_id", "email", "first_name", 
                                       "middle_name", "last_name", "suffix", "birthday",
                                       "mobile_number", "address", "bio", "photo")}),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer',)
    search_fields = ('question', 'answer',)

class SystemInformationAdmin(admin.ModelAdmin):
    list_display = ('title', 'content',)
    search_fields = ('title', 'content',)
    
class ActivityGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'status',)
    search_fields = ('name', 'status',)
    
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('group', 'name', 'status', 'start_time', 'end_time', 'status')
    search_fields = ('group__name', 'status',)
    
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('activity', 'user',  'time_in', 'time_out')
    search_fields = ('activity', 'user',  'time_in', 'time_out')

class FineAdmin(admin.ModelAdmin):
    list_display = ('user', 'activity',  'amount', 'created_at')
    search_fields = ('user', 'activity',  'amount', 'created_at')
    
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'relation',  'content', 'status', 'created_at')
    search_fields = ('user', 'relation',  'content', 'status', 'created_at')

# Register your models here.
admin.site.register(Department, DepartmentAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(FAQ, FAQAdmin)
admin.site.register(SystemInformation, SystemInformationAdmin)

admin.site.register(ActivityGroup, ActivityGroupAdmin)
admin.site.register(Activity, ActivityAdmin)
admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(Fine, FineAdmin)
admin.site.register(Notification, NotificationAdmin)

