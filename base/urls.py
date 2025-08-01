from django.urls import path

from . import views

urlpatterns = [ 
    path('', views.index, name='index'), 
    path('dashboard/',views.dashboard,name='dashboard'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'), 
     path('student/', views.student, name='student'),
    path('teacher/', views.teacher, name='teacher'), 
    path('classes/', views.classes, name='classes'),
    path('subject/', views.subject, name='subject'),
    path('attendance/', views.attendance, name='attendance'),
    path("api/register/", views.register_user, name="register_user"),
    path("api/login/", views.login_user, name="login_user"),
    path('logout/', views.logout, name='logout'),  
    
    # Home page
    # Add more URL patterns here as needed
]
