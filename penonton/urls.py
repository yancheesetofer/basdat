from penonton.views import *
from django.urls import path

app_name = "penonton"

urlpatterns = [
    path("", index, name="index"),
    path("waktu/", listWaktuStadium, name="waktu"),
    path("list/", listPertandingan, name="list"),
    path("tiket/", tiketPertandingan, name="tiket")
]
