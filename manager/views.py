import psycopg2
from django.shortcuts import render
from django.db import connection
from pprint import pprint


# Create your views here.

def get_database():
    conn = connection.connect(database="tk3_sepakbola", user="postgres", password="postgres")
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


def list_pertandingan_manager_all(request):
    with get_database().cursor() as cursor:
        cursor.execute("""
            SELECT 
                T1.Nama_Tim || ' vs ' || T2.Nama_Tim AS "Tim Bertanding",
                S.Nama AS "Stadium",
                P.Start_Datetime || ' - ' || P.End_Datetime AS "Tanggal dan Waktu"
            FROM 
                Tim_Pertandingan TP1 
                JOIN Tim T1 ON TP1.Nama_Tim = T1.Nama_Tim
                JOIN Tim_Pertandingan TP2 ON TP1.ID_Pertandingan = TP2.ID_Pertandingan AND TP1.Nama_Tim != TP2.Nama_Tim
                JOIN Tim T2 ON TP2.Nama_Tim = T2.Nama_Tim
                JOIN Pertandingan P ON TP1.ID_Pertandingan = P.ID_Pertandingan
                JOIN Stadium S ON P.Stadium = S.ID_Stadium;
        """)
        pertandingan = cursor.fetchall()
    print("pertandingan", pertandingan)
    return render(request, 'list_pertandingan_manager.html', {'pertandingan': pertandingan})


def list_pertandingan_manager(request):
    with get_database().cursor() as cursor:
        cursor.execute("""
            SELECT 
                T1.Nama_Tim || ' vs ' || T2.Nama_Tim AS "Tim Bertanding",
                S.Nama AS "Stadium",
                P.Start_Datetime || ' - ' || P.End_Datetime AS "Tanggal dan Waktu"
            FROM 
                Tim_Pertandingan TP1 
                JOIN Tim T1 ON TP1.Nama_Tim = T1.Nama_Tim
                JOIN Tim_Pertandingan TP2 ON TP1.ID_Pertandingan = TP2.ID_Pertandingan AND TP1.Nama_Tim != TP2.Nama_Tim
                JOIN Tim T2 ON TP2.Nama_Tim = T2.Nama_Tim
                JOIN Pertandingan P ON TP1.ID_Pertandingan = P.ID_Pertandingan
                JOIN Stadium S ON P.Stadium = S.ID_Stadium
            WHERE %s in 
            (SELECT username FROM tim_manajer
             JOIN manajer m on tim_manajer.id_manajer = m.id_manajer
             WHERE 
                (t1.nama_tim = tim_manajer.nama_tim OR t2.nama_tim = tim_manajer.nama_tim));
        """, [request.session["username"]])
        pertandingan = cursor.fetchall()

    print("pertandingan", pertandingan)
    return render(request, 'list_pertandingan_manager.html', {'pertandingan': pertandingan})


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

def scheduleBooking(request):
    return render(request, "schedule_booking.html")


def stadiumBooking(request):
    return render(request, "stadium_booking.html")


def history_rapat(request):
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
            JOIN manajer As manajer_a ON rapat.manajer_tim_a = manajer_a.id_manajer
            JOIN manajer As manajer_b ON rapat.manajer_tim_b = manajer_b.id_manajer
            WHERE manajer_a.username = %s OR manajer_b.username = %s
        """, [request.session["username"], request.session["username"]])
        rapats = cursor.fetchall()
    print(rapats)
    return render(request, 'history_rapat.html', {'rapats': rapats})


def history_rapat_all(request, manajer_id="manajer_id"):
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
