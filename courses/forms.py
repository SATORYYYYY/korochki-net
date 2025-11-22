from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Application, Review
import re

class RegisterForm(UserCreationForm):
    username = forms.CharField(label='Логин', help_text='Латиница и цифры, не менее 6 символов')
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput, help_text='Минимум 8 символов')
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput)
    first_name = forms.CharField(label='Имя')
    last_name = forms.CharField(label='Фамилия')
    email = forms.EmailField(label='Email')
    phone = forms.CharField(label='Телефон', help_text='Формат: 8(XXX)XXX-XX-XX')
    address = forms.CharField(label='Адрес')
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'address', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not re.match(r'^[a-zA-Z0-9]+$', username):
            raise forms.ValidationError('Логин должен содержать только латинские буквы и цифры')
        return username

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not re.match(r'^[а-яА-ЯёЁ\s]+$', first_name):
            raise forms.ValidationError('Имя должно содержать только кириллические буквы')
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not re.match(r'^[а-яА-ЯёЁ\s]+$', last_name):
            raise forms.ValidationError('Фамилия должна содержать только кириллические буквы')
        return last_name

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['course', 'desired_start_date', 'payment_method']
        widgets = {
            'desired_start_date': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, f'{i} звезд' if i == 1 else f'{i} звезды' if i < 5 else f'{i} звезд') for i in range(1, 6)]),
            'comment': forms.Textarea(attrs={'rows': 4}),
        }