from django.shortcuts import render
from django.db import *
from django.contrib import messages
from pprint import pprint
import psycopg2


# Create your views here.


def register(request):
    return render(request, "registerAs.html")


def register_manager(request):
    return render(request, "registerUser.html")


def register_penonton(request):
    return render(request, "registerUser.html")


def register_panitia(request):
    context = {"isPanitia": "true"}
    return render(request, "registerUser.html", context)


def homePage(request):
    return render(request, "loginRegister.html")


def loginPage(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        cursor = connection.cursor()
        # search if the user is exist in user system
        try:
            cursor.execute(
                f"""
                select * 
                from user_system
                where username = %s AND password = %s
                """,
                [username, password],
            )
        except Exception as e:
            cursor = connection.cursor()
        response = cursor.fetchone()
        print(response)
        print(response[0])
        print(response[1])
        if response is not None:
            # save in session
            request.session["username"] = response[0]
            request.session["password"] = response[1]
            request.session["is_authenticated"] = True

            # search for user role
            # try for role manajer
            try :
                cursor.execute(
                    f"""
                    select *
                    from manajer
                    where username = %s
                    """,
                    [response[0]]
                )
            except Exception as e:
                print("asdasda")
            data = cursor.fetchone()
            print(data)
            if data is not None:
                id_manajer = data[0]
                request.session["role"] = "manajer"
                try:
                    cursor.execute(
                        f"""
                        select *
                        from non_pemain
                        where non_pemain.id = %s
                        """,
                        [str(id_manajer)]
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
                        [str(id_manajer)]
                    )
                except Exception as e:
                    cursor = connection.cursor()

                statusManajerData = cursor.fetchone()
                status = statusManajerData[1]
                return render(request, "../../manager/templates/dashboard_manager.html", context={
                    'namaDepan': namaDepan,
                    'namaBelakang': namaBelakang,
                    'nomorHP': nomorHP,
                    'email': email,
                    'alamat': alamat,
                    'status': status
                })
            else :
                # try for role panitia
                try :
                    cursor.execute(
                        f"""
                        select *
                        from panitia
                        where username = %s
                        """,
                        [response[0]]
                    )
                except Exception as e:
                    print("asdasda")
                data = cursor.fetchone()
                print(data)
                print("ini data panitia ")
                if data is not None:
                    id_panitia = data[0]
                    jabatan = data[1]
                    request.session["role"] = "panitia"
                    try:
                        cursor.execute(
                            f"""
                            select *
                            from non_pemain
                            where non_pemain.id = %s
                            """,
                            [str(id_panitia)]
                        )
                    except Exception as e:
                        cursor = connection.cursor()

                    panitiaData = cursor.fetchone()
                    namaDepan = panitiaData[1]
                    namaBelakang = panitiaData[2]
                    nomorHP = panitiaData[3]
                    email = panitiaData[4]
                    alamat = panitiaData[5]

                    try:
                        cursor.execute(
                            f"""
                            select *
                            from status_non_pemain
                            where id_non_pemain = %s
                            """,
                            [str(id_panitia)]
                        )
                    except Exception as e:
                        cursor = connection.cursor()
                    statusPanitiaData = cursor.fetchone()
                    status = statusPanitiaData[1]
                    

                    print("nama depan " + namaDepan)
                    print("nama belakang " + namaBelakang)
                    print("nomor hp " + nomorHP)
                    print("email " + email)
                    print("alamat " + alamat)
                    print("status " + status)
                    print("jabatan " + jabatan)
                    return render(request, "../../panitia/templates/dashboard_panitia.html", context={
                        'namaDepan': namaDepan,
                        'namaBelakang': namaBelakang,
                        'nomorHP': nomorHP,
                        'email': email,
                        'alamat': alamat,
                        'status': status,
                        'jabatan': jabatan
                    })
                else :
                    # try for role penonton
                    try :
                        cursor.execute(
                            f"""
                            select *
                            from penonton
                            where username = %s
                            """,
                            [response[0]]
                        )
                    except Exception as e:
                        print("asdasda")
                    data = cursor.fetchone()
                    print(data)
                    print("ini data panitia ")
                    if data is not None:
                        id_penonton = data[0]
                        request.session["role"] = "panitia"
                        try:
                            cursor.execute(
                                f"""
                                select *
                                from non_pemain
                                where non_pemain.id = %s
                                """,
                                [str(id_penonton)]
                            )
                        except Exception as e:
                            cursor = connection.cursor()

                        penontonData = cursor.fetchone()
                        namaDepan = penontonData[1]
                        namaBelakang = penontonData[2]
                        nomorHP = penontonData[3]
                        email = penontonData[4]
                        alamat = penontonData[5]

                        try:
                            cursor.execute(
                                f"""
                                select *
                                from status_non_pemain
                                where id_non_pemain = %s
                                """,
                                [str(id_penonton)]
                            )
                        except Exception as e:
                            cursor = connection.cursor()
                        statusPenontonData = cursor.fetchone()
                        status = statusPenontonData[1]
                        

                        print("nama depan " + namaDepan)
                        print("nama belakang " + namaBelakang)
                        print("nomor hp " + nomorHP)
                        print("email " + email)
                        print("alamat " + alamat)
                        print("status " + status)
                        return render(request, "../../penonton/templates/dashboardPenonton.html", context={
                            'namaDepan': namaDepan,
                            'namaBelakang': namaBelakang,
                            'nomorHP': nomorHP,
                            'email': email,
                            'alamat': alamat,
                            'status': status
                        })


                # Check is 
        else:
            messages.error("Email atau password yang dimasukkan salah")

    return render(request, "login.html")
