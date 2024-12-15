from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Profile


def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username already Exists")
                return redirect('register')
            if User.objects.filter(email=email).exists():
                messages.info(request, "Email already Exists")
                return redirect('register')
            else:
                User.objects.create_user(username=username, email=email, password=password).save()
                return redirect('login')
        else:
            messages.info(request, "Password should match")
            return redirect('register')

    return render(request, "account/register.html")


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect("index")
        else:
            messages.info(request, 'Username or Password is incorrect')
            return redirect("login")

    return render(request, "account/login.html")

def logout_view(request):
    logout(request)
    return render(request, 'index.html')

def profile_detail(request):
    return render(request, 'profile/profile.html')

@login_required
def profile_detail(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'profile/profile.html', {'profile': profile})

@login_required
def profile_edit(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        profile.bio = request.POST['bio']
        if 'profile_pic' in request.FILES:
            profile.profile_pic = request.FILES['profile_pic']
        profile.save()
        return redirect('profile')
    return render(request, 'profile/profile_edit.html', {'profile': profile})