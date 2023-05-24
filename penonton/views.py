from django.shortcuts import render


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

