from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
import logging

from .repositories import (
    RepositoryError
)

logger = logging.getLogger("system_monitor")

class ServiceError(Exception):
    """Base class for all service errors."""
    pass

class DeviceService:
    def __init__(self, device_repository_in):
        self.device_repo = device_repository_in
    
    def create_device(self, user, device_data):
        """
        Create a new device with error handling
        """
        try:
            return self.device_repo.create_device(user, device_data)
        except IntegrityError as e:
            logger.error(f"IntegrityError while creating device for user {user.id}: {e}")
            raise ValueError("Device already exists or constraint violation")
        except RepositoryError as e:
            logger.error(f"RepositoryError while creating device for user {user.id}: {e}")
            raise ServiceError("Internal server error")
        
    def get_metrics(self, user, device_name):
        try:
            logger.debug(f"device service initiated for data metrics retrieval for USER: {user}, DEVICE: {device_name}")

            device = self.device_repo.get_device_by_name(device_name, user)
            metrics = self.device_repo.get_metrics(user, device)

            logger.debug("data service: metrics retrieved.")

            return metrics
        except ObjectDoesNotExist as e:
            logger.error(f"ObjectDoesNotExist while fetching device {device_name} for user {user.id}: {e}")
            raise ValueError("Device not found.")
        except RepositoryError as e:
            logger.error(f"RepositoryError while fetching metrics for device {device_name} and user {user.id}: {e}")
            raise ServiceError("Internal server error")

class CPUService:
    def __init__(self, device_repository_in, cpu_repository_in):
        self.device_repo = device_repository_in
        self.cpu_repo = cpu_repository_in
    
    def get_cpu_data(self, user, device_name):
        """
        Get CPU data for a specific device
        """
        try:
            device = self.device_repo.get_device_by_name(device_name, user)
        except ObjectDoesNotExist as e:
            logger.error(f"ObjectDoesNotExist while fetching device {device_name} for user {user.id}: {e}")
            raise ValueError("Device not found.")
        
        try:
            return self.cpu_repo.get_cpu_data(device)
        except ObjectDoesNotExist as e:
            logger.error(f"ObjectDoesNotExist while fetching CPU data for device {device_name} and user {user.id}: {e}")
            raise ValueError("CPU data not found for the given device.")
        except RepositoryError as e:
            logger.error(f"RepositoryError while fetching CPU data for device {device_name} and user {user.id}: {e}")
            raise ServiceError("Internal server error")
    
    def get_cpu_data_at_timestamp(self, user, device_name, timestamp):
        """
        Get CPU data at a specific timestamp
        """
        try:
            device = self.device_repo.get_device_by_name(device_name, user)
        except ObjectDoesNotExist as e:
            logger.error(f"ObjectDoesNotExist while fetching device {device_name} for user {user.id} at timestamp {timestamp}: {e}")
            raise ValueError("Device not found.")
        
        try:
            return self.cpu_repo.get_cpu_data_at_timestamp(device, timestamp)
        except ObjectDoesNotExist as e:
            logger.error(f"ObjectDoesNotExist while fetching CPU data for device {device_name}, user {user.id} at timestamp {timestamp}: {e}")
            raise ValueError("CPU data not found for the given device.")
        except RepositoryError as e:
            logger.error(f"RepositoryError while fetching CPU data for device {device_name}, user {user.id} at timestamp {timestamp}: {e}")
            raise ServiceError("Internal server error")
    
    def create_cpu_data(self, user, device_name, cpu_data):
        """
        Create CPU data for a device
        """
        try:
            device = self.device_repo.get_device_by_name(device_name, user)
        except ObjectDoesNotExist as e:
            logger.error(f"ObjectDoesNotExist while fetching device {device_name} for user {user.id}: {e}")
            raise ValueError("Device not found.")
        
        try:
            return self.cpu_repo.create_cpu_data(device, cpu_data)
        except IntegrityError as e:
            logger.error(f"IntegrityError while creating CPU data for device {device_name}, user {user.id}: {e}")
            raise ValueError("CPU data already exists or constraint violation")
        except RepositoryError as e:
            logger.error(f"RepositoryError while creating CPU data for device {device_name}, user {user.id}: {e}")
            raise ServiceError("Internal server error")

