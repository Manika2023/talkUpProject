from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required

# create views
def index(request):
    return render(request, 'meetings_app/index.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'meetings_app/login.html', {'success': "Registration successful. Please login."})
        else:
            error_message = form.errors.as_text()
            return render(request, 'meetings_app/register.html', {'error': error_message})

    return render(request, 'meetings_app/register.html')


def login_view(request):
    if request.method=="POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        print(user)
        if user is not None:
            auth_login(request, user)
            return redirect("dashboard")
        else:
            return render(request, 'meetings_app/login.html', {'error': "Invalid credentials. Please try again."})

    return render(request, 'meetings_app/login.html')

@login_required
def dashboard(request):
    return render(request, 'meetings_app/dashboard.html',{"name":request.user.first_name})

@login_required
def videocall(request):
    return render(request,'meetings_app/videocall.html',{'name': request.user.first_name + " " + request.user.last_name})

@login_required
def logout_view(request):
    logout(request)
    return redirect('/login') 

@login_required
def join_room(request):
    if request.method=="POST":
        roomID=request.POST.get('roomID')
        return redirect("/meeting?roomID=" + roomID)
    return render(request,'meetings_app/joinroom.html')

# create function for home page

def home(request):
    return render(request,'meetings_app/home.html')

def about(request):
    return render(request,'meetings_app/about.html')