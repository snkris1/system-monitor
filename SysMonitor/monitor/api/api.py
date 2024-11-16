from ninja import Router
from monitor.models import CPU, Device, Memory, Network
from .schemas import CPUSchema, CPUCreateSchema, DeviceSchema, MemorySchema, MemoryCreateSchema, NetworkSchema, NetworkCreateSchema
from django.shortcuts import get_object_or_404
from datetime import datetime 

# BETTER HANDLE ENDPOINTS  WITH USER AS A PARAMETER OR SOMETHING 

monitor_router = Router()


# DEVICE

@monitor_router.post("/device", response=DeviceSchema)
def create_device(request, device: DeviceSchema):
    device_data = device.dict()
    device_model = Device.objects.create(**device_data)
    return device_model


# CPU

@monitor_router.get("/{device}/cpu", response=list[CPUSchema])
def get_cpu_data(request, device: str):
    user = request.user
    device_model = get_object_or_404(Device, name=device, user=user)
    return CPU.objects.filter(device=device_model)

@monitor_router.get("/{device}/cpu/{timestamp}")
def get_cpu_data_at_timestamp(request, device: str, timestamp: datetime):
    user = request.user
    device_model = get_object_or_404(Device, name=device, user=user)
    return CPU.objects.filter(device=device_model, timestamp=timestamp)

@monitor_router.post("/{device}/cpu", response=CPUSchema)
def create_cpu_data(request, cpu: CPUCreateSchema, device: str):
    user = request.user
    device_model = get_object_or_404(Device, name=device, user=user)
    cpu_data = cpu.dict()
    cpu_model = CPU.objects.create(device=device_model, **cpu_data)
    return cpu_model


# MEMORY
# ensure URL path parameters are standard and follow other REST API standards
@monitor_router.get("/{device}/memory", response=list[MemorySchema])
def get_memory_data(request, device: str):
    user = request.user
    device_model = get_object_or_404(Device, name=device, user=user)
    return Memory.objects.filter(device=device_model)

@monitor_router.get("/{device}/memory/{timestamp}", response=MemorySchema)
def get_memory_data_at_timestamp(request, device:str, timestamp: datetime):
    user = request.user
    device_model = get_object_or_404(Device, name=device, user=user)
    return Memory.objects.filter(device=device_model, timestamp=timestamp)

@monitor_router.post("/{device}/memory", response=MemorySchema)
def create_memory_data(request, device: str, data: MemoryCreateSchema):
    user = request.user
    device_model = get_object_or_404(Device, name=device, user=user)
    memory_data = data.dict()
    memory_model = Memory.objects.create(device=device_model, **memory_data)
    return memory_model

# Network
@monitor_router.get("/{device}/network", response=list[NetworkSchema])
def get_network_data(request, device: str):
    user = request.user
    device_model = get_object_or_404(Device, name=device, user=user)
    return Network.objects.filter(device=device_model)

@monitor_router.get("/{device}/network/{timestamp}", response=NetworkSchema)
def get_network_data_at_timestamp(request, device: str, timestamp: datetime):
    user = request.user
    device_model = get_object_or_404(Device, name=device, user=user)
    return Network.objects.filter(device=device_model, timestamp=timestamp)

@monitor_router.post("/{device}/network", response=NetworkSchema)
def create_network_data(request, device:str, data: NetworkCreateSchema):
    user = request.user
    device_model = get_object_or_404(Device, name=device, user=user)
    network_data = data.dict()
    network_model = Network.objects.create(device=device_model, **network_data)
    return network_model