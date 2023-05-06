from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect

# Create your views here.


def index(request):
    return render(request, "pilihStadium.html")


def listWaktuStadium(request):
    return render(request, "listWaktuStadium.html")


def listPertandingan(request):
    return render(request, "listPertandingan.html")


def tiketPertandingan(request):
    return render(request, "beliTiket.html")
