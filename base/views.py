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


def teacher(request):
    return render (request, 'teacher.html')

def classes(request):
    return render (request, 'class.html')

def subject(request):
    return render (request, 'subject.html')


def attendance(request):
    return render (request, 'attendace.html')