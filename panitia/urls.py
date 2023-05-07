from panitia.views import *
from django.urls import path

app_name = 'panitia'

urlpatterns = [
    path('', index ,name="index"),
    path('mulai/', mulai, name="mulai"),
    path('peristiwa/', peristiwa, name="peristiwa"),
    path('profile/', show_profile, name="profile"),
    path('manage/', manage_pertandingan, name="manage_pertandingan"),
    path('peristiwa/list/', list_peristiwa, name="list_peristiwa")
]
