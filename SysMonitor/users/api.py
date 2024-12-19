from django.contrib.auth import get_user_model, authenticate
from ninja import Router
from django.contrib.auth.hashers import make_password
from .schemas import LoginSchema, RegisterSchema, TokenSchema, RefreshSchema, LogoutSchema
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from ninja.errors import HttpError
from rest_framework_simplejwt.tokens import BlacklistMixin

auth_router = Router()
protected_auth_router = Router()
User = get_user_model()

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }

# TODO: IMPROVE ERROR HANDLING IN ENDPOINTS
# TODO: FIX THAT WHEN USER SIGNS UP THERE EMAIL IS SAVED AS USERNAME
# TODO: ADD ERROR HANDLING MIDDLEWARE AND LOGGING

# Public endpoints (no authentication required)
# TODO: MAY BE AN ISSUE HERE WITH USERNAME=DATA.EMAIL
@auth_router.post("/login", response=TokenSchema) 
def login(request, data: LoginSchema):
    user = authenticate(request, username=data.email, password=data.password)
    if user is not None:
        tokens = get_tokens_for_user(user)
        return tokens
    else:
        raise HttpError(401, "Invalid email or password")
    


# TODO: INCLUDE OPTIONAL USERNAME FIELD. AND FIGURE OUT USER EMAIL VS USERNAME SCHENAIGANS
@auth_router.post("/register", response=TokenSchema)
def register(request, data: RegisterSchema):
    if User.objects.filter(username=data.email).exists():
        raise HttpError(400, "Email already exists")
    
    user = User.objects.create(
        email=data.email, 
        password=make_password(data.password)
    )
    
    tokens = get_tokens_for_user(user)
    return tokens

# Protected endpoints (require valid access token)
@protected_auth_router.post("/refresh", response=TokenSchema)
def refresh_token(request, data: RefreshSchema):
    try:
        refresh = RefreshToken(data.refresh)
        new_tokens = {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }
        return new_tokens
    except TokenError:
        raise HttpError(401, "Invalid or expired token") # can create custom exception handler that does this so its centralized or middleware

@protected_auth_router.delete("/logout")
def logout(request, data: LogoutSchema):
    try:
        refresh_token = data.refresh_token
        token = RefreshToken(refresh_token)
        token.check_blacklist()
        token.blacklist()
        return {"message": "Logout successful"}
    except Exception:
        raise HttpError(400, "Logout failed")