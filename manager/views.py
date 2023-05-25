from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.db import *
from pprint import pprint
from django.contrib.auth.decorators import login_required

# Create your views here.


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


def listSemuaPertandingan(request):
    return render(request, "listSemuaPertandingan.html")


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


@login_required(login_url='../../user/login')
def registerTim(request):
    cursor = connection.cursor()
    # check if manager has any teams
    username = request.session["username"]
    username = 'rsamber14'
    try:
        cursor.execute(
            f"""
                select * 
                from tim t 
                join tim_manajer tm on t.nama_tim = tm.nama_tim 
                join manajer m on tm.id_manajer = m.id_manajer 
                where username = '{username}';;
            """
        )
        if cursor.fetchone():
            return redirect("../detail/")
    except Exception as e:
        return HttpResponseBadRequest()

    # handle register tim
    if request.method == "POST":
        nama_tim = request.POST.get("namaTim")
        nama_univ = request.POST.get("namaUniv")
        try:
            cursor.execute(
                f"""
                    insert into tim values ('{nama_tim}', '{nama_univ}');
                """
            )
        except Exception as e:
            return HttpResponseBadRequest("Bad Request 400: Tim can not be registered")
        request.session["nama_tim"]  = nama_tim
        request.session["nama_univ"] = nama_univ
    
    
    return render(request, "registerTim.html")


@login_required(login_url='../../user/login')
def detailTim(request):
    username = request.session["username"]
    username = 'rsamber14'
    if (request.session["role"] != 'manajer'):  
        return HttpResponseBadRequest("This page is restricted")

    daftar_pemain = []
    daftar_pelatih = []
    cursor = connection.cursor()
    try:
        cursor.execute(
            f"""
            select distinct concat(nama_depan, ' ', nama_belakang) as nama_lengkap, 
            nomor_hp, tgl_lahir, is_captain, posisi, npm, jenjang 
            from pemain p 
            join tim t on p.nama_tim = t.nama_tim 
            join tim_manajer tm on tm.nama_tim = t.nama_tim 
            join manajer m on tm.id_manajer = m.id_manajer 
            where username = '{username}';"""
        )
        listPemain = cursor.fetchall()
        # fetch daftar pemain
        daftar_pemain = [{
            "nama_lengkap": x[0],
            "nomor_hp": x[1],
            "tgl_lahir": x[2],
            "is_captain": x[3],
            "posisi": x[4],
            "npm": x[5],
            "jenjang": x[6] 
        } for x in listPemain]
    except Exception as e:
        pass
    
    
    try:
        # fetch daftar pelatih
        cursor.execute(
            f"""
            select distinct concat(nama_depan, ' ', nama_belakang) as nama_lengkap, 
            nomor_hp, email, spesialisasi 
            from pelatih p join spesialisasi_pelatih sp on sp.id_pelatih = p.id_pelatih 
            join non_pemain np on p.id_pelatih = np.id 
            join tim t on p.nama_tim = t.nama_tim 
            join tim_manajer tm on tm.nama_tim = t.nama_tim 
            join manajer m on tm.id_manajer = m.id_manajer 
            where m.username = '{username}';"""
        )
        listPelatih = cursor.fetchall()
        daftar_pelatih = [{
            "nama_lengkap": x[0],
            "nomor_hp": x[1],
            "email": x[2],
            "spesialisasi": x[3],
        } for x in listPelatih]
        print(daftar_pelatih)
    except Exception as e:
        pass

    context = {
        'daftar_pemain' : daftar_pemain,
        'daftar_pelatih' : daftar_pelatih
    }
    return render(request, "detailTim.html", context)

def makecaptain(request):
    nama_tim = request.session["nama_tim"]
    # nama_tim = 'Hurricanes'
    cursor = connection.cursor()
    if request.method == "POST":
        pemain_selected = request.POST.get("pemain")
        # register pemain to tim
        try:
            cursor.execute(
                f"""
                select count(p.nama_tim) 
                from pemain p 
                join tim t on p.nama_tim = t.nama_tim  
                where p.nama_tim = '{nama_tim}' 
                group by p.nama_tim;
                """
            )
            jumlah_pemain = cursor.fetchone()[0]
            if jumlah_pemain < 14:
                cursor.execute(
                    f"""
                    update pemain set nama_tim = '{nama_tim}' where id_pemain = '{pemain_selected}'; 
                    """
                )
        except Exception as e:
            return HttpResponseBadRequest(f"Can not registered pemain into Tim {nama_tim}")
    

