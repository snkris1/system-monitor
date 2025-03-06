from channels.middleware import BaseMiddleware
from channels.auth import BaseMiddleware
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.authentication import JWTAuthentication
from urllib.parse import parse_qs
from asgiref.sync import sync_to_async
import logging

logger = logging.getLogger("system_monitor")

class TokenAuthMiddleWare(BaseMiddleware):
    #TODO: DO ASYNC WHERE NECESSARY and BETTER ERROR HANDLING
    #TODO: STUDY SYNC TO ASYNC AND ASYNC IN GENERAL
    async def __call__(self, scope, receive, send):
        query_string = scope['query_string'].decode()
        logger.debug(f"Decoded query string: {query_string}")
        access_token = self._get_token_from_query_string(query_string)

        jwt_authenticator = JWTAuthentication()
        try:
            validated_token = await sync_to_async(jwt_authenticator.get_validated_token)(access_token)

            user = await sync_to_async(jwt_authenticator.get_user)(validated_token)
            scope["user"] = user
            logger.info(f"User '{user.username} authenticated.")

            return await super().__call__(scope, receive, send)
        except InvalidToken:
            logger.info("Invalid token.")
            pass
        except TokenError:
            logger.error("Token error.")
            pass
        except Exception as e:
            logger.error(f"Authentication error: {e}")
            pass
    
    def _get_token_from_query_string(self, query_string):
        parsed_query = parse_qs(query_string)

        access_token = parsed_query.get("access_token", [None])[0]

        if not access_token:
            logger.debug(f"Access token '{access_token}' retrieved.")
        else:
            logger.debug(f"Access token '{access_token}' retrieved.")

        return access_token
    