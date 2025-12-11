from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm,CourseRequestForm, ReviewForm,LoginForm
from .models import CourseRequest
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

from django.contrib.auth.models import User


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password1'],
                first_name=form.cleaned_data['full_name'], 
            )
            
            messages.success(request, f"Добро пожаловать, {user.username}!")
            return redirect('login')  
        else:
            messages.error(request, "Проверьте корректность введённых данных")
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def home(request):
    if request.method == 'POST':
        form = CourseRequestForm(request.POST)
        if form.is_valid():
            course_request = form.save(commit=False)
            course_request.user = request.user
            course_request.save()
            messages.success(request, 'Заявка успешно отправлена!')
            return redirect('home')
    else:
        form = CourseRequestForm()
    return render(request, 'accounts/home.html', {'form': form})

@login_required
def profile(request):
    requests = CourseRequest.objects.filter(user=request.user)
    return render (request,"accounts/profile.html",{"requests":requests})

class LoginView(LoginView):
    template_name = 'accounts/login.html'

    def get_success_url(self):
        if self.request.user.is_superuser:
            return '/admin/'
        return reverse_lazy('home') 
    
@login_required
def add_review(request, pk):
    course_request = get_object_or_404(CourseRequest, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=course_request)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ReviewForm(instance=course_request)
    
    return render(request, 'accounts/review.html', {'form': form})

def login_view(request):
    form = LoginForm(request.POST or None)
    
    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)

               
                if user.is_superuser:
                    return redirect('/admin/')
                
               
                return redirect('home')
            else:
                form.add_error(None, "Неправильный логин или пароль")
    
    return render(request, 'accounts/login.html', {'form': form})