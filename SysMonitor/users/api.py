from django.contrib.auth import get_user_model, authenticate
from ninja import Router
from django.contrib.auth.hashers import make_password
from .schemas import LoginSchema, RegisterSchema, TokenSchema, RefreshSchema
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from ninja.errors import HttpError

auth_router = Router()
User = get_user_model()

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }

@auth_router.post("/refresh", response=TokenSchema)
def refresh_token(request, data: RefreshSchema):
    try:
        refresh = RefreshToken(data.refresh)
        new_tokens = {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }
        return new_tokens
    except TokenError:
        raise TokenError("Invalid or expired token") # can create custom exception handler that does this so its centralized or middleware

@auth_router.post("/login", response=TokenSchema) 
def login(request, data: LoginSchema):
    user = authenticate(request, username=data.email, password=data.password)
    if user is not None:
        tokens = get_tokens_for_user(user)
        return tokens
    else:
        raise HttpError(401, "Invalid email or password")

@auth_router.post("/register", response=TokenSchema)
def register(request, data: RegisterSchema):
    if User.objects.filter(username=data.email).exists():
        return {"error" : "Email already exists"}, 400
    
    user = User.objects.create(
        username=data.email, 
        password=make_password(data.password)
    )
    
    tokens = get_tokens_for_user(user)
    return tokens
    
