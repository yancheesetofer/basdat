from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, "booking_list.html")


def listSemuaPertandingan(request):
    return render(request, "listSemuaPertandingan.html")

def show_profile(request):
    list_pemain = ['Kylian Mbappe', 'Antoine Griezmann', 'Olivier Giroud',
                  'Marcus Thuram', 'Youssouf Fofana', 'Benjamin Pavard', 
                  'Alphonse Areola', 'Ibrahima Konaté', 'Théo Hernandez',
                    'Dayot Upamecano', 'Jean-Clair Todibo']
    context = {
        'nama_tim' : 'CSUI FC',
        'asal' : 'Universitas Depok',
        'list_pemain' : list_pemain,
    }
    # jika belum ada tim terdaftar
    context = {}

    
    return render(request, 'dashboard_manager.html', context)

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
    return render(request, 'stadium_booking.html')

def historyRapat(request):
    return render(request, 'history_rapat.html')

def schedule_booking(request):
    return render(request, 'schedule_booking.html')

def stadium_booking(request):
    return render(request, 'stadium_booking.html')