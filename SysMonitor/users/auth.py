from ninja.security import HttpBearer
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from ninja.errors import HttpError
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
        except InvalidToken:
            raise HttpError(401, "Invalid token. Authentication failed.")
        except TokenError:
            raise HttpError(401, "Token error. Authentication failed.")
        except Exception as e:
            raise HttpError(500, f"Internal server error: {str(e)}")