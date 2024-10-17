import jwt
from django.conf.global_settings import SECRET_KEY
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
class JWTAuth(BaseAuthentication):
    def authenticate(self, request):
        token=request.COOKIES.get('access_token')
        if not token:
            raise AuthenticationFailed("access_token missing from cookies")
        try:
            decoded=jwt.decode(token,SECRET_KEY,algorithms=["HS256"])
            return (decoded,None)
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token Expired")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid access_token")
      