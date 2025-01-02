"""
ASGI config for SysMonitor project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from users.websocket_auth import TokenAuthMiddleWare
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from monitor.routing import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SysMonitor.settings')

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": (
            TokenAuthMiddleWare(URLRouter(websocket_urlpatterns))
        ),
    }
)
