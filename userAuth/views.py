from rest_framework.views import APIView
from userAuth.serializers import *
from django.template.loader import render_to_string
from common.utility import (
    SendMsgResponse,
    SendResponse,
    SendErrorResponse,
    generateToken,
)
from rest_framework.request import HttpRequest
from rest_framework.serializers import ValidationError
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from userAuth.models import ResetToken
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
import jwt
from django.utils import timezone
from django.conf.global_settings import SECRET_KEY
# Create your views here
class UserView(APIView):
    permission_classes = [IsAuthenticated]
    def get_authenticators(self):
        if self.request.method=="POST":
            return []    
        return super().get_authenticators()
    def get_permissions(self):
        if self.request.method == "POST":
            return [AllowAny]
        return super().get_permissions()

    def post(self, request):
        try:
            userData = UserInputSerializers(request.data)
            validate_data = userData.run_validation(userData.data)
            userData.create(validate_data)
            return SendMsgResponse("User creation successfull", 201)
        except ValidationError as e:
            return SendErrorResponse(e, 400)
        except Exception as e:
            return SendErrorResponse(e, 500)

    def get(self, request: HttpRequest):
        try:
            UserModel = get_user_model()
            username = request.GET.get("username", False)
            userid = request.GET.get("userid", False)
            email = request.GET.get("email", False)
            user = False
            if username:
                user = UserModel.objects.get(username=username)
            if userid != False:
                user = UserModel.objects.get(id=userid)
            if email:
                user = UserModel.objects.get(email=email)
            if user:
                userData = UserSerializers(user)
                return SendResponse(userData.data, 200)
            else:
                return SendMsgResponse(
                    "username or userid or email should be in the params", 400
                )
        except ObjectDoesNotExist as e:
            return SendErrorResponse(e, 404)
        except Exception as e:
            return SendErrorResponse(e, 500)

    def put(self, request, pk=None):
        try:
            if pk:
                UserModel = get_user_model()
                user = UserModel.objects.get(id=pk)
                serializer = UserSerializers(user, data=request.data, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return SendResponse(serializer.data, 202)
            return SendErrorResponse("invalid Id", 400)
        except ObjectDoesNotExist as e:
            return SendErrorResponse("User not found", 404)
        except ValidationError as e:
            return SendErrorResponse(e, 400)
        except Exception as e:
            return SendErrorResponse(e, 500)


class UserLogin(APIView):
    permission_classes = [AllowAny]
    authentication_classes=[]

    def post(self, request: HttpRequest):
        try:
            UserModel = get_user_model()
            loginData = UserLoginSerializers(request.data)
            validate_data = loginData.run_validation(loginData.data)
            loginData.validate(validate_data)
            user = False
            email = validate_data.get("email", False)
            username = validate_data.get("username", False)
            if email:
                user = UserModel.objects.get(email=email)
            if username:
                user = UserModel.objects.get(username=username)
            if user:
                user = authenticate(
                    username=user.username, password=validate_data.get("password")
                )
                if user:
                    userData = UserSerializers(user)
                    timeExp = timezone.now() + timezone.timedelta(minutes=15)
                    token = jwt.encode(userData.data, SECRET_KEY)
                    response = Response(userData.data, 200)
                    response.set_cookie("access_token", token, expires=timeExp,samesite="None",httponly=True,secure=True)
                    return response
                return SendErrorResponse("Password icorrect", 400)
            return SendErrorResponse("User not found", 400)
        except Exception as e:
            return SendErrorResponse(e, 500)


class PasswordReset(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            email = request.data.get("email", False)
            if email:
                UserModel = get_user_model()
                user = UserModel.objects.get(email=email)
                token = ResetToken.objects.filter(user=user, isvalid=True).last()
                if not token or (token and token.is_expired):
                    if token:
                        token.isvalid = False
                        token.save()
                    pin = generateToken(5)
                    token = ResetToken(user=user, token=str(pin))
                    token.save()
                    html_message = render_to_string(
                        "emailTemplate.html",
                        context={
                            "username": user.username,
                            "brand": "django-rest-boilterplate",
                            "pin": pin,
                            "website": "www.website.com",
                            "address1": "House-16, Road-12, (4th floor), Nikunja-2",
                            "address2": "Khilkhet, Dhaka-1229",
                            "link": f"http://localhost:5173/passwordreset?email={user.email}&pin={pin}",
                        },
                    )
                    message = render_to_string(
                        "emailTemplate.txt",
                        context={
                            "username": user.username,
                            "brand": "django-rest-boilterplate",
                            "pin": pin,
                            "website": "www.website.com",
                            "address1": "House-16, Road-12, (4th floor), Nikunja-2",
                            "address2": "Khilkhet, Dhaka-1229",
                            "link": f"http://localhost:5173/passwordreset?email={user.email}&pin={pin}",
                        },
                    )

                    mailFlag = send_mail(
                        subject=f"Password Reset for {user.username}",
                        recipient_list=[user.email],
                        fail_silently=True,
                        html_message=html_message,
                        message=message,
                        from_email=None,
                    )
                    if mailFlag:
                        return SendMsgResponse("Mail send successfully", 200)
                    raise Exception("Mail send failed")
                return SendMsgResponse(
                    f"Your Previous token's validity still {token.remaining_time} left",
                    400,
                )
            return SendMsgResponse("Email not found", 400)
        except ObjectDoesNotExist as e:
            return SendErrorResponse("User not found", 404)
        except Exception as e:
            return SendErrorResponse(e, 500)


class ResetPassword(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            resetData = ResetPasswordSerializers(request.data)
            validate_data = resetData.run_validation(resetData.data)
            resetData.validate(validate_data)
            isSuccess, userOrmsg = resetData.update(validate_data)
            if isSuccess:
                userData = UserSerializers(userOrmsg)
                return SendResponse(userData.data)
            return SendMsgResponse(userOrmsg, 400)
        except ValidationError as e:
            return SendErrorResponse(e, 400)
        except Exception as e:
            return SendErrorResponse(e)
