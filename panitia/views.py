from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, "list_pertandingan.html")

def mulai(request):
    return render(request, "mulaiPertandingan.html")

def peristiwa(request):
    return render(request, "peristiwaTimBertanding.html")

def show_profile(request):
    rapat1 = {
        'id_pertandingan' : 11,
        'hari' : "Sabtu, 6 Mei 2023",
        'jam' : '16.30',
        "manajera" : "Tuchel (2)",
        'manajerb' : 'Klopp (3)'
    }
    rapat2 = {
        'id_pertandingan' : 11,
        'hari' : "Senin 8 Mei 2023",
        'jam' : '19.00',
        "manajera" : "Tuchel (2)",
        'manajerb' : 'Klopp (3)'
    }

    list_rapat = [rapat1, rapat2]

    context = {
        'list_rapat' : list_rapat
    }
    # Jika rapaat belum ada
    # context = {}

    return render(request, 'dashboard_panitia.html', context=context)

def manage_pertandingan(request):
    context = {
        'isLengkap' : True
    }
    return render(request, "manage_pertandingan.html", context)

def list_peristiwa(request):
    return render(request, "list_peristiwa.html")


def buat_pertandingan(request):
    return render(request, "buat_pertandingan.html")

def list_pertandingan(request):
    return render(request, "list_pertandingan.html")

def mulai_rapat(request):
    return render(request, "mulai_rapat.html")

def nota_rapat(request):
    return render(request, "nota_rapat.html")

def submit_pertandingan(request):
    return render(request, "submit_pertandingan.html")

def schedule_list(request):
    return render(request, "schedule_list.html")
