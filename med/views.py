from django.shortcuts import render

# Create your views here.


def login(request):
    return render(request, 'login.html')

def index(request):
    return render(request, 'index.html')
    

def profile(request):
    return render(request, 'profile.html')

def signup(request):
    return render(request,'signup.html')

def popupform(request):
    return render(request,'popupform.html')
def report(request, id):
    return render(request, 'report.html', {"id": id})


def user_detail(request):
    return render(request, 'user_detail.html')

def imagingA(request):
    return render(request, 'imagingA.html')

def RADS(request):
    return render(request, 'RADS.html')

def invoice(request):
    return render(request, 'invoice.html')
def payment(request):
    return render(request, 'payment.html')