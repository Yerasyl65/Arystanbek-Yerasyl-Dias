from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Subject, Homework, Grade


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'role')


class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        fields = ['subject', 'description', 'due_date']


class GradeForm(forms.ModelForm):
    student = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(role='student'),
        label='Ученик'
    )
    subject = forms.ModelChoiceField(
        queryset=Subject.objects.all(),
        label='Предмет'
    )

    class Meta:
        model = Grade
        fields = ['student', 'subject', 'value']
        widgets = {
            'value': forms.NumberInput(attrs={'min': 1, 'max': 100}),
        }
