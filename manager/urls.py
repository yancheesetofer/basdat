from manager.views import *
from django.urls import path

app_name = "manager"

urlpatterns = [
    path("listPeminjaman/", listPeminjaman, name="listPeminjaman"),
    path("semuaPertandingan/", listSemuaPertandingan, name="semuaPertandingan"),
    path("profile/", show_profile, name="profile"),
    path("register/", registerTim, name="daftarTim"),
    path("detail/", detailTim, name="detailTim"),
    path("pemain/", pilihPemain, name="pilihPemain"),
    path("pelatih/", pilihPelatih, name="pilihPelatih"),
    path("historyRapat/", historyRapat, name="historyRapat"),
    path("scheduleBooking/", scheduleBooking, name="scheduleBooking"),
    path("stadiumBooking/", stadiumBooking, name="stadiumBooking"),
    path("bookingConfirmation/", bookingConfirmation, name="bookingConfirmation"),
]