@login_required(login_url='../../user/login')
def pilihPemain(request):
    nama_tim = request.session["nama_tim"]
    nama_tim = 'Hurricanes'
    cursor = connection.cursor()
    if request.method == "POST":
        pemain_selected = request.POST.get("pemain")
        # register pemain to tim
        try:
            cursor.execute(
                f"""
                select count(p.nama_tim) 
                from pemain p 
                join tim t on p.nama_tim = t.nama_tim  
                where p.nama_tim = '{nama_tim}' 
                group by p.nama_tim;
                """
            )
            jumlah_pemain = cursor.fetchone()[0]
            if jumlah_pemain < 14:
                cursor.execute(
                    f"""
                    update pemain set nama_tim = '{nama_tim}' where id_pemain = '{pemain_selected}'; 
                    """
                )
        except Exception as e:
            return HttpResponseBadRequest(f"Can not registered pemain into Tim {nama_tim}")
    
    pemain_notim = []
    try:
        cursor.execute(
            f"""
            select concat(nama_depan, ' ', nama_belakang) as nama_lengkap, posisi, id_pemain 
            from pemain 
            where nama_tim is null;
            """
        )
        pemain_notim = [{
            'nama_lengkap' : x[0],
            'posisi' : x[1],
            'id_pemain' : x[2]
        }for x in cursor.fetchall()]
        
    except Exception as e:
        pass
    
    context = {
        'pemain_notim' : pemain_notim
    }
    return render(request, "pemain.html", context)

@login_required(login_url='../../user/login')
def pilihPelatih(request):
    cursor = connection.cursor()
    nama_tim = request.session["nama_tim"]
    # nama_tim = 'Bears'
    cursor = connection.cursor()
    if request.method == "POST":
        pelatih_selected = request.POST.get("pelatih")

        # register pemain to tim
        try:
            cursor.execute(
                f"""
                    SELECT spesialisasi from spesialisasi_pelatih where id_pelatih = '{pelatih_selected}'; 
                    """
            )
            spesialisasi = cursor.fetchone()[0]
            cursor.execute(
                f"""
                    SELECT isSpExist('{nama_tim}' spl varchar); 
                    """
            )
            isSpExist = cursor.fetchone()
            if isSpExist:
                cursor.execute(
                    f"""
                        update SPESIALISASI_PELATIH set nama_tim = '{nama_tim}' where id_pelatih = '{pelatih_selected}'; 
                        """
                )
        except Exception as e:
            return HttpResponseBadRequest(e)


    pelatih_notim = []
    try:
        cursor.execute(
            f"""
            select p.id_pelatih, concat(nama_depan, ' ', nama_belakang) as nama_lengkap, spesialisasi 
            from pelatih p 
            left outer join spesialisasi_pelatih sp on p.id_pelatih = sp.id_pelatih 
            left outer join non_pemain np on p.id_pelatih = np.id 
            where nama_tim is null;
            """
        )
        pelatih_notim = [{
            'id_pelatih' : x[0],
            'nama_lengkap' : x[1],
            'spesialisasi' : x[2]
        }for x in cursor.fetchall()]
    except Exception as e:
        pass
    
    context = {
        'pelatih_notim' : pelatih_notim
    }

    return render(request, "pelatih.html", context)


def bookingList(request):
    return render(request, "booking_list.html")


def historyRapat(request):
    return render(request, "history_rapat.html")


def scheduleBooking(request):
    return render(request, "schedule_booking.html")


def stadiumBooking(request):
    return render(request, "stadium_booking.html")


def historyRapat(request):
    return render(request, "history_rapat.html")


def schedule_booking(request):
    return render(request, "schedule_booking.html")


def stadium_booking(request):
    return render(request, "stadium_booking.html")
