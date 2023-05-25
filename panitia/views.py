from django.shortcuts import render
from django.conf import settings
from django.db import *
from django.http import HttpResponse
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
    daftar_stadium={}
    try:
        cursor = connection.cursor()
        query = """
                SELECT nama
FROM stadium;
            """
        cursor.execute(query)
        daftar_stadium = cursor.fetchall()
        
    finally:
        # closing database connection.
        if connection:
            connection.commit()
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
    
    context = {
            'ds':daftar_stadium}
    return render(request, "buat_pertandingan.html",context)

def list_pertandingan(request):
    daftar_pertandingan={}
    try:
        cursor = connection.cursor()
        query = """
                SELECT string_agg(DISTINCT nama_tim, ' VS ' )
FROM tim_pertandingan
GROUP BY id_pertandingan;
            """
        cursor.execute(query)
        daftar_pertandingan = cursor.fetchall()
        
        
    finally:
        # closing database connection.
        if connection:
            connection.commit()
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
    
    list_tim=zip(daftar_pertandingan[0:4],daftar_pertandingan[4:8])
    context = {
            'lt':list_tim}
    
    return render(request, "list_pertandingan.html",context)

def mulai_rapat(request):
    return render(request, "mulai_rapat.html")

def nota_rapat(request):
    return render(request, "nota_rapat.html")

def submit_pertandingan(request):
    daftar_wasit={}
    daftar_tim={}
    try:
        cursor = connection.cursor()
        query = """
                Select distinct W.id_wasit
                From wasit W
                WHERE W.id_wasit NOT IN 
                (SELECT WB.id_wasit From wasit_bertugas WB);
            """
        cursor.execute(query)
        daftar_wasit = cursor.fetchall()
        
        cursor = connection.cursor()
        query = """
                Select nama_tim
                From tim;
            """
        cursor.execute(query)
        daftar_tim = cursor.fetchall()
        
    finally:
        # closing database connection.
        if connection:
            connection.commit()
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

    context = {
            'dw':daftar_wasit,
            'dt1':daftar_tim[0:15],
            'dt2':daftar_tim[16:]}
    return render(request, "submit_pertandingan.html",context)

def schedule_list(request):
    return render(request, "schedule_list.html")
