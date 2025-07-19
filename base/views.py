from django.shortcuts import render

# Create your views 
def index(request):
    return render (request, 'index.html')


def dashboard(request):
    return render (request, 'dashboard.html')


def login(request):
    return render (request, 'registration/login.html')


def signup(request):
    return render (request, 'registration/signup.html')


def student (request):
    return render (request, 'student.html')