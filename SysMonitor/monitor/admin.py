from django.contrib import admin
from .models import Device, CPU

class CPUAdmin(admin.ModelAdmin):
    list_display = ("formatted_datetime", "device", "total_usage_percent")
    list_filter = ("device", "timestamp")

    def formatted_datetime(self, obj):
        return obj.timestamp.strftime("%Y-%m-%d %H:%M:%S") 
    formatted_datetime.short_description = 'datetime' 

admin.site.register(Device)
admin.site.register(CPU, CPUAdmin)