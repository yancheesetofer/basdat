from user.views import *
from django.urls import path

app_name = "user"

urlpatterns = [
    path("register/", register, name="index"),
    path("register/manager", register_manager, name="register_manager"),
    path("register/penonton", register_penonton, name="register_penonton"),
    path("register/panitia", register_panitia, name="register_panitia"),
    path("",homePage, name="homePage"),
    path("login",loginPage, name="loginPage"),
]
