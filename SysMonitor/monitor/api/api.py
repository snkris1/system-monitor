from ninja import Router
from monitor.models import CPU, Device
from .schemas import CPUSchema, CPUCreateSchema, DeviceSchema
from django.shortcuts import get_object_or_404
from datetime import datetime 

monitor_router = Router()

@monitor_router.get("{device}/cpu", response=list[CPUSchema])
def get_cpu_data(request, device: str):
    device_model = get_object_or_404(Device, name=device)
    return CPU.objects.filter(device=device_model)

@monitor_router.get("{device}/cpu/{timestamp}")
def get_cpu_data_at_timestamp(request, device: str, timestamp: datetime):
    device_model = get_object_or_404(Device, name=device)
    return CPU.objects.filter(device=device_model, timestamp=timestamp)

@monitor_router.post("{device}/cpu", response=CPUSchema)
def create_cpu_data(request, cpu: CPUCreateSchema, device: str):
    device_model = get_object_or_404(Device, name=device)
    cpu_data = cpu.dict()
    cpu_model = CPU.objects.create(device=device_model, **cpu_data)
    return cpu_model

@monitor_router.post("/device", response=DeviceSchema)
def create_device(request, device: DeviceSchema):
    device_data = device.dict()
    device_model = Device.objects.create(**device_data)
    return device_model