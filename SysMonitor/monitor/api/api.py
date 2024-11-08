from ninja import Router
from monitor.models import InputActivity, CPU, Device
from .schemas import CPUSchema, CPUCreateSchema, DeviceSchema
from django.shortcuts import get_object_or_404
from datetime import datetime 

api = Router()

@api.get("{device}/cpu", response=list[CPUSchema])
def get_cpu_data(request, device_name: str):
    device_model = get_object_or_404(Device, name=device_name)
    return CPU.objects.filter(device=device_model)

@api.get("{device}/cpu/{timestamp}")
def get_cpu_data_at_timestamp(request, device_name: str, timestamp: datetime):
    device_model = get_object_or_404(Device, name=device_name)
    return CPU.objects.filter(device=device_model, timestamp=timestamp)

@api.post("{device}/cpu", response=CPUSchema)
def create_cpu_data(request, cpu: CPUCreateSchema, device_name: str):
    device_model = get_object_or_404(Device, name=device_name)
    cpu_data = cpu.dict()
    cpu_model = CPU.objects.create(device=device_model, **cpu_data)
    return cpu_model

api.post("/device", response=DeviceSchema)
def create_device(request, device: DeviceSchema):
    device_data = device.dict()
    device_model = Device.objects.create(**device_data)
    return device_model