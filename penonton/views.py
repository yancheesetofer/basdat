from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect

# Create your views here.

def index(request):
    return render(request, "awal.html")

def listWaktuStadium(request):
    if (request.method) == 'POST':
        stadium = request.get("stadium")
        tanggal = request.get("tanggal")
        return render(request, 'listWaktuStadium.html', {stadium, tanggal})