class MemoryService:
    def __init__(self, device_repository_in, memory_repository_in):
        self.device_repo = device_repository_in
        self.memory_repo = memory_repository_in
    
    def get_memory_data(self, user, device_name):
        """
        Get memory data for a specific device
        """
        try:
            device = self.device_repo.get_device_by_name(device_name, user)
        except ObjectDoesNotExist as e:
            logger.error(f"ObjectDoesNotExist while fetching device {device_name} for user {user.id}: {e}")
            raise ValueError("Device not found.")
        
        try:
            return self.memory_repo.get_memory_data(device)
        except ObjectDoesNotExist as e:
            logger.error(f"ObjectDoesNotExist while fetching memory data for device {device_name}, user {user.id}: {e}")
            raise ValueError("Memory data not found for the given device.")
        except RepositoryError as e:
            logger.error(f"RepositoryError while fetching memory data for device {device_name}, user {user.id}: {e}")
            raise ServiceError("Internal server error")
    
    def get_memory_data_at_timestamp(self, user, device_name, timestamp):
        """
        Get memory data at a specific timestamp
        """
        try:
            device = self.device_repo.get_device_by_name(device_name, user)
        except ObjectDoesNotExist as e:
            logger.error(f"ObjectDoesNotExist while fetching device {device_name} for user {user.id} at timestamp {timestamp}: {e}")
            raise ValueError("Device not found.")
        
        try:
            return self.memory_repo.get_memory_data_at_timestamp(device, timestamp)
        except ObjectDoesNotExist as e:
            logger.error(f"ObjectDoesNotExist while fetching memory data for device {device_name}, user {user.id} at timestamp {timestamp}: {e}")
            raise ValueError("Memory data not found for the given device.")
        except RepositoryError as e:
            logger.error(f"RepositoryError while fetching memory data for device {device_name}, user {user.id} at timestamp {timestamp}: {e}")
            raise ServiceError("Internal server error")
    
    def create_memory_data(self, user, device_name, memory_data):
        """
        Create memory data for a device
        """
        try:
            device = self.device_repo.get_device_by_name(device_name, user)
        except ObjectDoesNotExist as e:
            logger.error(f"ObjectDoesNotExist while fetching device {device_name} for user {user.id}: {e}")
            raise ValueError("Device not found.")
        
        try:
            return self.memory_repo.create_memory_data(device, memory_data)
        except IntegrityError as e:
            logger.error(f"IntegrityError while creating memory data for device {device_name}, user {user.id}: {e}")
            raise ValueError("Memory data already exists or constraint violation")
        except RepositoryError as e:
            logger.error(f"RepositoryError while creating memory data for device {device_name}, user {user.id}: {e}")
            raise ServiceError("Internal server error")

class NetworkService:
    def __init__(self, device_repository_in, network_repository_in):
        self.device_repo = device_repository_in
        self.network_repo = network_repository_in
    
    def get_network_data(self, user, device_name):
        """
        Get network data for a specific device
        """
        try:
            device = self.device_repo.get_device_by_name(device_name, user)
        except ObjectDoesNotExist as e:
            logger.error(f"ObjectDoesNotExist while fetching device {device_name} for user {user.id}: {e}")
            raise ValueError("Device not found.")
        
        try:
            return self.network_repo.get_network_data(device)
        except ObjectDoesNotExist as e:
            logger.error(f"ObjectDoesNotExist while fetching network data for device {device_name}, user {user.id}: {e}")
            raise ValueError("Network data not found for the given device.")
        except RepositoryError as e:
            logger.error(f"RepositoryError while fetching network data for device {device_name}, user {user.id}: {e}")
            raise ServiceError("Internal server error")
    
    def get_network_data_at_timestamp(self, user, device_name, timestamp):
        """
        Get network data at a specific timestamp
        """
        try:
            device = self.device_repo.get_device_by_name(device_name, user)
        except ObjectDoesNotExist as e:
            logger.error(f"ObjectDoesNotExist while fetching device {device_name} for user {user.id} at timestamp {timestamp}: {e}")
            raise ValueError("Device not found.")
        
        try:
            return self.network_repo.get_network_data_at_timestamp(device, timestamp)
        except ObjectDoesNotExist as e:
            logger.error(f"ObjectDoesNotExist while fetching network data for device {device_name}, user {user.id} at timestamp {timestamp}: {e}")
            raise ValueError("Network data not found for the given device.")
        except RepositoryError as e:
            logger.error(f"RepositoryError while fetching network data for device {device_name}, user {user.id} at timestamp {timestamp}: {e}")
            raise ServiceError("Internal server error")
    
    def create_network_data(self, user, device_name, network_data):
        """
        Create network data for a device
        """
        try:
            device = self.device_repo.get_device_by_name(device_name, user)
        except ObjectDoesNotExist as e:
            logger.error(f"ObjectDoesNotExist while fetching device {device_name} for user {user.id}: {e}")
            raise ValueError("Device not found.")
        
        try:
            return self.network_repo.create_network_data(device, network_data)
        except IntegrityError as e:
            logger.error(f"IntegrityError while creating network data for device {device_name}, user {user.id}: {e}")
            raise ValueError("Network data already exists or constraint violation")
        except RepositoryError as e:
            logger.error(f"RepositoryError while creating network data for device {device_name}, user {user.id}: {e}")
            raise ServiceError("Internal server error")