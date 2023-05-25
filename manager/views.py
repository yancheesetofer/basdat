from django.shortcuts import redirect, render
from django.db import *
from pprint import pprint
import datetime
from django.http import HttpResponseForbidden
from django.contrib import messages

# Create your views here.


def listPeminjaman(request):
    cursor = connection.cursor()
    id_manajer = request.session.get("id")
    cursor.execute(
        f"""
        select *
        from peminjaman
        where id_manajer = %s
        """,
        [id_manajer],
    )
    list_peminjaman = []
    all_peminjaman = cursor.fetchall()
    for peminjaman in all_peminjaman:
        start_datetime = peminjaman[1]
        end_datetime = peminjaman[2]
        try:
            cursor.execute(
                f"""
                select *
                from stadium
                where id_stadium = %s
                """,
                [peminjaman[3]],
            )
        except Exception as e:
            cursor = connection.cursor()

        all_detail_peminjaman = cursor.fetchall()
        for detailPeminjaman in all_detail_peminjaman:
            namaStadium = detailPeminjaman[1]

        dataPeminjaman = {
            "namaStadium": namaStadium,
            "startDate": start_datetime,
            "endDate": end_datetime,
        }

        list_peminjaman.append(dataPeminjaman)
    pprint(list_peminjaman)
    print("hai")
    return render(
        request, "booking_list.html", context={"list_peminjaman": list_peminjaman}
    )


def listSemuaPertandingan(request):
    return render(request, "listSemuaPertandingan.html")


def show_profile(request):
    cursor = connection.cursor()
    id_manajer = request.session.get("id")
    print(id_manajer)
    try:
        cursor.execute(
            f"""
            select *
            from tim_manajer
            where id_manajer = %s
            """,
            [id_manajer],
        )
    except Exception as e:
        cursor = connection.cursor()
    data = cursor.fetchone()
    print(data)
    namaTim = data[1]

    try:
        cursor.execute(
            f"""
            select *
            from tim
            where nama_tim = %s
            """,
            [namaTim],
        )
    except Exception as e:
        cursor = connection.cursor()
    dataTim = cursor.fetchone()
    print(data)
    asalTim = dataTim[1]

    try:
        cursor.execute(
            f"""
            select *
            from non_pemain
            where non_pemain.id = %s
            """,
            [str(id_manajer)],
        )
    except Exception as e:
        cursor = connection.cursor()

    manajerData = cursor.fetchone()
    namaDepan = manajerData[1]
    namaBelakang = manajerData[2]
    nomorHP = manajerData[3]
    email = manajerData[4]
    alamat = manajerData[5]

    try:
        cursor.execute(
            f"""
            select *
            from status_non_pemain
            where id_non_pemain = %s
            """,
            [str(id_manajer)],
        )
    except Exception as e:
        cursor = connection.cursor()

    statusManajerData = cursor.fetchone()
    status = statusManajerData[1]

    try:
        cursor.execute(
            f"""
            select *
            from pemain
            where nama_tim = %s
            """,
            [namaTim],
        )
    except Exception as e:
        cursor = connection.cursor()
    dataPemain = cursor.fetchall()
    listPemainTim = []
    for perPemain in dataPemain:
        pemain = {
            "namaDepan": perPemain[2],
            "namaBelakang": perPemain[3],
            "nomorHP": perPemain[4],
            "tanggalLahir": perPemain[5],
            "isCaptain": perPemain[6],
            "posisi": perPemain[7],
            "npm": perPemain[8],
            "jenjang": perPemain[9],
        }
        listPemainTim.append(pemain)

    return render(
        request,
        "dashboard_manager.html",
        {
            "nama_tim": namaTim,
            "asal": asalTim,
            "list_pemain": listPemainTim,
            "namaDepan": namaDepan,
            "namaBelakang": namaBelakang,
            "nomorHP": nomorHP,
            "email": email,
            "alamat": alamat,
            "status": status,
        },
    )


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
    if request.method == "POST":
        print("kontol")
        namaStadium = request.POST.get("stadium")
        date = request.POST.get("date")
        cursor = connection.cursor()
        try:
            cursor.execute(
                f"""
                select id_stadium
                from stadium
                where nama = %s
                """,
                [namaStadium],
            )
        except Exception as e:
            cursor = connection.cursor()

        id_stadium = cursor.fetchone()

        print("idstadium " + str(id_stadium[0]))
        return render(
            request,
            "schedule_booking.html",
            {
                "stadium": namaStadium,
                "date": date,
            },
        )
    print("KOK SINI")
    return HttpResponseForbidden("kenot")


def stadiumBooking(request):
    cursor = connection.cursor()
    try:
        cursor.execute(
            f"""
            select nama
            from stadium
            """
        )
    except Exception as e:
        cursor = connection.cursor()

    allStadium = cursor.fetchall()
    allStadiumData = []
    for stadium in allStadium:
        data = stadium[0]
        result = {"namaStadium": data}
        allStadiumData.append(result)

    return render(request, "stadium_booking.html", {"allStadium": allStadiumData})


def historyRapat(request):
    return render(request, "history_rapat.html")


def bookingConfirmation(request):
    print("test")
    if request.method == "POST":
        print("watefak")
        start_datetime = request.POST.get("start_datetime")
        end_datetime = request.POST.get("end_datetime")
        id_manager = request.session.get("id")
        stadium = request.POST.get("stadium")
        cursor = connection.cursor()
        try:
            cursor.execute(
                f"""
                select id_stadium
                from stadium
                where nama = %s
                """,
                [stadium],
            )
        except Exception as e:
            cursor = connection.cursor()

        id_stadium = cursor.fetchone()

        response = ""

        try:
            cursor.execute(
                f"""
                INSERT INTO peminjaman (id_manajer, start_datetime, end_datetime, id_stadium) 
                VALUES (%s, %s, %s, %s);
                """,
                [id_manager, start_datetime, end_datetime, id_stadium[0]],
            )
        except Exception as e:
            response = e

        print(start_datetime)
        print(end_datetime)
        print(id_stadium[0])
        print(id_manager)
        print("ini response sayang")
        print(response)
        if response == "":
            messages.success(request, "Berhasil melakukan peminjaman stadium")
        else :
            messages.error(request, response)

    return redirect("/manager/listPeminjaman")
