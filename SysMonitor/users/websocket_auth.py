from channels.middleware import BaseMiddleware
from channels.auth import AuthMiddlewareStack

class TokenAuthMiddleWare(AuthMiddlewareStack):
    pass