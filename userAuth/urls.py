from django.urls import path
from userAuth.views import *
urlpatterns = [
    path("createuser/",userCreate)
]
