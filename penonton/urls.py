from penonton.views import *
from django.urls import path

app_name = "penonton"

urlpatterns = [
    path('', index, name="index")
]
