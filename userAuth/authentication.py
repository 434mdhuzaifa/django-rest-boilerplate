import jwt
from django.conf.global_settings import SECRET_KEY
from rest_framework.authentication import BaseAuthentication
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import APIException
UserModel = get_user_model()

class CustomAuthException(APIException):
    default_code="auth failed"
    default_detail="Auth Failed"
    def __init__(self, detail=None, code=None,status_code=None):
        self.code=code if code is not None else self.default_code
        self.detail={"detail":detail}
        self.status_code = status_code if status_code is not None else 401

class JWTAuth(BaseAuthentication):
    def authenticate(self, request):
        token = request.COOKIES.get("access_token")
        if not token:
            raise CustomAuthException("access_token missing from cookies",status_code=400)
        try:
            decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user = UserModel.objects.get(username=decoded.get("username", ""))
            return (user, None)
        except jwt.ExpiredSignatureError:
            raise CustomAuthException("Token Expired",status_code=401)
        except jwt.InvalidTokenError:
            raise CustomAuthException("Invalid access_token",status_code=401)
        except ObjectDoesNotExist:
            raise CustomAuthException("User not found",status_code=404  )
