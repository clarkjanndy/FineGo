from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin

from . models import (
    Department,
    User, 
    FAQ, 
    SystemInformation
)

# Register your admin manager here
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'abbreviation',)
    search_fields = ('name', 'abbreviation',)

class UserAdmin(DefaultUserAdmin):
    list_display = ('username', 'email', 'last_login', 'is_superuser', 'date_joined')

    fieldsets = (
        (_("Credentials"), {"fields": ("username", "password")}),
        (_("Information"), {"fields": ("student_id", "email", "first_name", 
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

# Register your models here.
admin.site.register(Department, DepartmentAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(FAQ, FAQAdmin)
admin.site.register(SystemInformation, SystemInformationAdmin)

