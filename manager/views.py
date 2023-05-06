from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, "booking_list.html")


def listSemuaPertandingan(request):
    return render(request, "listSemuaPertandingan.html")
