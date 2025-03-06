from ninja import NinjaAPI
from monitor.api.api import monitor_router
from users.api import auth_router, protected_auth_router
from users.auth import JWTAuth


api = NinjaAPI()

api.add_router("/monitor/", monitor_router, auth=JWTAuth())   
api.add_router("/auth/", auth_router) # TODO: verify auth for auth endpoints
api.add_router("/auth/", protected_auth_router, auth=JWTAuth())