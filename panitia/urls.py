from panitia.views import *
from django.urls import path

app_name = 'panitia'

urlpatterns = [
    path('', index ,name="index"),
    path('mulai/', mulai, name="mulai"),
    path('peristiwa/', peristiwa, name="peristiwa")
]
