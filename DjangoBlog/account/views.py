from django.shortcuts import render, redirect, reverse, HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User


def login_page(request):
    return render(request, 'login.html')


def signup_page(request):
    return render(request, 'register.html')


def register_(req):
    if req.method == 'POST':
        username = req.POST.get('username', False)
        password = req.POST.get('password', False)
        email = req.POST.get('email', False)

        if False in [username, password, email]:
            return HttpResponse("there is an error")
        else:
            user = User.objects.create_user(username=username, password=password, email=email)
            return redirect('account:login_page')


def login_(req):
    if req.method == 'POST':
        username = req.POST.get('username', False)
        password = req.POST.get('password', False)
        email = req.POST.get('email', False)
        if False in [username, password, email]:
            return HttpResponse("there is an error")
        else:
            user = authenticate(username=username, password=password, email=email)
            login(req, user)
            return redirect(reverse('home'))


def logout_(req):
    logout(req)
    return redirect(reverse('home'))


def profile_page(request):
    return render(request, 'profile.html')