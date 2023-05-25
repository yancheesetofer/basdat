from datetime import date
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
    cursor = connection.cursor()
    listResponseWanted = []
    
    try:
        cursor.execute(
            f"""
            select distinct id_pertandingan
            from tim_pertandingan
            """
        )
    except Exception as e:
        cursor = connection.cursor()
    
    listIDPertandingan = cursor.fetchall()

    for idPertandingan in listIDPertandingan:
        id = idPertandingan[0]
        try:
            cursor.execute(
                f"""
                select date(start_datetime), cast(start_datetime as time), cast(end_datetime as time), stadium 
                from pertandingan
                where id_pertandingan = %s
                """,
                [id]
            )
        except Exception as e:
            cursor = connection.cursor()

        list_pertandingan = cursor.fetchall()


        exactdate = list_pertandingan[0][0]
        startDate = list_pertandingan[0][1]
        endDate = list_pertandingan[0][2]
        id_stadium = list_pertandingan[0][3]

        try:
            cursor.execute(
                f"""
                select nama_tim
                from tim_pertandingan
                where id_pertandingan = %s
                """,
                [id]
            )
        except Exception as e:
            cursor = connection.cursor()
        
        keduaTim = cursor.fetchall()

        try:
            cursor.execute(
                f"""
                select nama
                from stadium
                where id_stadium = %s
                """,
                [id_stadium]
            )
        except Exception as e:
            cursor = connection.cursor()
        namaStadium = cursor.fetchone()

        try:
            cursor.execute(
                f"""
                select *
                from rapat
                where id_pertandingan = %s
                """,
                [id]
            )
        except Exception as e:
            cursor = connection.cursor()
        rapat = cursor.fetchone()
        if rapat != None:
            result= {
            "timBertanding": keduaTim[0][0] + " vs " + keduaTim[1][0],
            "stadium": namaStadium[0],
            "tanggalWaktu": str(exactdate) + " " + str(startDate) + " - " + str(endDate),
            "isPertandingan": id,
            "rapat": rapat[0]
            }
        else :
            result= {
                "timBertanding": keduaTim[0][0] + " vs " + keduaTim[1][0],
                "stadium": namaStadium[0],
                "tanggalWaktu": str(exactdate) + " " + str(startDate) + " - " + str(endDate),
                "isPertandingan": id,
                "rapat": None
        }
        listResponseWanted.append(result)


    return render(request, "mulai_rapat.html", {
        "listResponse": listResponseWanted
    })

def nota_rapat(request):
    return render(request, "nota_rapat.html")

def submit_pertandingan(request):
    return render(request, "submit_pertandingan.html")

def schedule_list(request):
    return render(request, "schedule_list.html")
