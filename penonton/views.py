import uuid

from django.db import connection
from django.shortcuts import render, redirect
# from .forms import StadiumForm, PembayaranForm
# import psycopg2


def get_database():
    conn = connection
    return conn


# Create your views here.
def show_profile(request):
    cursor = connection.cursor()
    idPenonton = request.session.get("id")
    try:
        cursor.execute(
            f"""
            select *
            from non_pemain
            where id = %s
            """,
            [idPenonton]
        )
    except Exception as e:
        cursor = connection.cursor()
    dataPenonton = cursor.fetchall()
    namaDepan = dataPenonton[0][1]
    namaBelakang = dataPenonton[0][2]
    nomorHP = dataPenonton[0][3]
    email = dataPenonton[0][4]
    alamat = dataPenonton[0][5]

    try:
        cursor.execute(
            f"""
            select status
            from status_non_pemain
            where id_non_pemain = %s
            """,
            [idPenonton]
        )
    except Exception as e:
        cursor = connection.cursor()
    dataStatus = cursor.fetchone()

    panitia = {
        'namaDepan' : namaDepan,
        'namaBelakang' : namaBelakang,
        'nomorHP' : nomorHP,
        'email' : email,
        'alamat' : alamat,
        'status' : dataStatus[0]
    }

    list_pertandingan = []

    try:
        cursor.execute(
            f"""
            select *
            from pertandingan
            """
        )
    except Exception as e:
        cursor = connection.cursor()
    dataPertandingan = cursor.fetchall()

    for pertandingan in dataPertandingan:
        idPertandingan = pertandingan[0]
        startDatetime = pertandingan[1]
        end_datetime = pertandingan[2]
        id_stadium = pertandingan[3]

        print(idPertandingan)
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
        dataStadium = cursor.fetchone()
        namaStadium = dataStadium[0]

        try:
            cursor.execute(
                f"""
                select nama_tim
                from tim_pertandingan
                where id_pertandingan = %s
                """,
                [idPertandingan]
            )
        except Exception as e:
            cursor = connection.cursor()
        dataPetanding = cursor.fetchall()
        print(dataPetanding)
        if dataPetanding:
            print(dataPetanding[0])
            timA = dataPetanding[0][0]
            timB = dataPetanding[1][0]
            judul = timA + " vs " + timB
        else:
            continue
            judul = "Tim yang bertanding belum ditentukan"
        # print(dataPetanding[0])
        # print(dataPetanding[1])

        detailPertandingan = {
            'judul' : judul,
            'namaStadium' : namaStadium,
            'startDate' : startDatetime,
            'endDate' : end_datetime
        }
        list_pertandingan.append(detailPertandingan)

    context = {
        "list_pertandingan_penonton": list_pertandingan,
        "panitia" : panitia
    }

    return render(request, "dashboardPenonton.html", context)


# def pilih_stadium(request):
#     if request.method == 'POST':
#         form = StadiumForm(request.POST)
#         if form.is_valid():
#             request.session['stadium'] = form.cleaned_data['stadium']
#             request.session['tanggal'] = form.cleaned_data['tanggal'].strftime('%Y-%m-%d')
#             return redirect('/penonton/cr_pembelian_tiket/list_waktu_stadium')  # redirect to next page
#     else:
#         form = StadiumForm()
#     return render(request, 'pilih_stadium.html', {'form': form})


def list_waktu_stadium(request):
    stadium = request.session.get('stadium')
    tanggal = request.session.get('tanggal')
    if request.method == 'POST':
        waktu = request.POST['waktu']
        request.session['waktu'] = waktu
        request.session.modified = True
        return redirect('/penonton/cr_pembelian_tiket/pilih_pertandingan/')  # redirect to next page
    else:
        with get_database().cursor() as cursor:
            cursor.execute("""
                SELECT start_datetime, end_datetime 
                FROM Pertandingan 
                WHERE Stadium = %s AND DATE(start_datetime) = %s; 
            """, [stadium, tanggal])
            waktu_list = cursor.fetchall()
    if not waktu_list:
        waktu_list = [(" ", " ")]
    print(f"WAKTU LIST{waktu_list} ")
    return render(request, 'list_waktu_stadium.html', {'waktu_list': waktu_list})


def pilih_pertandingan(request):
    stadium = request.session.get('stadium')
    tanggal = request.session.get('tanggal')
    if request.method == 'POST':
        pertandingan = request.POST['pertandingan']
        request.session['pertandingan'] = pertandingan
        request.session.modified = True
        return redirect('/penonton/cr_pembelian_tiket/beli_tiket')  # redirect to next page
    else:
        print("STADIUM TANGGAL", stadium if stadium else "kosong", tanggal if tanggal else "kosong")
        with get_database().cursor() as cursor:
            cursor.execute("""
                SELECT t1.Nama_Tim, t2.Nama_Tim 
                FROM Tim_Pertandingan tp1
                JOIN Tim_Pertandingan tp2 ON tp1.ID_Pertandingan = tp2.ID_Pertandingan
                JOIN Tim t1 ON tp1.Nama_Tim = t1.Nama_Tim
                JOIN Tim t2 ON tp2.Nama_Tim = t2.Nama_Tim
                WHERE tp1.Nama_Tim <> tp2.Nama_Tim AND tp1.ID_Pertandingan IN (
                    SELECT ID_Pertandingan 
                    FROM Pertandingan p
                    WHERE p.Stadium = %s AND DATE(p.start_datetime) = DATE(%s)
                )
            """, [stadium, tanggal])
            pertandingan_list = cursor.fetchall()
    return render(request, 'pilih_pertandingan.html', {'pertandingan_list': pertandingan_list})


# def beli_tiket(request):
#     if request.method == 'POST':
#         form = PembayaranForm(request.POST)
#         if form.is_valid():
#             jenis_tiket = form.cleaned_data['jenis_tiket']
#             pembayaran = form.cleaned_data['pembayaran']
#             # Generate receipt number
#             nomor_receipt = uuid.uuid4().hex
#             with connection.cursor() as cursor:
#                 cursor.execute("""
#                     INSERT INTO Pembelian_Tiket(Nomor_Receipt, ID_Penonton, Jenis_Tiket, Jenis_Pembayaran, ID_Pertandingan) 
#                     VALUES (%s, (SELECT ID_Penonton FROM Penonton WHERE Username = %s), %s, %s, 
#                     (SELECT ID_Pertandingan 
#                         FROM Pertandingan 
#                         WHERE Stadium = (SELECT ID_Stadium FROM Stadium WHERE Nama = %s)
#                         AND DATE(Start_Datetime) = DATE(%s)))
#                 """, [nomor_receipt, request.user.username, jenis_tiket, pembayaran, request.session['stadium'],
#                       request.session['tanggal']])
#             return redirect('/penonton/profile')  # redirect to dashboard page
#     else:
#         form = PembayaranForm()
#     return render(request, 'beli_tiket.html', {'form': form})


def list_pertandingan_penonton(request):
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
    return render(request, 'list_pertandingan_penonton.html', {'pertandingan': pertandingan})
