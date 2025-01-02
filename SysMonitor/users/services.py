from ninja.errors import HttpError
from django.contrib.auth import get_user_model

User = get_user_model()

class ServiceError(Exception):
    """Base class for all service errors."""
    pass

def get_user_by_id(user_id):
    try:
        user = User.objects.get(id=user_id)
        return user
    except User.DoesNotExist:
        raise ServiceError(f"User with id {user_id} does not exist")