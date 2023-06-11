from datetime import date
import datetime
from django.shortcuts import render, redirect
from django.conf import settings
from django.db import *
from utilities.helper import query
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone




# Create your views here.




def index(request):
    return render(request, "list_pertandingan_penonton.html")

def mulai(request, id_pertandingan):
    
    data = query(
        f"""
        SELECT ARRAY_AGG(nama_tim) as nama_tim, id_pertandingan
        FROM tim_pertandingan
        WHERE id_pertandingan='{id_pertandingan}'
        GROUP BY id_pertandingan;
        """
    )

    context = {
        "data": data[0]
    }
    return render(request, 'mulaiPertandingan.html', context)



def peristiwa_tim(request, id_pertandingan, nama_tim):
    peristiwa = query(
        f"""
        SELECT datetime, jenis, pemain.id_pemain, nama_depan, nama_belakang
        FROM peristiwa, pemain
        WHERE peristiwa.id_pemain=pemain.id_pemain
        AND peristiwa.id_pertandingan='{id_pertandingan}'
        AND nama_tim='{nama_tim}';
        """
    )

    context = {
        'peristiwa': peristiwa,
        'nama_tim': nama_tim
    }

    return render(request, 'peristiwaTimBertanding.html', context)


def show_profile(request):
    cursor = connection.cursor()
    # cursor.execute("SET search_path TO SIREST")
    id_panitia = request.session.get("id")
    print(id_panitia)
    try:
        cursor.execute(
            f"""
            select * 
            from non_pemain
            where id = %s
            """,
            [id_panitia]
        )
    except Exception as e:
        cursor = connection.cursor()
    dataPanitia = cursor.fetchall()
    print("data didaapt")
    print(dataPanitia)

    try:
        cursor.execute(
            f"""
            select jabatan
            from panitia
            where id_panitia = %s
            """,
            [id_panitia]
        )
    except Exception as e:
        cursor = connection.cursor()
    jabatanPanitia = cursor.fetchall()
    print(jabatanPanitia)

    try:
        cursor.execute(
            f"""
            select status
            from status_non_pemain
            where id_non_pemain = %s
            """,
            [id_panitia]
        )
    except Exception as e:
        cursor = connection.cursor()
    statusPanitia = cursor.fetchall()
    print(statusPanitia)

    listDataPanitia = {
        'namaDepan' : dataPanitia[0][1],
        'namaBelakang' : dataPanitia[0][2],
        'nomorHP' : dataPanitia[0][3],
        'email' : dataPanitia[0][4],
        'alamat' : dataPanitia[0][5],
        'status' : statusPanitia[0][0],
        'jabatan' : jabatanPanitia[0][0]
    }

    cursor.execute(
        f"""
        select *
        from rapat
        where perwakilan_panitia = %s
        """,
        [id_panitia]
    )
    list_rapat = []
    allrapat = cursor.fetchall()
    # user_info = query(
    #         f"""
    #         SELECT np.nama_depan, np.nama_belakang, np.nomor_hp, np.email, np.alamat, snp.status, p.jabatan
    #         FROM non_pemain np
    #         JOIN status_non_pemain snp ON np.id = snp.id_non_pemain
    #         JOIN panitia p ON np.id = p.id_panitia;

    #         """
    # )
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
        'list_rapat' : list_rapat,
        'dataPanitia' : listDataPanitia                 
    }
    return render(request, 'dashboard_panitia.html',context)

def manage_pertandingan(request):
    pertandingan = query(
            f"""
            SELECT pertandingan.id_pertandingan, ARRAY_AGG(tim_pertandingan.nama_tim) as tim, start_datetime
            FROM pertandingan, tim_pertandingan
            WHERE pertandingan.id_pertandingan=tim_pertandingan.id_pertandingan
            GROUP BY pertandingan.id_pertandingan
            ORDER BY start_datetime asc;
            """
        )

    pemenang = {}
    for p in pertandingan:    
        pemenangQuery = query(
            f"""
            SELECT nama_tim, skor
            FROM tim_pertandingan
            WHERE id_pertandingan='{p.id_pertandingan}';
            """
        )

        if pemenangQuery[0].skor > pemenangQuery[1].skor:
            pemenang[p.id_pertandingan] = pemenangQuery[0].nama_tim
        elif pemenangQuery[0].skor < pemenangQuery[1].skor:
            pemenang[p.id_pertandingan] = pemenangQuery[1].nama_tim
        else:
            pemenang[p.id_pertandingan] = "SERI"

    jumlahPertandingan = query(
        f"""
        select count(*) as jumlah_pertandingan from pertandingan;
        """
    )
    
    context = {
        'pertandingan': pertandingan,
        'pemenang': pemenang,
        'jumlahPertandingan': jumlahPertandingan[0].jumlah_pertandingan 
    }


    return render(request, 'manage_pertandingan.html', context)


