from manager.views import *
from django.urls import path

app_name = 'panitia'

urlpatterns = [
    path('', index ,name="index")
]
