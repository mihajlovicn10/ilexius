from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth import login, logout, authenticate
from .models import User

# Create your views here.

def register(request): 
    if request.method == "POST": 
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        username = request.POST["username"]
        password = request.POST["password"]
        user = User.objects.create_user(email,password,username=username,first_name=first_name,last_name=last_name)
        user.login_count = 0
        user.login_attempt = 0
        user.save() 
        return redirect("/login")
    return render(request, 'register.html')

def login_view(request): 
    if request.user.is_authenticated:
        return redirect(f"/profile/{request.user.username}")
    if request.method == 'POST': 
        username = request.POST["username"]
        password = request.POST["password"]
        user= authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            user.login_count += 1
            user.save()
            login(request, user)
            return redirect(f"/profile/{request.user.username}")
        else:
            try:
                user = User.objects.get(username=username)
                user.login_attempt += 1
                user.save()
            except User.DoesNotExist:
                return render(request, "login.html", context={"message":"No such user"})
            return render(request, "login.html", context={"message":"Wrong password"})

    return render(request, "login.html")

def logout_view(request): 
    logout(request)
    return redirect("/login")

def profile(request, username):  
       
    user = User.objects.get(username=username)
    print(user.is_superuser)
    login_count = user.login_count
    login_attempt = user.login_attempt
    if request.user.is_authenticated:
        logged_as = request.user.username
    else:
        logged_as = "not logged in"
    return render(request, "user.html", context={"username":username, "logged_as":logged_as, "login_count":login_count, "login_attempt":login_attempt, "pk":user.id})

def login_as(request, pk):
    logout(request)
    user = User.objects.get(pk=pk)
    user.login_count += 1
    user.save()
    #user = authenticate(request, username=user.username, password=user.password)
    print(user)
    login(request,user)
    return redirect(f"/profile/{user.username}")

def index(request):
    return redirect("/login")