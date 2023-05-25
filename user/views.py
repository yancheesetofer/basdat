from django.shortcuts import render
from django.db import *
from django.contrib import messages
from pprint import pprint
from django.shortcuts import redirect
import psycopg2
from django.urls import reverse
from django.template.loader import render_to_string


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
                cursor = connection.cursor()
            data = cursor.fetchone()
            if data is not None:
                id_manajer = data[0]
                request.session["role"] = "manajer"
                request.session["id"] = str(id_manajer)

                return redirect("/manager/profile")
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
                    cursor = connection.cursor()
                data = cursor.fetchone()
                if data is not None:
                    id_panitia = data[0]
                    jabatan = data[1]
                    request.session["role"] = "panitia"
                    request.session["id"] = str(id_panitia)
                    
                    return redirect("/panitia/profile")
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
                        cursor = connection.cursor()
                    data = cursor.fetchone()

                    if data is not None:
                        id_penonton = data[0]
                        request.session["role"] = "penonton"
                        request.session["id"] = str(id_penonton)
                        return redirect("/penonton/profile")

        else:
            messages.error("Email atau password yang dimasukkan salah")

    return render(request, "login.html")
