from ninja import NinjaAPI
from monitor.api import router as monitor_router
from users.api import router as auth_router
from rest_framework_simplejwt.authentication import JWTAuthentication


api = NinjaAPI()

api.add_router("/monitor/", monitor_router, auth=JWTAuthentication())   
api.add_router("/auth/", auth_router)