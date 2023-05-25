from django.shortcuts import render
from django.conf import settings
from django.db import *

# Create your views here.




def index(request):
    return render(request, "list_pertandingan.html")

def mulai(request):
    return render(request, "mulaiPertandingan.html")

def peristiwa(request):
    return render(request, "peristiwaTimBertanding.html")

def show_profile(request):
    cursor = connection.cursor()
    # cursor.execute("SET search_path TO SIREST")
    cursor.execute("SELECT * FROM rapat")
    list_rapat = []
    allrapat = cursor.fetchall()
    for i in allrapat:
        rapat = {
            'id_pertandingan' : i[0],
            'waktu' : i[1],
            "manajera" : i[3],
            'manajerb' : i[4],
            'isi' : i[5]
        }
        list_rapat.append(rapat)

    context = {
        'list_rapat' : list_rapat
    }

    return render(request, 'dashboard_panitia.html')

def manage_pertandingan(request):
    context = {
        'isLengkap' : True
    }
    return render(request, "manage_pertandingan.html", context)

def list_peristiwa(request):
    return render(request, "list_peristiwa.html")


def buat_pertandingan(request):
    return render(request, "buat_pertandingan.html")

def list_pertandingan(request):
    return render(request, "list_pertandingan.html")

def mulai_rapat(request):
    return render(request, "mulai_rapat.html")

def nota_rapat(request):
    return render(request, "nota_rapat.html")

def submit_pertandingan(request):
    return render(request, "submit_pertandingan.html")

def schedule_list(request):
    return render(request, "schedule_list.html")
