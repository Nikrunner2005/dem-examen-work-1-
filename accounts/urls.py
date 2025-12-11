from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # корень сайта → home
    path('home/', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),  # кастомный LoginView из views.py
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('review/<int:pk>/', views.add_review, name='review'),
]   
