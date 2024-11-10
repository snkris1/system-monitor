from ninja import NinjaAPI
from monitor.api.api import monitor_router
from users.api import auth_router
from rest_framework_simplejwt.authentication import JWTAuthentication


api = NinjaAPI()

api.add_router("/monitor/", monitor_router, auth=JWTAuthentication())   
api.add_router("/auth/", auth_router)