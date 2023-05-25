from penonton.views import *
from django.urls import path

app_name = "penonton"

urlpatterns = [
    path('profile/', show_profile, name='profile'),
    path('cr_pembelian_tiket/pilih_stadium/', pilih_stadium, name='pilih_stadium'),
    path('cr_pembelian_tiket/list_waktu_stadium/', list_waktu_stadium, name='list_waktu_stadium'),
    path('cr_pembelian_tiket/list_pertandingan/', pilih_pertandingan, name='pilih_pertandingan'),
    path('cr_pembelian_tiket/beli_tiket/', beli_tiket, name='beli_tiket'),
]
