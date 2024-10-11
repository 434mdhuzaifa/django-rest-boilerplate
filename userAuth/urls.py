from django.urls import path
from userAuth.views import *
urlpatterns = [
    path("user/",UserView.as_view()),
    path("userlogin/",userLogin),
    path("reset-password-otp/",passwordReset),
    path("reset-password-data/",resetPassword)
]
