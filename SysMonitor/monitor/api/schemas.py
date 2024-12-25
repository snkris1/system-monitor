from ninja import ModelSchema, Schema
from monitor.models import CPU, Device, Memory, Network
from pydantic import field_validator

class DeviceSchema(ModelSchema):
    class Meta:
        model = Device
        fields = ['name']

class CPUSchema(ModelSchema):
    class Meta:
        model = CPU
        fields = ['device', 'total_usage_percent', 'per_cpu_percent', 'cpu_freq', 'cpu_temperature']

class CPUCreateSchema(Schema):
    total_usage_percent: float
    per_cpu_percent: dict
    cpu_freq: dict
    cpu_temperature: dict

    @field_validator('total_usage_percent')
    @classmethod
    def validate_cpu_utilization(cls, value: float) -> float:
        if not (0 <= value <= 100):
            raise ValueError('Total CPU utilization must be between 0 and 100')
        return value
    
class MemorySchema(ModelSchema):
    class Meta:
        model = Memory
        fields = ['total_memory', 'available_memory', 'used_memory', 'memory_percent']

class MemoryCreateSchema(Schema):
    class Meta:
        model = Memory
        fields = ['total_memory', 'available_memory', 'used_memory', 'memory_percent']

class NetworkSchema(ModelSchema):
    class Meta:
        model = Network
        fields = ['is_up', 'speed', 'mtu']

class NetworkCreateSchema(ModelSchema):
    class Meta:
        model = Network
        fields = ['is_up', 'speed', 'mtu']