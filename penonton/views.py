import uuid

from django.db import connection
from django.shortcuts import render, redirect
from .forms import StadiumForm, PembayaranForm


# Create your views here.
def show_profile(request):
    pertandingan1 = {
        "id": 11,
        "waktu_mulai": "Minggu, 7 Mei 2023 7:00 pm",
        "waktu_selesai": "Minggu, 7 Mei 2023 8:30 pm",
        "stadium": "Anfield",
    }
    pertandingan2 = {
        "id": 13,
        "waktu_mulai": "Selasa, 9 Mei 2023 7:00 pm",
        "waktu_selesai": "Selasa, 9 Mei 2023 8:30 pm",
        "stadium": "Old Trafford",
    }
    list_pertandingan = [pertandingan1, pertandingan2]

    context = {"list_pertandingan": list_pertandingan}
    context = {}
    return render(request, "dashboardPenonton.html", context)


def pilih_stadium(request):
    if request.method == 'POST':
        form = StadiumForm(request.POST)
        if form.is_valid():
            request.session['stadium'] = form.cleaned_data['stadium']
            request.session['tanggal'] = form.cleaned_data['tanggal']
            return redirect('list_waktu_stadium')  # redirect to next page
    else:
        form = StadiumForm()
    return render(request, 'pilih_stadium.html', {'form': form})


def list_waktu_stadium(request):
    stadium = request.session.get('stadium')
    tanggal = request.session.get('tanggal')
    if request.method == 'POST':
        waktu = request.POST['waktu']
        request.session['waktu'] = waktu
        return redirect('pilih_pertandingan')  # redirect to next page
    else:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT start_datetime, end_datetime 
                FROM Pertandingan 
                WHERE Stadium = %s AND DATE(start_datetime) = %s
            """, [stadium, tanggal])
            waktu_list = cursor.fetchall()
    return render(request, 'list_waktu_stadium.html', {'waktu_list': waktu_list})


def pilih_pertandingan(request):
    stadium = request.session.get('stadium')
    tanggal = request.session.get('tanggal')
    waktu = request.session.get('waktu')
    if request.method == 'POST':
        pertandingan = request.POST['pertandingan']
        request.session['pertandingan'] = pertandingan
        return redirect('beli_tiket')  # redirect to next page
    else:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT t1.Nama_Tim, t2.Nama_Tim 
                FROM Tim_Pertandingan tp1
                JOIN Tim_Pertandingan tp2 ON tp1.ID_Pertandingan = tp2.ID_Pertandingan
                JOIN Tim t1 ON tp1.Nama_Tim = t1.Nama_Tim
                JOIN Tim t2 ON tp2.Nama_Tim = t2.Nama_Tim
                WHERE tp1.Nama_Tim <> tp2.Nama_Tim AND tp1.ID_Pertandingan IN (
                    SELECT ID_Pertandingan 
                    FROM Pertandingan 
                    WHERE Stadium = %s AND DATE(start_datetime) = %s AND TIME(start_datetime) = %s
                )
            """, [stadium, tanggal, waktu])
            pertandingan_list = cursor.fetchall()
    return render(request, 'pilih_pertandingan.html', {'pertandingan_list': pertandingan_list})


def beli_tiket(request):
    if request.method == 'POST':
        form = PembayaranForm(request.POST)
        if form.is_valid():
            jenis_tiket = form.cleaned_data['jenis_tiket']
            pembayaran = form.cleaned_data['pembayaran']
            # Generate receipt number
            nomor_receipt = uuid.uuid4().hex
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO Pembelian_Tiket(Nomor_Receipt, ID_Penonton, Jenis_Tiket, Jenis_Pembayaran, ID_Pertandingan) 
                    VALUES (%s, (SELECT ID_Penonton FROM Penonton WHERE Username = %s), %s, %s, 
                    (SELECT ID_Pertandingan FROM Pertandingan WHERE Stadium = (SELECT ID_Stadium FROM Stadium WHERE Nama = %s) AND DATE(Start_Datetime) = %s AND TIME(Start_Datetime) = %s))
                """, [nomor_receipt, request.user.username, jenis_tiket, pembayaran, request.session['stadium'], request.session['tanggal'], request.session['waktu']])
            return redirect('dashboard')  # redirect to dashboard page
    else:
        form = PembayaranForm()
    return render(request, 'beli_tiket.html', {'form': form})
