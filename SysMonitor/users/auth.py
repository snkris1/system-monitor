from ninja.security import HttpBearer
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from django.contrib.auth.models import User
from rest_framework_simplejwt.authentication import JWTAuthentication

class JWTAuth(HttpBearer):
    def authenticate(self, request, token):
        jwt_authenticator = JWTAuthentication()
        try:
            validated_token = jwt_authenticator.get_validated_token(token)
            user = jwt_authenticator.get_user(validated_token)
            request.token = validated_token
            return user
        except Exception as e:
            raise AuthenticationFailed(f"Authentication failed.")
        