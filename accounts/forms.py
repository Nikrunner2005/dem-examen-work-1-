from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
import re
from datetime import date
from django.contrib.auth import authenticate
from .models import CourseRequest

class RegisterForm(forms.ModelForm):
    full_name = forms.CharField(label='ФИО',max_length=100,required=True,widget=forms.TextInput(attrs={'placeholder':'Иванов Иван Иванович'}))
    username = forms.CharField(label='Логин',min_length=6,max_length=30,required=True,widget=forms.TextInput(attrs={'placeholder':'login123'}))
    password1 = forms.CharField(label='пароль',min_length=8,widget=forms.PasswordInput,required=True)
    password2 = forms.CharField(label='повторите пароль', widget=forms.PasswordInput, required=True)
    email=forms.EmailField(label='почта',required=True,widget=forms.EmailInput(attrs={'placeholder':'example@mail.com'}))
    phone = forms.CharField(label='телефон',required=True,widget=forms.TextInput(attrs={'placeholder':'8(999)123-45-67'}))
    
    class Meta:
        model=User
        fields = ('username', 'full_name', 'email', 'phone', 'password1', 'password2')

    def clean_password2(self):
        p1 = self.cleaned_data.get('password1')
        p2 = self.cleaned_data.get('password2')

        if p1 != p2:
            raise forms.ValidationError("Пароли не совпадают!")

        validate_password(p1)
        return p2
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not re.fullmatch(r'[A-Za-z0-9]{6,}',username):
            raise ValidationError ('Логин должен содержать только латиницу и цифры, минимум 6 символов')
        if User.objects.filter(username=username).exists():
            raise ValidationError("Такой логин уже существует")
        return username
    
    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name')
        if not re.fullmatch(r'[А-Яа-яЁё]+ [А-Яа-яЁё]+ [А-Яа-яЁё]+', full_name):
            raise ValidationError("ФИО только кириллица и пробелы")
        return full_name
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if len(phone) != 15:
            raise forms.ValidationError("Некорректный номер")
        return phone
    
class CourseRequestForm(forms.ModelForm):
    date_start = forms.DateField(
        label='Дата начала',
        widget=forms.DateInput(
            attrs={
                'type': 'date', 
                'class': 'input-field'
            }
        )
    )

    class Meta:
        model = CourseRequest
        fields = ['course', 'date_start']
        labels = {
            'course': 'Курс',
        }
        widgets = {
            'course': forms.Select(attrs={'class': 'input-field'}),
        }

    def clean_date_start(self):
        from datetime import date
        selected_date = self.cleaned_data.get("date_start")

        if selected_date < date.today():
            raise forms.ValidationError("Нельзя выбрать дату в прошлом!")

        return selected_date


class LoginForm(forms.Form):
    username = forms.CharField(label="Логин", widget=forms.TextInput(attrs={'placeholder': 'login123'}))
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль'}))

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        user = authenticate(username=username, password=password)
        if user is None:
        
            raise forms.ValidationError("Неправильный логин или пароль. Попробуйте снова.")

        cleaned_data['user'] = user
        return cleaned_data

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if not username or not password:
            raise forms.ValidationError("Все поля должны быть заполнены!")

 
        user = authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError("Неверное имя пользователя или пароль")

        cleaned_data['user'] = user
        return cleaned_data
        
 
class ReviewForm(forms.ModelForm):
    class Meta:
        model = CourseRequest
        fields = ['review']
        widgets = {
            'review': forms.Textarea(
                attrs={
                    'class': 'input-field review-textarea',
                    'placeholder': 'Оставьте ваш отзыв здесь...',
                    'rows': 6
                }
            )
        }
    
