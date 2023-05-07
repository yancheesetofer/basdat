from penonton.views import *
from django.urls import path

app_name = "penonton"

urlpatterns = [
    path("pilih/", pilih, name="pilih"),
    path("waktu/", listWaktuStadium, name="waktu"),
    path("pertandinganStadium/", listPertandinganStadium, name="pertandinganStadium"),
    path("tiket/", tiketPertandingan, name="tiket"),
    path("semuaPertandingan/", listSemuaPertandingan, name="semuaPertandingan"),
    path('profile/', show_profile, name='profile' )
]
