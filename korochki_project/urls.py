"""
URL configuration for korochki_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path
from courses import views

# Маршруты нашего приложения - как дорожные указатели
urlpatterns = [
    path('admin/', admin.site.urls),  # Админка - для управленцев
    path('', views.home, name='home'),  # Главная страница - приветствие
    path('register/', views.register, name='register'),  # Регистрация - запись в клуб
    path('login/', views.custom_login, name='login'),  # Вход 
    path('logout/', views.custom_logout, name='logout'),  # Выход - до свидания!
    path('applications/', views.application_list, name='application_list'),  # Мои заявки
    path('applications/create/', views.create_application, name='create_application'),  # Подать заявку
    path('applications/<int:application_id>/review/', views.create_review, name='create_review'),  # Оставить отзыв
]

# Кастомизируем заголовки админки - чтобы было красиво
admin.site.site_header = 'Панель администратора Корочки.есть'  # Заголовок
admin.site.site_title = 'Корочки.есть'  # Титул вкладки
admin.site.index_title = 'Управление данными'  # Заголовок на главной админки
