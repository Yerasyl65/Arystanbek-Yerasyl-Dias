from django.contrib import admin
from django.urls import path
from myapp import views as myapp_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', myapp_views.landing_view, name='home'),  # Главная

    # Аутентификация
    path('login/', myapp_views.login_view, name='login'),
    path('register/', myapp_views.register_view, name='register'),
    path('logout/', myapp_views.logout_view, name='logout'),

    # Расписание
    path('schedule/', myapp_views.schedule_view, name='schedule'),

    # Домашние задания
    path('homework/', myapp_views.homework_view, name='homework'),
    path('homework/add/', myapp_views.add_homework, name='add_homework'),

    # Оценки
    path('grades/', myapp_views.grades_view, name='grades'),
    path('grades/add/', myapp_views.add_grade, name='add_grade'),

    # Профиль
    path('profile/', myapp_views.profile_view, name='profile'),
]