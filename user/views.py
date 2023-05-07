from django.shortcuts import render


# Create your views here.


def register(request):
    return render(request, "registerAs.html")

def register_manager(request):
    return render(request, "registerUser.html")

def register_penonton(request):
    return render(request, "registerUser.html")

def register_panitia(request):
    context = {
        'isPanitia' : 'true'
    }
    return render(request, "registerUser.html", context)


