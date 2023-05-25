from manager.views import *
from django.urls import path

app_name = "manager"

urlpatterns = [
    path("", index, name="index"),
    path("r_list_pertandingan_manager/", list_pertandingan_manager, name="list_pertandingan_manager"),
    path("r_list_pertandingan_manager_all", list_pertandingan_manager_all,
         name="list_pertandingan_manager_all"),
    path("profile/", show_profile, name="profile"),
    path("register/", registerTim, name="daftarTim"),
    path("detail/", detailTim, name="detailTim"),
    path("pemain/", pilihPemain, name="pilihPemain"),
    path("pelatih/", pilihPelatih, name="pilihPelatih"),
    path("r_history_rapat/", history_rapat, name="history_rapat"),
    path("r_history_rapat_all/", history_rapat_all, name="history_rapat_all"),
    path("scheduleBooking/", scheduleBooking, name="scheduleBooking"),
    path("stadiumBooking/", stadiumBooking, name="stadiumBooking"),
    path('makecaptain/', makecaptain, name='makecaptain')
]
