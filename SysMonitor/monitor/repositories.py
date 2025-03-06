from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from .models import Device, CPU, Memory, Network
from django.core import serializers
import logging

#TODO: MISSING ERROR HANDLING FOR EXCEPTIONS FOR SOME FUNCTIONS

logger = logging.getLogger("system_monitor")

class RepositoryError(Exception):
    """Base class for all repository errors."""
    pass

class DeviceRepository:
    def create_device(self, user, device_data):
        try:
            return Device.objects.create(user=user, **device_data)
        except IntegrityError as e:
            if 'UNIQUE constraint' in str(e):
                raise IntegrityError(f"Device with name '{device_data.get('name')}' already exists for this user.") from e
            raise  # Re-raise other IntegrityErrors
        except Exception as e:
            raise RepositoryError(f"Failed to create device: {e}") from e

    def get_device_by_name(self, name, user):
        try:
            logger.debug(f"device repository 'get_device_by_name' called for USER: {user}, DEVICE: {name}")
            return Device.objects.get(name=name, user=user)
        except Device.DoesNotExist:
            raise ObjectDoesNotExist
        except Exception as e:
            raise RepositoryError(f"Failed to get device: {e}") from e
        
    def get_metrics(self, user, device: Device):
        try:
            logger.debug(f"device repository initiated for data metrics retrieval for USER: {user}, DEVICE: {device}")

            cpu_data = device.cpu_data.all()
            memory_data = device.memory_data.all()
            network_data = device.network_data.all()

            cpu_data_json = serializers.serialize('json', cpu_data)
            memory_data_json = serializers.serialize('json', memory_data)
            network_data_json = serializers.serialize('json', network_data)

            metrics = {
                "cpu_data": cpu_data_json,
                "memory_data": memory_data_json,
                "network_data": network_data_json
            }

            return metrics
        except Exception as e:
            raise RepositoryError(f"Failed to retrieve metrics: {e}") from e

class CPURepository:
    def get_cpu_data(self, device):
        return CPU.objects.filter(device=device)

    def get_cpu_data_at_timestamp(self, device, timestamp):
        try:
            return CPU.objects.get(device=device, timestamp=timestamp)
        except CPU.DoesNotExist:
            raise ObjectDoesNotExist

    def create_cpu_data(self, device, cpu_data):
        try:
            return CPU.objects.create(device=device, **cpu_data)
        except Exception as e:
            raise RepositoryError(f"Failed to create CPU data: {e}") from e  # Generic error for unexpected issues

class MemoryRepository:
    def get_memory_data(self, device):
        return Memory.objects.filter(device=device)

    def get_memory_data_at_timestamp(self, device, timestamp):
        try:
            return Memory.objects.get(device=device, timestamp=timestamp)
        except Memory.DoesNotExist:
            raise ObjectDoesNotExist

    def create_memory_data(self, device, memory_data):
        try:
            return Memory.objects.create(device=device, **memory_data)
        except Exception as e:
            raise RepositoryError(f"Failed to create memory data: {e}") from e # Generic error

class NetworkRepository:
    def get_network_data(self, device):
        return Network.objects.filter(device=device)

    def get_network_data_at_timestamp(self, device, timestamp):
        try:
            return Network.objects.get(device=device, timestamp=timestamp)
        except Network.DoesNotExist:
            raise ObjectDoesNotExist

    def create_network_data(self, device, network_data):
        try:
            return Network.objects.create(device=device, **network_data)
        except Exception as e:
            raise RepositoryError(f"Failed to create network data: {e}") from e # Generic error