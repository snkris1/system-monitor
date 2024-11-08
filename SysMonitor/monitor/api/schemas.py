from ninja import ModelSchema, Schema
from monitor.models import InputActivity, CPU, Device
from pydantic import field_validator

class DeviceSchema(ModelSchema):
    class Meta:
        model = Device
        model_fields = ['device_name']

class CPUSchema(ModelSchema):
    class Meta:
        model = CPU
        model_fields = ['device', 'cpu_utilization', 'cpu_temperature', 'timestamp']

class CPUCreateSchema(Schema):
    device: str
    cpu_utilization: float
    cpu_temperature: int

    @field_validator('cpu_utilization')
    @classmethod
    def validate_cpu_utilization(cls, value: float) -> float:
        if not (0 <= value <= 100):
            raise ValueError('CPU utilization must be between 0 and 100')
        return value
    
    @field_validator('cpu_temperature')
    @classmethod
    def validate_cpu_temperature(cls, value: int) -> int:
        if value < 0:
            raise ValueError('CPU temperature must be a positive integer')
        return value