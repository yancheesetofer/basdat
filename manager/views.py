import psycopg2
from django.shortcuts import render
from django.db import connection
from pprint import pprint


# Create your views here.

def get_database():
    conn = psycopg2.connect(database="tk3_sepakbola", user="postgres", password="postgres")
    return conn


def index(request):
    cursor = connection.cursor()
    cursor.execute(
        f"""
        select *
        from peminjaman
        """
    )
    list_peminjaman = []
    all_peminjaman = cursor.fetchall()
    for peminjaman in all_peminjaman:
        peminjaman = {
            "id_manajer": peminjaman[0],
            "start_datetime": peminjaman[1],
            "end_datetime": peminjaman[2],
            "id_stadium": peminjaman[3],
        }
        list_peminjaman.append(peminjaman)
    pprint(peminjaman)
    return render(request, "booking_list.html", context={
        "list_peminjaman": list_peminjaman
    })


def list_pertandingan_manager(request):
    return render(request, "list_pertandingan_penonton.html")


def show_profile(request):
    list_pemain = [
        "Kylian Mbappe",
        "Antoine Griezmann",
        "Olivier Giroud",
        "Marcus Thuram",
        "Youssouf Fofana",
        "Benjamin Pavard",
        "Alphonse Areola",
        "Ibrahima Konaté",
        "Théo Hernandez",
        "Dayot Upamecano",
        "Jean-Clair Todibo",
    ]
    context = {
        "nama_tim": "CSUI FC",
        "asal": "Universitas Depok",
        "list_pemain": list_pemain,
    }
    # jika belum ada tim terdaftar
    # context = {}
    return render(request, "dashboard_manager.html", context)


def registerTim(request):
    return render(request, "registerTim.html")


def detailTim(request):
    return render(request, "detailTim.html")


def pilihPemain(request):
    return render(request, "pemain.html")


def pilihPelatih(request):
    return render(request, "pelatih.html")


def bookingList(request):
    return render(request, "booking_list.html")


def historyRapat(request):
    return render(request, "history_rapat.html")


def scheduleBooking(request):
    return render(request, "schedule_booking.html")


def stadiumBooking(request):
    return render(request, "stadium_booking.html")


def history_rapat_id(request, manajer_id="manajer_id"):
    with connection.cursor() as cursor:
        cursor.execute("""
        SELECT 
                tim_pertandingan_a.Nama_Tim AS Tim_A,
                tim_pertandingan_b.Nama_Tim AS Tim_B,
                panitia.username,
                stadium.nama,
                rapat.Datetime
            FROM Rapat AS rapat
            JOIN Tim_Manajer AS tim_manajer_a ON rapat.Manajer_Tim_A = tim_manajer_a.ID_Manajer
            JOIN Tim_Manajer AS tim_manajer_b ON rapat.Manajer_Tim_B = tim_manajer_b.ID_Manajer
            JOIN Tim AS tim_pertandingan_a ON tim_manajer_a.Nama_Tim = tim_pertandingan_a.Nama_Tim
            JOIN Tim AS tim_pertandingan_b ON tim_manajer_b.Nama_Tim = tim_pertandingan_b.Nama_Tim
            JOIN Panitia AS panitia ON rapat.perwakilan_panitia = panitia.id_panitia
            JOIN user_system AS user_panitia ON panitia.username = user_panitia.username
            JOIN Pertandingan AS pertandingan ON rapat.ID_Pertandingan = pertandingan.ID_Pertandingan
            JOIN Stadium AS stadium ON pertandingan.Stadium = stadium.ID_Stadium
            WHERE rapat.Manajer_Tim_A = %s OR rapat.Manajer_Tim_B = %s
        """, [manajer_id, manajer_id])
        rapats = cursor.fetchall()
    print(rapats)
    return render(request, 'history_rapat.html', {'rapats': rapats})


def history_rapat(request, manajer_id="manajer_id"):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                tim_pertandingan_a.Nama_Tim AS Tim_A,
                tim_pertandingan_b.Nama_Tim AS Tim_B,
                panitia.username,
                stadium.nama,
                rapat.Datetime
            FROM Rapat AS rapat
            JOIN Tim_Manajer AS tim_manajer_a ON rapat.Manajer_Tim_A = tim_manajer_a.ID_Manajer
            JOIN Tim_Manajer AS tim_manajer_b ON rapat.Manajer_Tim_B = tim_manajer_b.ID_Manajer
            JOIN Tim AS tim_pertandingan_a ON tim_manajer_a.Nama_Tim = tim_pertandingan_a.Nama_Tim
            JOIN Tim AS tim_pertandingan_b ON tim_manajer_b.Nama_Tim = tim_pertandingan_b.Nama_Tim
            JOIN Panitia AS panitia ON rapat.perwakilan_panitia = panitia.id_panitia
            JOIN user_system AS user_panitia ON panitia.username = user_panitia.username
            JOIN Pertandingan AS pertandingan ON rapat.ID_Pertandingan = pertandingan.ID_Pertandingan
            JOIN Stadium AS stadium ON pertandingan.Stadium = stadium.ID_Stadium
        """, )
        rapats = cursor.fetchall()
    print(rapats)
    return render(request, 'history_rapat.html', {'rapats': rapats})


def schedule_booking(request):
    return render(request, "schedule_booking.html")


def stadium_booking(request):
    return render(request, "stadium_booking.html")
