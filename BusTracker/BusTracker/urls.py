"""
URL configuration for BusTracker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from usuarios import views as views_usuarios
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views_usuarios.home , name='home'),
    path('login/', views_usuarios.user_login , name='login'),
    path('register/', views_usuarios.register , name='register'),
    path('logout/', views_usuarios.user_logout , name='logout'),
    path('chatbot/', views_usuarios.chatbot , name='chatbot'),




]

