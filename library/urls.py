from django.contrib import admin
from django.urls import path
from library import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('librarian/', views.librarian_dashboard, name='librarian_dashboard'),
    path('user/', views.user_dashboard, name='user_dashboard'),
]