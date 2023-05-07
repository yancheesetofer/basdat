from manager.views import *
from django.urls import path

app_name = "manager"

urlpatterns = [
    path("", index, name="index"),
    path("semuaPertandingan/", listSemuaPertandingan, name="semuaPertandingan"),
    path("profile/", show_profile, name="profile"),
]
