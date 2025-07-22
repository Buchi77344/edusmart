from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import auth
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
# Create your views 
def index(request):
    return render (request, 'index.html')


def dashboard(request):
    return render (request, 'dashboard.html')
#registration for schools

def login(request):
    return render (request, 'registration/login.html')
@csrf_exempt
def login_user(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get("username")
            password = data.get("password")

            if not username or not password:
                return JsonResponse({"error": "Both fields are required."}, status=400)

            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth.login(request, user)
                return JsonResponse({"message": "Login successful."}, status=200)
            else:
                return JsonResponse({"error": "Invalid credentials."}, status=401)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON."}, status=400)

    return JsonResponse({"error": "Only POST method allowed."}, status=405)


def signup(request):
    return render (request, 'registration/signup.html')
def logout(request):
    auth.logout(request)
    return redirect('login')

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
import json

User = get_user_model()

@csrf_exempt
def register_user(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            school_name = data.get("school_name")
            email = data.get("email")
            password1 = data.get("password1")
            password2 = data.get("password2")
            institution_type = data.get("institution_type", [])

            if not all([school_name, email, password1, password2, institution_type]):
                return JsonResponse({"error": "All fields are required."}, status=400)

            if password1 != password2:
                return JsonResponse({"error": "Passwords do not match."}, status=400)

            if User.objects.filter(email=email).exists():
                return JsonResponse({"error": "Email already exists."}, status=400)

            user = User.objects.create(
                username=email,
                email=email,
                password=make_password(password1),
                school_name=school_name,
                institution_type=institution_type,  # This should be a list
                role="admin",
            )

            return JsonResponse({"message": "Account created successfully."}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON."}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Only POST requests allowed."}, status=405)

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