def list_peristiwa(request, id_pertandingan, nama_tim):
    print(id_pertandingan)
    peristiwa = query(
        f"""
        SELECT datetime, jenis, pemain.id_pemain, nama_depan, nama_belakang
        FROM peristiwa, pemain
        WHERE peristiwa.id_pemain=pemain.id_pemain
        AND peristiwa.id_pertandingan='{id_pertandingan}'
        AND nama_tim='{nama_tim}';
        """
    )
    print(nama_tim)
    print(id_pertandingan)
    print(peristiwa)

    context = {
        'peristiwa': peristiwa,
        'nama_tim': nama_tim
    }

    return render(request, 'list_peristiwa.html', context)

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

        timA = keduaTim[0][0]
        timB = keduaTim[1][0]

        if rapat != None:
            result= {
            "timBertanding": timA + " vs " + timB,
            "stadium": namaStadium[0],
            "tanggalWaktu": str(exactdate) + " " + str(startDate) + " - " + str(endDate),
            "idPertandingan": id,
            "rapat": rapat[0],
            "timA": timA,
            "timB": timB
            }
        else :
            result= {
                "timBertanding": keduaTim[0][0] + " vs " + keduaTim[1][0],
                "stadium": namaStadium[0],
                "tanggalWaktu": str(exactdate) + " " + str(startDate) + " - " + str(endDate),
                "idPertandingan": id,
                "rapat": None,
                "timA": timA,
                "timB": timB
        }
        listResponseWanted.append(result)


    return render(request, "mulai_rapat.html", {
        "listResponse": listResponseWanted
    })

def nota_rapat(request):
    if request.method == "POST":
        idPertandingan = request.POST.get("idPertandingan")
        nama = request.POST.get("stadium")
        timA = request.POST.get("timA")
        timB = request.POST.get("timB")
        print("cabo")
        print(idPertandingan)
        print(nama)
        print("hai")
        print(timA)
        print("halo")
        print(timB)

    return render(request, "nota_rapat.html", {
        "idPertandingan": idPertandingan,
        "nama": nama,
        "timA": timA,
        "timB": timB
    })

