from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class TimestampedModel(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Timestamp", help_text="Time of the record")

    class Meta:
        abstract = True

class Device(models.Model):
    name = models.CharField(max_length=255, verbose_name="Device Name", help_text="Name of the device")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User", related_name="devices")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Device"
        verbose_name_plural = "Devices"

class CPU(TimestampedModel):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, verbose_name="CPU Device", related_name="cpu")
    total_usage_percent = models.FloatField(verbose_name="Total CPU Utilization")
    per_cpu_percent = models.JSONField(verbose_name="CPU Utilization per Core")
    cpu_freq = models.JSONField(verbose_name="CPU Frequency")
    cpu_temperature = models.JSONField(verbose_name="CPU Temperature", help_text="CPU temperature in Celsius")

    def __str__(self):
        return f"{self.device.name} CPU Information"
    
    class Meta:
        verbose_name = "CPU"
        verbose_name_plural = "CPUs"
        ordering = ['timestamp']
    
class Memory(TimestampedModel):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, verbose_name="CPU Device", related_name="memory")
    total_memory = models.IntegerField(verbose_name="Total Memory")
    available_memory = models.IntegerField(verbose_name="Available Memory")
    used_memory = models.IntegerField(verbose_name="Used Memory")
    memory_percent = models.FloatField(verbose_name="Memory Usage")

    def __str__(self):
        return f"{self.device.name} Memory Information"
    
    class Meta:
        verbose_name = "Memory"
        verbose_name_plural = "Memory"
        ordering = ['-timestamp']

class Network(TimestampedModel):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, verbose_name="CPU Device", related_name="network")
    is_up = models.BooleanField(verbose_name="Is Up", help_text="Network status")
    speed = models.IntegerField(verbose_name="Speed")
    mtu = models.IntegerField(verbose_name="MTU")

    def __str__(self):
        return f"{self.device.name} Network Information"
    
    class Meta:
        verbose_name = "Network"
        verbose_name_plural = "Networks"
        ordering = ['-timestamp']