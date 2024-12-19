import functools
from ninja import Router
from ninja.errors import HttpError
from .schemas import (
    CPUSchema, 
    CPUCreateSchema, 
    DeviceSchema, 
    MemorySchema, 
    MemoryCreateSchema, 
    NetworkSchema, 
    NetworkCreateSchema
)
from ..services import (
    DeviceService, 
    CPUService, 
    MemoryService, 
    NetworkService, 
    ServiceError, 
    IntegrityError
)
from ..repositories import (
    CPURepository,
    NetworkRepository,
    MemoryRepository,
    DeviceRepository,
)
from datetime import datetime 

monitor_router = Router()

def handle_service_errors(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ServiceError as e:
            raise HttpError(400, str(e))
        except ValueError as e:
            raise HttpError(400, str(e))
    return wrapper

# DEVICE
@monitor_router.post("/device", response=DeviceSchema)
@handle_service_errors
def create_device(request, device: DeviceSchema):
    user = request.auth
    device_repository = DeviceRepository()
    device_service = DeviceService(device_repository)
    device_data = device.dict()
    return device_service.create_device(user, device_data)

# CPU
@monitor_router.get("/{device}/cpu", response=list[CPUSchema])
@handle_service_errors
def get_cpu_data(request, device: str):
    user = request.auth
    device_repository = DeviceRepository()
    cpu_repository = CPURepository()
    cpu_service = CPUService(device_repository, cpu_repository)
    return cpu_service.get_cpu_data(user, device)

@monitor_router.get("/{device}/cpu/{timestamp}")
@handle_service_errors
def get_cpu_data_at_timestamp(request, device: str, timestamp: datetime):
    user = request.auth
    device_repository = DeviceRepository()
    cpu_repository = CPURepository()
    cpu_service = CPUService(device_repository, cpu_repository)
    return cpu_service.get_cpu_data_at_timestamp(user, device, timestamp)

@monitor_router.post("/{device}/cpu", response=CPUSchema)
@handle_service_errors
def create_cpu_data(request, cpu: CPUCreateSchema, device: str):
    user = request.auth
    device_repository = DeviceRepository()
    cpu_repository = CPURepository()
    cpu_service = CPUService(device_repository, cpu_repository)
    cpu_data = cpu.dict()
    return cpu_service.create_cpu_data(user, device, cpu_data)

# MEMORY
@monitor_router.get("/{device}/memory", response=list[MemorySchema])
@handle_service_errors
def get_memory_data(request, device: str):
    user = request.auth
    device_repository = DeviceRepository()
    memory_repository = MemoryRepository()
    memory_service = MemoryService(device_repository, memory_repository)
    return memory_service.get_memory_data(user, device)

@monitor_router.get("/{device}/memory/{timestamp}", response=MemorySchema)
@handle_service_errors
def get_memory_data_at_timestamp(request, device:str, timestamp: datetime):
    user = request.auth
    device_repository = DeviceRepository()
    memory_repository = MemoryRepository()
    memory_service = MemoryService(device_repository, memory_repository)
    return memory_service.get_memory_data_at_timestamp(user, device, timestamp)

@monitor_router.post("/{device}/memory", response=MemorySchema)
@handle_service_errors
def create_memory_data(request, device: str, data: MemoryCreateSchema):
    user = request.auth
    device_repository = DeviceRepository()
    memory_repository = MemoryRepository()
    memory_service = MemoryService(device_repository, memory_repository)
    memory_data = data.dict()
    return memory_service.create_memory_data(user, device, memory_data)

# NETWORK
@monitor_router.get("/{device}/network", response=list[NetworkSchema])
@handle_service_errors
def get_network_data(request, device: str):
    user = request.auth
    device_repository = DeviceRepository()
    network_repository = NetworkRepository()
    network_service = NetworkService(device_repository, network_repository)
    return network_service.get_network_data(user, device)

@monitor_router.get("/{device}/network/{timestamp}", response=NetworkSchema)
@handle_service_errors
def get_network_data_at_timestamp(request, device: str, timestamp: datetime):
    user = request.auth
    device_repository = DeviceRepository()
    network_repository = NetworkRepository()
    network_service = NetworkService(device_repository, network_repository)
    return network_service.get_network_data_at_timestamp(user, device, timestamp)

@monitor_router.post("/{device}/network", response=NetworkSchema)
@handle_service_errors
def create_network_data(request, device:str, data: NetworkCreateSchema):
    user = request.auth
    device_repository = DeviceRepository()
    network_repository = NetworkRepository()
    network_service = NetworkService(device_repository, network_repository)
    network_data = data.dict()
    return network_service.create_network_data(user, device, network_data)