def prosesNotaRapat(request):
    if request.method == "POST":
        idPanitia = request.session.get("id")
        nowDatetime = datetime.datetime.now()
        idPertandingan = request.POST.get("idPertandingan")
        namaTimA = request.POST.get("timA")
        namaTimB = request.POST.get("timB")
        isiRapat = request.POST.get("isi_rapat")
        print(idPanitia + " idPanitia")
        print(nowDatetime)
        print(idPertandingan + " id pertandingan")
        print(namaTimA)
        print(namaTimB)
        print(isiRapat + " isi rapat")

        cursor = connection.cursor()
        try:
            cursor.execute(
                f"""
                select id_manajer
                from tim_manajer
                where nama_tim = %s
                """,
                [namaTimA]
            )
        except Exception as e:
            cursor = connection.cursor()

        idManajerTimA = cursor.fetchone()
        print(idManajerTimA[0])

        cursor = connection.cursor()
        try:
            cursor.execute(
                f"""
                select id_manajer
                from tim_manajer
                where nama_tim = %s
                """,
                [namaTimB]
            )
        except Exception as e:
            cursor = connection.cursor()

        idManajerTimB = cursor.fetchone()
        print(idManajerTimB[0])

        try:
            cursor.execute(
                f"""
                INSERT INTO rapat (id_pertandingan, datetime, perwakilan_panitia, manajer_tim_a, manajer_tim_b, isi_rapat)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                [idPertandingan, nowDatetime, idPanitia, idManajerTimA, idManajerTimB, isiRapat]
            )
        except Exception as e:
            cursor = connection.cursor()
        
    
    return redirect("/panitia/mulaiRapat")

def confirmationRapat(request):
    if request.method == "POST":
        idPertandingan = request.POST.get("idPertandingan")
        nama = request.POST.get("stadium")
        timA = request.POST.get("timA")
        timB = request.POST.get("timB")
        notaRapat = request.POST.get("notaRapat")
        perwakilanPanitia = request.session.get("id")
        datetime = timezone.now()

        cursor = connection.cursor()

        try:
            cursor.execute(
                f"""
                select id_manajer
                from tim_manajer
                where nama_tim = %s
                """,
                [timA]
            )
        except Exception as e:
            cursor = connection.cursor()
        
        manajerA = cursor.fetchone()

        try:
            cursor.execute(
                f"""
                select id_manajer
                from tim_manajer
                where nama_tim = %s
                """,
                [timB]
            )
        except Exception as e:
            cursor = connection.cursor()
        
        manajerB = cursor.fetchone()
        

        try:
            cursor.execute(
                f"""
                INSERT INTO rapat (id_pertandingan, datetime, perwakilan_panitia, manajer_tim_a, manajer_tim_b, isi_rapat)
                values (%s, %s, %s, %s, %s, %s)
                """,
                [idPertandingan, datetime, perwakilanPanitia, manajerA, manajerB, notaRapat]
            )
        except Exception as e:
            cursor = connection.cursor()

    return redirect("/panitia/profile")

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

@csrf_exempt
def peristiwa(request, id_pertandingan, nama_tim):
    if request.method == "POST":
        # Do Something
        pemain1 = request.POST.get('pemain1') 
        pemain2 = request.POST.get('pemain2')
        pemain3 = request.POST.get('pemain3') 
        pemain4 = request.POST.get('pemain4')
        pemain5 = request.POST.get('pemain5')  
        peristiwa1 = request.POST.get('peristiwa1') 
        peristiwa2 = request.POST.get('peristiwa2') 
        peristiwa3 = request.POST.get('peristiwa3') 
        peristiwa4 = request.POST.get('peristiwa4') 
        peristiwa5 = request.POST.get('peristiwa5')
        waktu1 = str(request.POST.get('waktu1')).replace("T", " ") + ":00"
        waktu2 = str(request.POST.get('waktu2')).replace("T", " ") + ":00"
        waktu3 = str(request.POST.get('waktu3')).replace("T", " ") + ":00"
        waktu4 = str(request.POST.get('waktu4')).replace("T", " ") + ":00"
        waktu5 = str(request.POST.get('waktu5')).replace("T", " ") + ":00"
        peristiwa = [[pemain1, peristiwa1, waktu1], [pemain2, peristiwa2, waktu2], [pemain3, peristiwa3, waktu3], [pemain4, peristiwa4, waktu4], [pemain5, peristiwa5, waktu5]]
        print(request)

        for data in peristiwa:
            # Check null: Jika ada satu baris yang isinya kosong/ada kolom dalam satu baris yang kosong, tidak perlu menjalankan query
            if data[0] == 0 or data[1] == 0 or len(data[2]) < 19:
                continue
            else:
                # Format Insert: id_pertandingan, datetime, jenis, id_pemain
                insert_data = query(
                    f"""
                    INSERT INTO peristiwa VALUES(
                    '{id_pertandingan}', '{data[2]}', '{data[1]}', '{data[0]}'
                    );
                    """
                ) 

        if type(insert_data) != int  :
            return JsonResponse({'success': 'false', 'message': 'Something is wrong'}, status = 501)
        else:
            return JsonResponse({'success': 'true', 'message': 'Berhasil menyimpan peristiwa.'}, status=200)        
    else:
        data = query(
            f"""
            SELECT pertandingan.id_pertandingan, tim_pertandingan.nama_tim, JSON_AGG(JSON_BUILD_ARRAY(id_pemain, pemain.nama_depan, pemain.nama_belakang)) as nama_pemain
            FROM pertandingan, tim_pertandingan, pemain
            WHERE pertandingan.id_pertandingan=tim_pertandingan.id_pertandingan
            AND tim_pertandingan.nama_tim=pemain.nama_tim
            AND pertandingan.id_pertandingan='{id_pertandingan}'
            AND tim_pertandingan.nama_tim='{nama_tim}'
            GROUP BY pertandingan.id_pertandingan, tim_pertandingan.nama_tim;
            """
        )

        context = {
            'data': data[0]
        }
        return render(request, 'peristiwaTimBertanding.html',context)

@csrf_exempt
def submit_peristiwa(request):
    if request.method == "POST":
        pemain_count = 5
        peristiwa = []

        for i in range(1, pemain_count + 1):
            pemain = request.POST.get('nama_pemain{}'.format(i))
            peristiwa_value = request.POST.get('peristiwa{}'.format(i))
            waktu = request.POST.get('waktu{}'.format(i))
            print(pemain)
            print(peristiwa_value)
            print(waktu)
            if pemain and peristiwa_value and waktu:
                peristiwa.append([pemain, peristiwa_value, waktu])

        for data in peristiwa:
            pemain = data[0]
            peristiwa_value = data[1]
            waktu = str(data[2]).replace("T", " ") + ":00"

            insert_data = query(
                    f"""
                    INSERT INTO peristiwa VALUES(
                    '{id_pertandingan}', '{data[2]}', '{data[1]}', '{data[0]}'
                    );
                    """
                ) 

            # Perform your database insertion or processing here using the extracted values
            
        return render(request, 'peristiwaTimBertanding.html')
    
