from django.urls import path
from userAuth.views import *
urlpatterns = [
    path("user/",UserView.as_view()),
    path("user/<int:pk>/",UserView.as_view()),
    path("userlogin/",UserLogin.as_view()),
    path("reset-password-otp/",PasswordReset.as_view()),
    path("reset-password-data/",ResetPassword.as_view())
]
