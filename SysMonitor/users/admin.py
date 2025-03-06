from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from monitor.models import Device

# TODO: FIGURE OUT HOW TO USE ADMIN DASHBOARD
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'devices', 'is_staff')

    def devices(self, obj):
        return ", ".join([device.name for device in Device.objects.filter(user=obj)])

admin.site.register(User, UserAdmin)

