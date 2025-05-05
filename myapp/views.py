from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden

from .forms import CustomUserCreationForm, HomeworkForm, GradeForm
from .models import Schedule, Grade, Homework

# Декоратор: доступ только для учителей
def teacher_required(view_func):
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != 'teacher':
            return HttpResponseForbidden("Доступ только для учителей")
        return view_func(request, *args, **kwargs)
    return _wrapped

# 👤 ЛОГИН
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('schedule')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# 👋 ВЫХОД
def logout_view(request):
    logout(request)
    return redirect('login')

# 👤 РЕГИСТРАЦИЯ
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('schedule')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

# 🏠 ЛАНДИНГ
def landing_view(request):
    return render(request, 'index.html')  # Используем templates/index.html

# 📅 РАСПИСАНИЕ
@login_required
def schedule_view(request):
    schedule = Schedule.objects.all()
    return render(request, 'schedule.html', {'schedule': schedule})

# 📊 ОЦЕНКИ (список)
@login_required
def grades_view(request):
    grades = Grade.objects.all()
    return render(request, 'grades.html', {'grades': grades})

# 📝 ДОМАШКА (список)
@login_required
def homework_view(request):
    homework = Homework.objects.all()
    return render(request, 'homework.html', {'homework': homework})

# ➕ ДОБАВИТЬ ДОМАШНЕЕ ЗАДАНИЕ
@login_required
@teacher_required
def add_homework(request):
    form = HomeworkForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        hw = form.save(commit=False)
        hw.teacher = request.user
        hw.save()
        messages.success(request, "Домашнее задание создано")
        return redirect('homework')
    return render(request, 'add_homework.html', {'form': form})

# ➕ ДОБАВИТЬ ОЦЕНКУ
@login_required
@teacher_required
def add_grade(request):
    form = GradeForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Оценка выставлена")
        return redirect('grades')
    return render(request, 'add_grade.html', {'form': form})

# 👤 ПРОФИЛЬ
@login_required
def profile_view(request):
    return render(request, 'profile.html')
